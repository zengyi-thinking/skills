---
name: prompt-optimizer
description: Intelligent prompt optimizer that enhances user prompts by analyzing conversation context and applying learned preferences. Use this skill whenever a user's message contains keywords like "优化", "improve", "optimize", "改进", "refine", "重写", or explicitly asks to optimize/rewrite/enhance their prompt. Common triggers: "帮我写个API，优化", "create a database schema, improve", "implement login function, optimize", "重写这个提示词". The skill extracts conversation context, identifies technical stack, and generates optimized prompts with better structure and clarity.
license: MIT
---

# Prompt Optimizer

## Overview

Enhance user prompts by analyzing conversation context and applying intelligent optimization strategies. The skill learns from user feedback over time to provide increasingly personalized prompt improvements.

**Key capabilities:**
- Structure unclear prompts with role definitions and task breakdowns
- Inject relevant technical context from conversation history
- Add appropriate level of detail based on user preferences
- Learn from user feedback to personalize future optimizations

---

## Workflow

### Step 1: Extract Context Information

Before calling the optimizer script, analyze the conversation to extract:

**Required context to extract:**

| Field | Description | Example |
|-------|-------------|---------|
| `task` | What does the user want to accomplish? | `"Implement user authentication"` |
| `tech_stack` | Languages, frameworks, tools mentioned | `["Python", "FastAPI", "React", "JWT"]` |
| `domain` | Domain area (if identifiable) | `"web_development"`, `"data_science"` |
| `history_summary` | Key points from previous messages | `"User is building a web application, has discussed database schema"` |

**Example context extraction:**

```json
{
  "task": "user authentication and authorization",
  "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL"],
  "domain": "web_development",
  "history_summary": "Building a web application with user management features"
}
```

### Step 2: Call Optimizer Script

```bash
python scripts/optimize.py optimize \
  --prompt "原始提示词" \
  --context-json '{"task": "...", "tech_stack": [...], ...}' \
  --mode "moderate" \
  --output-format "json"
```

**Modes:**
- `minimal` - Light improvements (add structure only)
- `moderate` (default) - Balanced optimization
- `aggressive` - Complete rewrite with examples and detailed requirements

**Custom strategies (optional):**
```bash
--strategies "clarity,context,examples"
```

### Step 3: Present Optimization to User

Display the optimization result in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Prompt 优化建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【原始提示词】
{original_prompt}

【优化版本】
{optimized_prompt}

