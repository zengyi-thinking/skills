#!/usr/bin/env python3
"""
Memory Manager - 反馈管理与偏好学习

负责:
1. 记录用户的优化反馈（接受/拒绝/编辑）
2. 从历史反馈中学习用户偏好
3. 持久化用户偏好数据

使用方式:
    python scripts/memory.py record-feedback --original "..." --optimized "..." --accepted true
    python scripts/memory.py summary
    python scripts/memory.py export
    python scripts/memory.py reset
"""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys


# 数据目录位置
DATA_DIR = Path.home() / ".claude" / "data" / "prompt-optimizer"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PREFERENCES_FILE = DATA_DIR / "user_preferences.json"
HISTORY_FILE = DATA_DIR / "optimization_history.json"


class MemoryManager:
    """记忆管理器：处理反馈并学习用户偏好"""

    def __init__(self):
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """确保数据目录存在"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def record_feedback(
        self,
        original: str,
        optimized: str,
        accepted: bool,
        user_edits: Optional[str] = None,
        strategies_used: Optional[List[str]] = None
    ):
        """
        记录用户反馈并更新偏好模型

        参数:
        - original: 原始提示词
        - optimized: 优化后的提示词
        - accepted: 是否接受了优化
        - user_edits: 用户的编辑（如果有）
        - strategies_used: 使用的策略列表
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "original": original,
            "optimized": optimized,
            "accepted": accepted,
            "user_edits": user_edits,
            "strategies_used": strategies_used or []
        }

        # 1. 保存到历史
        self._append_history(entry)

        # 2. 更新偏好模型
        if accepted:
            self._learn_from_acceptance(optimized, user_edits, strategies_used)
        else:
            self._learn_from_rejection(original, strategies_used)

        print(f"[OK] 反馈已记录 (accepted={accepted})")

    def _learn_from_acceptance(
        self,
        accepted_prompt: str,
        user_edits: Optional[str],
        strategies: Optional[List[str]]
    ):
        """从接受的优化中学习"""
        prefs = self._load_preferences()

        # 更新策略偏好（接受过的策略权重增加）
        if "strategy_weights" not in prefs:
            prefs["strategy_weights"] = {}

        for strategy in (strategies or []):
            current_weight = prefs["strategy_weights"].get(strategy, 0.5)
            prefs["strategy_weights"][strategy] = min(1.0, current_weight + 0.1)

        # 如果用户有编辑，分析编辑模式
        if user_edits and user_edits != accepted_prompt:
            edit_patterns = self._analyze_edits(accepted_prompt, user_edits)
            if "edit_patterns" not in prefs:
                prefs["edit_patterns"] = []
            prefs["edit_patterns"].extend(edit_patterns)
            # 只保留最近 50 条
            prefs["edit_patterns"] = prefs["edit_patterns"][-50:]

        # 学习偏好长度
        final_prompt = user_edits if user_edits else accepted_prompt
        final_length = len(final_prompt.split())
        if "preferred_lengths" not in prefs:
            prefs["preferred_lengths"] = []
        prefs["preferred_lengths"].append(final_length)
        # 只保留最近 100 次
        prefs["preferred_lengths"] = prefs["preferred_lengths"][-100:]

        # 学习详细程度偏好
        if "detail_level_history" not in prefs:
            prefs["detail_level_history"] = []
        if final_length < 50:
            prefs["detail_level_history"].append("low")
        elif final_length < 150:
            prefs["detail_level_history"].append("medium")
        else:
            prefs["detail_level_history"].append("high")
        prefs["detail_level_history"] = prefs["detail_level_history"][-100:]

        # 更新最后使用时间
        prefs["last_used"] = datetime.now().isoformat()

        self._save_preferences(prefs)

    def _learn_from_rejection(
        self,
        original_prompt: str,
        strategies: Optional[List[str]]
    ):
        """从拒绝的优化中学习"""
        prefs = self._load_preferences()

        # 降低被拒绝策略的权重
        if "strategy_weights" not in prefs:
            prefs["strategy_weights"] = {}

        for strategy in (strategies or []):
            current_weight = prefs["strategy_weights"].get(strategy, 0.5)
            prefs["strategy_weights"][strategy] = max(0.0, current_weight - 0.15)

        # 记录用户偏好原始风格
        if "prefers_original_style_count" not in prefs:
            prefs["prefers_original_style_count"] = 0
        prefs["prefers_original_style_count"] += 1

        # 记录原始长度偏好
        original_length = len(original_prompt.split())
        if "preferred_lengths" not in prefs:
            prefs["preferred_lengths"] = []
        prefs["preferred_lengths"].append(original_length)
        prefs["preferred_lengths"] = prefs["preferred_lengths"][-100:]

        # 更新最后使用时间
        prefs["last_used"] = datetime.now().isoformat()

        self._save_preferences(prefs)

    def _analyze_edits(self, original: str, edited: str) -> List[str]:
        """
        分析用户编辑模式

        返回检测到的模式列表
        """
        patterns = []

        original_words = set(original.lower().split())
        edited_words = set(edited.lower().split())

        # 检测添加示例
        if "示例" in edited or "example" in edited.lower():
            if "示例" not in original and "example" not in original.lower():
                patterns.append("likes_examples")

        # 检测偏好简洁
        if len(edited) < len(original) * 0.8:
            patterns.append("prefers_concise")

        # 检测偏好详细
        if len(edited) > len(original) * 1.5:
            patterns.append("prefers_detailed")

        # 检测添加了技术要求
        tech_keywords = ["测试", "test", "安全", "security", "性能", "performance",
                         "错误处理", "error handling", "文档", "documentation"]
        added_tech_keywords = [
            kw for kw in tech_keywords
            if kw in edited.lower() and kw not in original.lower()
        ]
        if added_tech_keywords:
            patterns.append("likes_technical_details")

        # 检测添加了输出格式
        format_keywords = ["json", "markdown", "表格", "list", "格式"]
        added_format_keywords = [
            kw for kw in format_keywords
            if kw in edited.lower() and kw not in original.lower()
        ]
        if added_format_keywords:
            patterns.append("likes_output_specs")

        return patterns

    def _load_preferences(self) -> Dict:
        """加载用户偏好"""
        if PREFERENCES_FILE.exists():
            try:
                with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # 返回默认偏好
        return self._get_default_preferences()

    def _get_default_preferences(self) -> Dict:
        """获取默认偏好设置"""
        return {
            "created_at": datetime.now().isoformat(),
            "preferred_language": "auto",
            "detail_level": "medium",
            "likes_examples": True,
            "strategy_weights": {
                "clarity": 0.8,
                "context": 0.7,
                "examples": 0.6,
                "conciseness": 0.3
            },
            "edit_patterns": [],
            "preferred_lengths": [],
            "detail_level_history": []
        }

    def _save_preferences(self, prefs: Dict):
        """保存用户偏好"""
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)

    def _append_history(self, entry: Dict):
        """添加到历史记录"""
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []

        history.append(entry)

        # 只保留最近 200 条
        history = history[-200:]

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def get_summary(self) -> Dict:
        """获取学习摘要统计"""
        prefs = self._load_preferences()

        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        if not history:
            return {
                "total_optimizations": 0,
                "message": "暂无优化历史记录"
            }

        accepted_count = sum(1 for h in history if h.get("accepted"))
        total_count = len(history)
        acceptance_rate = accepted_count / total_count * 100 if total_count > 0 else 0

        # 计算平均偏好长度
        lengths = prefs.get("preferred_lengths", [])
        avg_length = sum(lengths) / len(lengths) if lengths else 50

        # 获取最常用的详细程度
        detail_history = prefs.get("detail_level_history", [])
        if detail_history:
            detail_counter = Counter(detail_history)
            most_common_detail = detail_counter.most_common(1)[0][0]
        else:
            most_common_detail = "medium"

        # 获取编辑模式统计
        edit_patterns = prefs.get("edit_patterns", [])
        pattern_counter = Counter(edit_patterns)

        summary = {
            "total_optimizations": total_count,
            "accepted_count": accepted_count,
            "acceptance_rate": f"{acceptance_rate:.1f}%",
            "avg_preferred_length": int(avg_length),
            "preferred_detail_level": most_common_detail,
            "favorite_strategies": self._get_top_strategies(
                prefs.get("strategy_weights", {})
            ),
            "common_edit_patterns": [
                {"pattern": p, "count": c}
                for p, c in pattern_counter.most_common(5)
            ],
            "last_used": prefs.get("last_used", "never")
        }

        return summary

    def _get_top_strategies(self, weights: Dict[str, float]) -> List[Dict]:
        """获取最常用的策略"""
        sorted_strategies = sorted(
            weights.items(),
            key=lambda x: x[1],
            reverse=True
        )

        strategy_names = {
            "clarity": "清晰化",
            "context": "上下文增强",
            "examples": "示例驱动",
            "conciseness": "精简化"
        }

        return [
            {
                "strategy": strategy_names.get(s, s),
                "weight": f"{w:.2f}"
            }
            for s, w in sorted_strategies[:4]
        ]

    def export_data(self) -> Dict:
        """导出所有数据（备份用）"""
        return {
            "preferences": self._load_preferences(),
            "history": self._load_history(),
            "exported_at": datetime.now().isoformat()
        }

    def _load_history(self) -> List:
        """加载历史记录"""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def reset_data(self, confirm: bool = False):
        """重置所有学习数据"""
        if not confirm:
            print("[!] 这将删除所有学习数据，请使用 --confirm 确认")
            return

        if PREFERENCES_FILE.exists():
            PREFERENCES_FILE.unlink()
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()

        # 重新初始化
        self.ensure_data_dir()
        default_prefs = self._get_default_preferences()
        self._save_preferences(default_prefs)

        print("[OK] 所有数据已重置")


