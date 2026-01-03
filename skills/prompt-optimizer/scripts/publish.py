#!/usr/bin/env python3
"""
Prompt Optimizer - 快速发布脚本

用法:
    python scripts/publish.py           # 交互式发布
    python scripts/publish.py --check   # 检查发布准备
    python scripts/publish.py --pack    # 打包 skill
"""
import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path


def check_readiness(skill_path: Path) -> dict:
    """检查 skill 是否准备好发布"""
    checks = {
        "files_exist": [],
        "files_missing": [],
        "warnings": [],
        "ready": False
    }

    # 必需文件
    required_files = [
        "SKILL.md",
        "LICENSE.txt",
        "scripts/optimize.py",
        "scripts/memory.py"
    ]

    # 参考文件
    optional_files = [
        "references/strategies.md",
        "references/examples.md",
        "README.md",
        "TESTING.md"
    ]

    # 检查必需文件
    for file in required_files:
        file_path = skill_path / file
        if file_path.exists():
            checks["files_exist"].append(file)
        else:
            checks["files_missing"].append(file)

    # 检查可选文件
    for file in optional_files:
        file_path = skill_path / file
        if file_path.exists():
            checks["files_exist"].append(file)
        else:
            checks["warnings"].append(f"可选文件缺失: {file}")

    # 验证 SKILL.md frontmatter
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            if '---' not in content or 'name:' not in content:
                checks["warnings"].append("SKILL.md frontmatter 格式可能有问题")
            elif 'description:' not in content:
                checks["warnings"].append("SKILL.md 缺少 description 字段")

    # 检查 Python 脚本语法
    for script in ["scripts/optimize.py", "scripts/memory.py"]:
        script_path = skill_path / script
        if script_path.exists():
            try:
                subprocess.run(
                    ["python", "-m", "py_compile", str(script_path)],
                    capture_output=True,
                    check=True
                )
            except subprocess.CalledProcessError:
                checks["warnings"].append(f"{script} 语法错误")

    # 判断是否准备好
    checks["ready"] = len(checks["files_missing"]) == 0

    return checks


def pack_skill(skill_path: Path, output_dir: Path = None) -> Path:
    """打包 skill 为 .skill 文件（实际是 zip）"""
    if output_dir is None:
        output_dir = skill_path.parent

    skill_name = skill_path.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{skill_name}_{timestamp}.skill"

    print(f"[*] 正在打包 {skill_name}...")

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # 排除一些不需要的文件
                if any(part.startswith('.') or part == '__pycache__'
                       for part in file_path.parts):
                    continue

                arcname = file_path.relative_to(skill_path)
                zipf.write(file_path, arcname)
                print(f"  + {arcname}")

    print(f"[OK] 打包完成: {output_file}")
    print(f"    大小: {output_file.stat().st_size / 1024:.1f} KB")

    return output_file


def create_github_release_instructions(skill_path: Path):
    """创建 GitHub 发布说明"""
    instructions = f"""# GitHub 发布指南

## 1. 推送到 GitHub

```bash
cd {skill_path.parent}
git add .
git commit -m "Add prompt-optimizer skill"
git push origin main
```

## 2. 创建 GitHub Release

1. 访问你的仓库页面
2. 点击 "Releases" → "Create a new release"
3. 标签版本: v1.0.0
4. 发布标题: Prompt Optimizer Skill v1.0.0
5. 描述:

```
## Prompt Optimizer v1.0.0

智能提示词优化工具，支持：

- 四种优化策略（清晰化、上下文增强、示例驱动、精简化）
- 三种优化模式
- 学习用户偏好
- 支持中英文

## 安装方法

```bash
# 添加 marketplace
/plugin marketplace add your-username/skills

# 安装 skill
/plugin install example-skills
```

## 使用示例

```
帮我写个API，优化
```
```

6. 上传打包好的 .skill 文件
7. 点击 "Publish release"

## 3. 分享链接

发布后分享以下链接：
- Release: https://github.com/your-username/skills/releases/tag/v1.0.0
- 仓库: https://github.com/your-username/skills

## 4. 用户安装

用户可以通过以下方式安装：

```bash
# 方法 1: 通过 marketplace
/plugin marketplace add your-username/skills

# 方法 2: 直接安装 .skill 文件
/plugin install path/to/prompt-optimizer_X.skill
```
"""
    return instructions


def main():
    parser = argparse.ArgumentParser(
        description="Prompt Optimizer 发布工具"
    )
    parser.add_argument('--check', action='store_true', help='检查发布准备')
    parser.add_argument('--pack', action='store_true', help='打包 skill')
    parser.add_argument('--output-dir', help='输出目录')
    parser.add_argument('--instructions', action='store_true', help='显示发布说明')

    args = parser.parse_args()

    # 获取 skill 路径
    script_path = Path(__file__).resolve()
    skill_path = script_path.parent.parent

    print("=" * 60)
    print("Prompt Optimizer - 发布工具")
    print("=" * 60)
    print()

    # 检查准备情况
    checks = check_readiness(skill_path)

    print("【发布检查】")
    print(f"  必需文件: {len(checks['files_exist'])} 个存在")
    if checks["files_missing"]:
        print(f"  [ERROR] 缺失文件: {', '.join(checks['files_missing'])}")
        return 1

    if checks["warnings"]:
        print(f"  [WARNING] {len(checks['warnings'])} 个警告:")
        for warning in checks["warnings"]:
            print(f"    - {warning}")

    if checks["ready"]:
        print("  [OK] Skill 已准备好发布！")
    else:
        print("  [ERROR] Skill 未准备好发布")
        return 1

    print()

    # 执行请求的操作
    if args.check:
        print("[OK] 检查完成")
        return 0

    if args.instructions:
        instructions = create_github_release_instructions(skill_path)
        print(instructions)
        return 0

    if args.pack:
        output_dir = Path(args.output_dir) if args.output_dir else skill_path.parent
        output_file = pack_skill(skill_path, output_dir)
        print()
        print("【下一步】")
        print(f"1. 文件已打包: {output_file}")
        print(f"2. 上传到 GitHub Releases")
        print(f"3. 或直接分享给朋友")
        return 0

    # 默认：交互式发布
    print("【发布选项】")
    print("1. 打包 skill (.skill 文件)")
    print("2. 显示 GitHub 发布说明")
    print("3. 两者都做")
    print()

    choice = input("请选择 (1/2/3): ").strip()

    if choice == "1":
        pack_skill(skill_path)
    elif choice == "2":
        print(create_github_release_instructions(skill_path))
    elif choice == "3":
        output_file = pack_skill(skill_path)
        print()
        print(create_github_release_instructions(skill_path))
        print()
        print(f"[提示] 记得上传 {output_file.name} 到 GitHub Releases!")
    else:
        print("[ERROR] 无效选择")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