【应用的策略】
{strategies_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请选择:
1. 使用优化版本
2. 编辑优化版本 (将打开编辑器)
3. 使用原始版本
4. 查看优化详情
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Handle User Choice

**Choice 1 - Use optimized:**
Execute the task using the optimized prompt.

**Choice 2 - Edit in editor:**
```bash
python scripts/optimize.py edit --prompt "{optimized_prompt}"
```
This opens the system default editor (VS Code/Vim/Nano) for user editing.

**Choice 3 - Use original:**
Execute the task using the original prompt.

**Choice 4 - Show details:**
Load and display [references/strategies.md](references/strategies.md) for detailed explanation.

### Step 5: Record Feedback

Always record user feedback to improve future optimizations:

```bash
python scripts/memory.py record-feedback \
  --original "{original_prompt}" \
  --optimized "{optimized_prompt}" \
  --accepted {true/false} \
  --user-edits "{edited_version_or_null}" \
  --strategies '["clarity","context"]'
```

This updates the user preference model for personalized future optimizations.

---

## Optimization Strategies

The optimizer applies these strategies based on context and mode:

### 1. Clarity (清晰化)
- Adds appropriate role definition
- Structures tasks with numbered lists
- Clarifies output format and constraints

**Best for:** Short, vague prompts

### 2. Context Enhancement (上下文增强)
- Injects tech stack information
- Adds domain-specific requirements
- Incorporates relevant conversation context

**Best for:** Technical tasks

### 3. Example-Driven (示例驱动)
- Requests input/output examples
- Asks for code templates
- Includes usage demonstrations

**Best for:** Tasks requiring specific formats

### 4. Conciseness (精简化)
- Removes redundant phrasing
- Consolidates similar requests
- Eliminates unnecessary prefixes

**Best for:** Overly verbose prompts

See [references/strategies.md](references/strategies.md) for detailed strategy documentation.

---

## Advanced Usage

### View Learning Statistics

```bash
python scripts/memory.py summary
```

Shows:
- Total optimizations and acceptance rate
- Preferred prompt length and detail level
- Most-used strategies
- Common edit patterns

### Export Learning Data

```bash
python scripts/memory.py export
```

Exports all preferences and history for backup or analysis.

### Reset Learning Data

```bash
python scripts/memory.py reset --confirm
```

Clears all learned preferences and starts fresh.

---

## Best Practices

### When to Use This Skill

Use the prompt optimizer when:
- User appends "优化", "improve", "optimize", "改进", or "refine"
- User explicitly asks to rewrite/enhance their prompt
- Prompt is unclear, vague, or lacks structure
- User wants better results from their prompts

### When NOT to Use

Do NOT use when:
- Prompt is already well-structured and clear
- User provides very specific, detailed requirements
- User wants to use their exact wording
- Prompt is part of a template or standardized format

### Context Extraction Tips

1. **Listen for technical keywords**: Framework names, languages, tools
2. **Summarize conversation history**: Focus on relevant technical context
3. **Identify the domain**: Web dev, data science, ML, DevOps, etc.
4. **Note user preferences**: From past interactions if available

### Mode Selection Guidelines

- **Minimal**: For already-decent prompts that just need structure
- **Moderate**: Default choice for most unclear prompts
- **Aggressive**: For very vague or incomplete prompts

---

## Examples

### Example 1: Web Development Task

**User:** "帮我写个登录功能，优化"

**Context to extract:**
```json
{
  "task": "implement user login functionality",
  "tech_stack": ["Python", "FastAPI", "React"],
  "domain": "web_development",
  "history_summary": "Building web application with authentication"
}
```

**Optimized result:**
```
作为资深后端开发工程师，请实现用户登录功能:

**技术栈**: Python, FastAPI, React

**要求**:
1. 使用 JWT 进行身份验证
2. 包含密码加密 (bcrypt)
3. 实现登录表单验证
4. 添加错误处理和安全措施

**请包含**:
- API 端点代码
- 前端登录表单
- 集成说明
```

### Example 2: Data Science Task

**User:** "analyze this data, improve"

**Context to extract:**
```json
{
  "task": "data analysis and visualization",
  "tech_stack": ["Python", "Pandas", "Matplotlib"],
  "domain": "data_science",
  "history_summary": "Working with sales dataset"
}
```

**Optimized result:**
```
作为数据科学专家，请分析这个数据集:

**技术栈**: Python, Pandas, Matplotlib

**分析步骤**:
1. 数据清洗和预处理
2. 探索性数据分析 (EDA)
3. 统计分析和可视化
4. 关键洞察和结论

**输出要求**:
- 清洗后的数据摘要
- 可视化图表
- 统计分析结果
- 可操作的洞察建议

**请包含代码示例和解释**
```

See [references/examples.md](references/examples.md) for more examples.

---

## Data Storage

User preferences and optimization history are stored in:
```
~/.claude/data/prompt-optimizer/
├── user_preferences.json      # Learned user preferences
└── optimization_history.json  # All optimization history
```

This allows the skill to learn and personalize across all projects.

---

## Troubleshooting

### Script not found
Ensure you're in the skill directory and scripts have execute permissions:
```bash
chmod +x scripts/*.py
```

### Python not found
The scripts require Python 3.7+. Install if needed.

### Editor not opening
The `edit` command tries VS Code first, then falls back to system `$EDITOR`, then common editors. Set your preferred editor:
```bash
export EDITOR=vim  # or your preferred editor
```

### Learning not working
Check data directory exists:
```bash
python scripts/memory.py path
```

If issues persist, use `python scripts/memory.py export` to backup data, then `reset --confirm` to start fresh.