def print_summary_table(summary: Dict):
    """格式化打印摘要表格"""
    print("\n" + "━" * 50)
    print("[Memory Manager] 学习统计摘要")
    print("━" * 50)

    if "message" in summary:
        print(f"\n{summary['message']}")
    else:
        print(f"\n总优化次数: {summary['total_optimizations']}")
        print(f"接受次数: {summary['accepted_count']}")
        print(f"接受率: {summary['acceptance_rate']}")
        print(f"\n平均偏好长度: {summary['avg_preferred_length']} 词")
        print(f"偏好详细程度: {summary['preferred_detail_level']}")

        if summary['favorite_strategies']:
            print(f"\n常用策略:")
            for s in summary['favorite_strategies']:
                print(f"  - {s['strategy']} (权重: {s['weight']})")

        if summary['common_edit_patterns']:
            print(f"\n编辑模式:")
            for p in summary['common_edit_patterns']:
                print(f"  - {p['pattern']}: {p['count']} 次")

        print(f"\n最后使用: {summary['last_used']}")

    print("━" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Memory Manager - 反馈管理与偏好学习",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # record-feedback 命令
    record_parser = subparsers.add_parser('record-feedback', help='记录用户反馈')
    record_parser.add_argument('--original', required=True, help='原始提示词')
    record_parser.add_argument('--optimized', required=True, help='优化后的提示词')
    record_parser.add_argument(
        '--accepted',
        required=True,
        type=lambda x: x.lower() in ('true', '1', 'yes', 'y'),
        help='是否接受优化 (true/false)'
    )
    record_parser.add_argument('--user-edits', help='用户编辑后的内容 (可选)')
    record_parser.add_argument(
        '--strategies',
        help='使用的策略 (JSON 数组格式)',
        default='[]'
    )

    # summary 命令
    summary_parser = subparsers.add_parser('summary', help='显示学习统计摘要')
    summary_parser.add_argument(
        '--format',
        choices=['table', 'json'],
        default='table',
        help='输出格式 (默认: table)'
    )

    # export 命令
    subparsers.add_parser('export', help='导出所有数据')

    # reset 命令
    reset_parser = subparsers.add_parser('reset', help='重置所有学习数据')
    reset_parser.add_argument(
        '--confirm',
        action='store_true',
        help='确认重置操作'
    )

    # path 命令
    subparsers.add_parser('path', help='显示数据文件路径')

    args = parser.parse_args()

    # 如果没有命令，显示帮助
    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = MemoryManager()

    if args.command == 'record-feedback':
        strategies = json.loads(args.strategies) if args.strategies else []
        manager.record_feedback(
            args.original,
            args.optimized,
            args.accepted,
            args.user_edits,
            strategies
        )

    elif args.command == 'summary':
        summary = manager.get_summary()
        if args.format == 'json':
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print_summary_table(summary)

    elif args.command == 'export':
        data = manager.export_data()
        print(json.dumps(data, ensure_ascii=False, indent=2))

    elif args.command == 'reset':
        manager.reset_data(confirm=args.confirm)

    elif args.command == 'path':
        print(f"数据目录: {DATA_DIR}")
        print(f"偏好文件: {PREFERENCES_FILE}")
        print(f"历史文件: {HISTORY_FILE}")
        if PREFERENCES_FILE.exists():
            print("\n[OK] 数据文件存在")
        else:
            print("\n[!] 数据文件不存在（首次使用）")


if __name__ == "__main__":
    main()
