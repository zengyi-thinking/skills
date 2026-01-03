# Prompt Optimizer Skill 测试指南

## 问题排查步骤

### 1. 确认 Skill 是否已安装

在 Claude Code 中运行以下命令查看已安装的 skills：

```
/plugin list
```

或者

```
/skills
```

检查 `prompt-optimizer` 是否在列表中。

### 2. 如果 Skill 未显示，需要安装

```bash
# 在 Claude Code 中运行
/plugin marketplace add anthropic/skills

# 然后安装具体的 skill 包
/plugin install example-skills
```

### 3. 验证 Skill 文件是否存在

确认以下文件存在：
- `skills/prompt-optimizer/SKILL.md`
- `skills/prompt-optimizer/scripts/optimize.py`
- `skills/prompt-optimizer/scripts/memory.py`

### 4. 测试触发词

尝试以下几种触发方式：

**方式 1：明确触发**
```
请使用 prompt-optimizer skill 优化我的提示词：帮我写个API
```

**方式 2：关键词触发**
```
帮我写个API，优化
```

**方式 3：英文触发**
```
create a REST API, optimize
```

### 5. 预期行为

当 Skill 被触发时，你应该看到：

1. Claude 分析对话上下文
2. 调用优化脚本
3. 显示优化结果，包含：
   - 原始提示词
   - 优化后的提示词
   - 应用的策略列表
4. 询问是否使用优化版本

### 6. 手动测试脚本

在终端中直接运行脚本测试：

```bash
cd skills/prompt-optimizer

# 测试优化功能
python scripts/optimize.py optimize \
  --prompt "帮我写个API" \
  --context-json '{"task": "create API", "tech_stack": ["Python", "FastAPI"], "domain": "web_development"}' \
  --mode moderate

# 测试内存管理
python scripts/memory.py summary
```

### 7. 常见问题

**Q: Skill 没有被触发**
A: 确保关键词明确，尝试使用 "请优化" 或 "please optimize"

**Q: 触发了但没有执行脚本**
A: 检查 Python 是否安装，运行 `python --version`

**Q: 脚本执行失败**
A: 检查文件权限和 Python 环境

### 8. 调试模式

如果需要查看详细的执行过程，可以在 SKILL.md 中添加调试指令。

## 期望输出示例

当输入 "帮我写个API，优化" 时，期望看到：

```
我检测到您想优化提示词。让我分析一下上下文...

[调用优化脚本]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Prompt Optimizer] 优化建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【原始提示词】
帮我写个API

【优化版本】
作为资深后端开发工程师，请创建 RESTful API：

**技术栈**: Python, FastAPI

**要求**：
1. 分析需求
2. 提供实现方案
3. 包含代码示例
4. 说明注意事项

【应用的策略】
[+] 清晰化 - 添加角色和结构
[+] 上下文增强 - 注入技术栈信息
```
