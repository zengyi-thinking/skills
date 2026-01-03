#!/usr/bin/env python3
"""
Prompt Optimizer - 核心优化逻辑

接收 Claude 传递的上下文参数，返回优化后的提示词。

使用方式:
    python scripts/optimize.py optimize --prompt "..." --context-json "{...}"
    python scripts/optimize.py edit --prompt "..."
    python scripts/optimize.py explain --context-json "{...}"
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional


# 数据目录位置（跨项目，用户级别）
DATA_DIR = Path.home() / ".claude" / "data" / "prompt-optimizer"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PREFERENCES_FILE = DATA_DIR / "user_preferences.json"
HISTORY_FILE = DATA_DIR / "optimization_history.json"


class PromptOptimizer:
    """提示词优化器"""

    def __init__(self):
        self.preferences = self._load_preferences()
        self.strategies = {
            "clarity": self._strategy_clarity,
            "context": self._strategy_context,
            "examples": self._strategy_examples,
            "conciseness": self._strategy_conciseness,
        }

    def optimize(
        self,
        prompt: str,
        context: Dict,
        mode: str = "moderate",
        custom_strategies: Optional[List[str]] = None
    ) -> Dict:
        """
        优化提示词

        参数由 Claude 传递:
        - prompt: 原始提示词
        - context: Claude 提取的上下文信息
        - mode: 优化模式 (minimal/moderate/aggressive)
        - custom_strategies: 自定义策略列表（可选）

        返回优化结果字典
        """
        result = {
            "original": prompt,
            "optimized": prompt,
            "strategies_applied": [],
            "explanation": [],
            "mode": mode
        }

        # 选择要应用的策略
        if custom_strategies:
            active_strategies = custom_strategies
        else:
            active_strategies = self._select_strategies_by_mode(mode, context)

        # 依次应用策略
        for strategy_name in active_strategies:
            if strategy_name in self.strategies:
                strategy_func = self.strategies[strategy_name]
                result["optimized"] = strategy_func(
                    result["optimized"],
                    context
                )
                result["strategies_applied"].append(strategy_name)
                result["explanation"].append(
                    f"[+] {self._get_strategy_description(strategy_name)}"
                )

        # 根据用户偏好调整
        result["optimized"] = self._apply_user_preferences(
            result["optimized"],
            context
        )

        return result

    def _select_strategies_by_mode(self, mode: str, context: Dict) -> List[str]:
        """根据模式选择策略"""
        if mode == "minimal":
            return ["clarity"]
        elif mode == "aggressive":
            strategies = ["clarity", "context", "examples", "conciseness"]
            # 过滤掉用户不喜欢的策略
            return self._filter_by_user_preferences(strategies)
        else:  # moderate
            strategies = ["clarity", "context"]
            # 根据上下文动态添加
            if context.get("tech_stack"):
                strategies.append("context")
            if len(context.get("original_prompt", prompt := "")) < 50:
                strategies.append("examples")
            return self._filter_by_user_preferences(strategies)

    def _filter_by_user_preferences(self, strategies: List[str]) -> List[str]:
        """根据用户偏好过滤策略"""
        weights = self.preferences.get("strategy_weights", {})
        # 过滤掉权重过低的策略（< 0.3）
        return [
            s for s in strategies
            if weights.get(s, 0.5) >= 0.3
        ]

    def _strategy_clarity(self, prompt: str, context: Dict) -> str:
        """策略1: 结构化清晰化"""
        # 检查是否已有角色设定
        role_indicators = ["作为", "你是", "act as", "you are"]
        has_role = any(indicator in prompt.lower() for indicator in role_indicators)

        if not has_role:
            role = self._infer_role(context)
            prompt = f"作为{role}，请：\n\n{prompt}"

        # 检查是否需要添加任务结构
        if len(prompt) < 150 and "步骤" not in prompt and "step" not in prompt.lower():
            if "\n\n**要求**" not in prompt:
                prompt += "\n\n**要求**：\n1. 分析需求\n2. 提供实现方案\n3. 包含代码示例\n4. 说明注意事项"

        return prompt

    def _strategy_context(self, prompt: str, context: Dict) -> str:
        """策略2: 上下文增强"""
        tech_stack = context.get("tech_stack", [])
        domain = context.get("domain", "")

        # 检查是否已经包含技术栈信息
        has_tech_info = any(
            tech.lower() in prompt.lower()
            for tech in tech_stack
        )

        if not has_tech_info and tech_stack:
            context_section = f"**技术栈**: {', '.join(tech_stack)}\n\n"
            prompt = context_section + prompt

        # 添加领域特定信息
        if domain and domain not in prompt.lower():
            domain_guidance = self._get_domain_guidance(domain)
            if domain_guidance:
                prompt += f"\n\n**领域要求**: {domain_guidance}"

        return prompt

    def _strategy_examples(self, prompt: str, context: Dict) -> str:
        """策略3: 添加示例要求"""
        example_keywords = ["示例", "example", "例子", "sample"]
        has_example_request = any(
            keyword in prompt.lower()
            for keyword in example_keywords
        )

        if not has_example_request:
            prompt += "\n\n**请包含使用示例和输出格式说明**"

        return prompt

    def _strategy_conciseness(self, prompt: str, context: Dict) -> str:
        """策略4: 精简化"""
        lines = prompt.split('\n')

        # 去除空行
        lines = [line for line in lines if line.strip()]

        # 去除重复的行（简单去重）
        seen = set()
        unique_lines = []
        for line in lines:
            normalized = line.strip().lower()
            if normalized not in seen:
                unique_lines.append(line)
                seen.add(normalized)

        return '\n'.join(unique_lines)

    def _infer_role(self, context: Dict) -> str:
        """根据上下文推断合适的角色"""
        tech_stack = context.get("tech_stack", [])
        domain = context.get("domain", "")

        # 根据技术栈推断
        backend_frameworks = ["Python", "FastAPI", "Django", "Flask", "Node.js", "Express", "Go", "Java", "Spring"]
        frontend_frameworks = ["React", "Vue", "Angular", "TypeScript", "Next.js", "Nuxt"]
        devops_tools = ["Docker", "Kubernetes", "CI/CD", "Terraform", "AWS"]
        data_tools = ["Pandas", "NumPy", "PyTorch", "TensorFlow", "SQL"]
        mobile_tools = ["React Native", "Flutter", "Swift", "Kotlin"]

        if any(t in tech_stack for t in backend_frameworks):
            return "资深后端开发工程师"
        elif any(t in tech_stack for t in frontend_frameworks):
            return "前端开发专家"
        elif any(t in tech_stack for t in devops_tools):
            return "DevOps 工程师"
        elif any(t in tech_stack for t in data_tools):
            return "数据科学专家"
        elif any(t in tech_stack for t in mobile_tools):
            return "移动应用开发工程师"

        # 根据领域推断
        if domain == "web_development":
            return "全栈开发工程师"
        elif domain == "data_science":
            return "数据科学专家"
        elif domain == "machine_learning":
            return "机器学习工程师"
        elif domain == "devops":
            return "DevOps 工程师"

        return "资深开发工程师"

    def _get_domain_guidance(self, domain: str) -> str:
        """获取领域特定的指导"""
        guidance_map = {
            "web_development": "遵循 RESTful 最佳实践，确保代码可维护和可扩展",
            "machine_learning": "包含数据处理、模型训练和评估的完整流程",
            "data_science": "确保数据清洗、探索性分析和可视化的完整性",
            "devops": "遵循基础设施即代码原则，确保配置的可重复性",
            "security": "遵循安全最佳实践，考虑常见漏洞防护"
        }
        return guidance_map.get(domain, "")

    def _apply_user_preferences(self, prompt: str, context: Dict) -> str:
        """应用学习的用户偏好"""
        # 语言偏好
        preferred_lang = self.preferences.get("preferred_language", "auto")
        if preferred_lang != "auto":
            # 这里可以根据需要实现语言转换
            pass

        # 详细程度
        detail_level = self.preferences.get("detail_level", "medium")
        word_count = len(prompt.split())

        if detail_level == "low" and word_count > 150:
            # 用户偏好简洁，当前提示词较长
            # 这里可以实现更智能的精简逻辑
            pass
        elif detail_level == "high" and word_count < 80:
            # 用户偏好详细，当前提示词较短
            prompt += "\n\n**请详细说明实现细节、最佳实践和可能的注意事项**"

        # 检查用户是否偏好示例
        if self.preferences.get("likes_examples", True):
            if "示例" not in prompt and "example" not in prompt.lower():
                prompt += "\n\n**请提供完整的使用示例**"

        return prompt

    def _load_preferences(self) -> Dict:
        """加载用户偏好"""
        if PREFERENCES_FILE.exists():
            try:
                with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # 默认偏好
        return {
            "preferred_language": "auto",
            "detail_level": "medium",
            "likes_examples": True,
            "strategy_weights": {
                "clarity": 0.8,
                "context": 0.7,
                "examples": 0.6,
                "conciseness": 0.3
            }
        }

    def _get_strategy_description(self, strategy_name: str) -> str:
        """获取策略的中文描述"""
        descriptions = {
            "clarity": "清晰化 - 添加角色和结构",
            "context": "上下文增强 - 注入技术栈信息",
            "examples": "示例驱动 - 添加示例要求",
            "conciseness": "精简化 - 去除冗余内容"
        }
        return descriptions.get(strategy_name, strategy_name)


def edit_in_editor(text: str) -> str:
    """
    在系统默认编辑器中打开文本供用户编辑

    优先使用 VS Code，然后尝试其他常见编辑器
    """
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.md',
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(text)
        temp_path = f.name

    try:
        print(f"\n[*] 正在打开编辑器: {temp_path}")
        print("(编辑完成后保存并关闭编辑器)")

        # 优先级: VS Code > 环境变量 EDITOR > 常见编辑器
        editor = os.environ.get('EDITOR')

        # 尝试 VS Code
        try:
            subprocess.call(['code', '--wait', temp_path])
        except (FileNotFoundError, subprocess.SubprocessError):
            # 尝试环境变量指定的编辑器
            if editor:
                try:
                    subprocess.call([editor, temp_path])
                except (FileNotFoundError, subprocess.SubprocessError):
                    pass
            else:
                # 尝试其他常见编辑器
                for cmd in ['vim', 'nano', 'notepad', 'gedit']:
                    try:
                        subprocess.call([cmd, temp_path])
                        break
                    except (FileNotFoundError, subprocess.SubprocessError):
                        continue
                else:
                    print(f"\n[!] 无法自动打开编辑器")
                    print(f"请手动编辑文件: {temp_path}")
                    input("编辑完成后按回车继续...")

        # 读取编辑后的内容
        with open(temp_path, 'r', encoding='utf-8') as f:
            edited_content = f.read()

        print("[OK] 编辑完成")
        return edited_content

    except Exception as e:
        print(f"[ERROR] 编辑器打开失败: {e}")
        return text
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_path)
        except:
            pass


def print_optimization_result(result: Dict):
    """格式化输出优化结果"""
    print("\n" + "━" * 60)
    print("[Prompt Optimizer] 优化建议")
    print("━" * 60)

    print(f"\n【原始提示词】")
    print(result["original"])

    print(f"\n【优化版本】")
    print(result["optimized"])

    if result["strategies_applied"]:
        print(f"\n【应用的策略】")
        for explanation in result["explanation"]:
            print(f"  {explanation}")

    print("\n" + "━" * 60)
    print("请选择:")
    print("  1. 使用优化版本")
    print("  2. 编辑优化版本 (将打开编辑器)")
    print("  3. 使用原始版本")
    print("  4. 查看优化详情")
    print("━" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Optimizer - 提示词优化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # optimize 命令
    optimize_parser = subparsers.add_parser('optimize', help='优化提示词')
    optimize_parser.add_argument('--prompt', required=True, help='原始提示词')
    optimize_parser.add_argument('--context-json', required=True, help='上下文信息 (JSON 格式)')
    optimize_parser.add_argument(
        '--mode',
        default='moderate',
        choices=['minimal', 'moderate', 'aggressive'],
        help='优化模式 (默认: moderate)'
    )
    optimize_parser.add_argument(
        '--strategies',
        help='自定义策略 (逗号分隔, 如: clarity,examples)'
    )
    optimize_parser.add_argument(
        '--output-format',
        choices=['text', 'json'],
        default='json',
        help='输出格式 (默认: json, 供 Claude 解析)'
    )

    # edit 命令
    edit_parser = subparsers.add_parser('edit', help='在编辑器中编辑提示词')
    edit_parser.add_argument('--prompt', required=True, help='要编辑的提示词')

    # explain 命令
    explain_parser = subparsers.add_parser('explain', help='显示策略详细说明')

    # 添加 --version 作为可选参数
    parser.add_argument('--version', action='version', version='Prompt Optimizer v1.0.0')

    args = parser.parse_args()

    # 如果没有命令，显示帮助
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'optimize':
        # 解析上下文
        try:
            context = json.loads(args.context_json)
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}", file=sys.stderr)
            sys.exit(1)

        # 解析自定义策略
        custom_strategies = None
        if args.strategies:
            custom_strategies = [s.strip() for s in args.strategies.split(',')]

        # 执行优化
        optimizer = PromptOptimizer()
        result = optimizer.optimize(
            args.prompt,
            context,
            args.mode,
            custom_strategies
        )

        # 输出结果
        if args.output_format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_optimization_result(result)

    elif args.command == 'edit':
        edited = edit_in_editor(args.prompt)
        print(json.dumps({"edited": edited}, ensure_ascii=False))

    elif args.command == 'explain':
        # 显示策略说明
        strategies_file = Path(__file__).parent.parent / "references" / "strategies.md"
        if strategies_file.exists():
            with open(strategies_file, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("策略说明文件未找到")

    elif args.command == 'version':
        print("Prompt Optimizer v1.0.0")


if __name__ == "__main__":
    main()
