# Prompt Optimizer Skill

一个智能的 Claude Code Skill，可以自动优化用户的提示词，提升 AI 输出质量。

## 功能特性

- 智能提示词优化
- 四种优化策略（清晰化、上下文增强、示例驱动、精简化）
- 三种优化模式（minimal、moderate、aggressive）
- 学习用户偏好，越用越智能
- 支持中英文提示词

## 快速开始

### 安装方法

#### 方法 1：通过 Claude Code Marketplace（推荐）

```bash
# 在 Claude Code 中运行
/plugin marketplace add <your-username>/skills

# 安装 skill 包
/plugin install example-skills
```

#### 方法 2：手动安装

1. 将 `prompt-optimizer` 文件夹复制到你的 skills 项目目录：
   ```bash
   cp -r prompt-optimizer /path/to/your/skills/skills/
   ```

2. 更新你的 marketplace.json：
   ```json
   {
     "skills": [
       "./skills/prompt-optimizer",
       ...
     ]
   }
   ```

3. 在 Claude Code 中重新加载 skills

### 使用方法

在 Claude Code 中输入带有触发词的提示词：

```
帮我写个API，优化
```

或者：

```
create a database schema, improve
```

**触发词**：`优化`、`improve`、`optimize`、`改进`、`refine`、`重写`

## 开发

### 目录结构

```
prompt-optimizer/
├── SKILL.md                      # 主指令文件
├── LICENSE.txt                   # MIT 许可证
├── README.md                     # 本文件
├── TESTING.md                    # 测试指南
├── scripts/
│   ├── optimize.py               # 核心优化器
│   └── memory.py                 # 反馈学习模块
└── references/
    ├── strategies.md             # 策略详细说明
    └── examples.md               # 优化示例
```

### 依赖要求

- Python 3.7+
- Claude Code

### 测试

```bash
# 测试优化功能
cd skills/prompt-optimizer
python scripts/optimize.py optimize \
  --prompt "帮我写个API" \
  --context-json '{"task": "create API", "tech_stack": ["Python", "FastAPI"]}' \
  --mode moderate

# 查看学习统计
python scripts/memory.py summary
```

## 发布你的版本

### 创建自己的 Skill 仓库

如果你想基于这个项目创建自己的版本：

1. **Fork 这个仓库**
   ```bash
   # 在 GitHub 上 fork 这个仓库
   git clone https://github.com/your-username/skills.git
   cd skills
   ```

2. **修改 SKILL.md**
   - 修改 `name` 字段为你的 skill 名称
   - 修改 `description` 使其符合你的需求
   - 调整优化策略和触发词

3. **测试你的修改**
   ```bash
   python scripts/optimize.py optimize --prompt "测试" --context-json '{}'
   ```

4. **提交并发布**
   ```bash
   git add .
   git commit -m "Customize prompt optimizer"
   git push origin main
   ```

5. **在 marketplace.json 中注册**
   ```json
   {
     "name": "my-custom-skills",
     "skills": [
       "./skills/prompt-optimizer"
     ]
   }
   ```

6. **分享你的仓库**
   - 在 GitHub 上发布 release
   - 分享仓库链接：`https://github.com/your-username/skills`
   - 用户可以通过以下方式安装：
     ```bash
     /plugin marketplace add your-username/skills
     ```

### 打包为独立 Skill

如果你想单独发布这个 skill：

1. **创建打包脚本**
   ```bash
   # 使用 skill-creator 中的打包工具
   python skills/skill-creator/scripts/package_skill.py skills/prompt-optimizer
   ```

2. **发布 .skill 文件**
   - 上传到 GitHub Releases
   - 或者直接分享文件夹

3. **用户安装**
   ```bash
   # 下载 .skill 文件后
   /plugin install path/to/prompt-optimizer.skill
   ```

## 分享方式总结

| 方式 | 难度 | 适用场景 | 链接示例 |
|-----|------|---------|---------|
| GitHub Marketplace | 简单 | 公开项目 | `github.com/your-username/skills` |
| 直接分享文件夹 | 最简单 | 小范围分享 | Google Drive、OneDrive |
| .skill 文件 | 中等 | 独立分发 | GitHub Releases |
| npm 包 | 复杂 | 大规模分发 | npmjs.com |

## 许可证

MIT License - 可以自由修改和分发

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- GitHub Issues: [提出问题](https://github.com/your-username/skills/issues)
- Discussions: [讨论区](https://github.com/your-username/skills/discussions)

## 致谢

基于 [Anthropic Agent Skills](https://github.com/anthropics/skills) 项目开发
