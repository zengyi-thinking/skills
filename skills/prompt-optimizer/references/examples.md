# Prompt 优化示例

本文档提供各种场景下的提示词优化示例，展示不同策略和模式的效果。

---

## 示例 1: Web 开发 - 用户认证

### 场景
用户正在开发一个 Web 应用，使用 Python + FastAPI + React 技术栈。

### 用户输入
```
"帮我写个登录功能，优化"
```

### Claude 提取的上下文
```json
{
  "task": "implement user authentication and login",
  "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL", "JWT"],
  "domain": "web_development",
  "history_summary": "User is building a web application with user management features"
}
```

### Minimal 模式优化
```
作为资深后端开发工程师，请实现用户登录功能：

**要求**：
1. 设计登录 API 端点
2. 实现身份验证逻辑
3. 处理登录成功和失败场景
```

### Moderate 模式优化（推荐）
```
作为资深后端开发工程师，请实现用户登录功能：

**技术栈**: Python, FastAPI, React, PostgreSQL, JWT

**领域要求**: 遵循 RESTful 最佳实践，确保代码可维护和可扩展

**要求**：
1. 设计登录 API 端点
2. 实现身份验证逻辑（使用 JWT）
3. 密码加密存储（bcrypt）
4. 添加输入验证和错误处理
5. 实现登录状态管理

**请包含**：
- 后端 API 代码
- 前端登录表单组件
- 集成说明
```

### Aggressive 模式优化
```
作为资深后端开发工程师，请实现完整的用户登录功能：

**技术栈**: Python, FastAPI, React, PostgreSQL, JWT

**领域要求**: 遵循 RESTful 最佳实践，确保代码可维护和可扩展，符合 OWASP 安全标准

**后端实现要求**：
1. 设计 RESTful 登录 API 端点 (/api/auth/login)
2. 实现用户身份验证逻辑：
   - 使用 bcrypt 进行密码哈希
   - 使用 JWT 生成访问令牌
   - 设置令牌过期时间
3. 输入验证：
   - 邮箱格式验证
   - 密码强度检查
4. 安全措施：
   - 防止暴力破解（速率限制）
   - SQL 注入防护
   - XSS 防护
5. 错误处理：
   - 用户不存在
   - 密码错误
   - 服务器错误

**前端实现要求**：
1. React 登录表单组件
2. 表单验证
3. JWT 令牌存储
4. 认证状态管理
5. 路由保护

**输出格式**：
- 完整的后端代码（FastAPI）
- 完整的前端代码（React + TypeScript）
- 数据库模型（SQLAlchemy）
- API 端点文档
- 集成测试示例
- 使用说明

**请包含代码示例和详细注释**
```

---

## 示例 2: 数据科学 - 数据分析

### 场景
用户需要分析销售数据，使用 Python 数据科学栈。

### 用户输入
```
"analyze this sales data, improve"
```

### Claude 提取的上下文
```json
{
  "task": "analyze sales dataset and provide insights",
  "tech_stack": ["Python", "Pandas", "Matplotlib", "Seaborn"],
  "domain": "data_science",
  "history_summary": "User has a sales dataset and wants to understand trends and patterns"
}
```

### 优化结果
```
作为数据科学专家，请分析这个销售数据集：

**技术栈**: Python, Pandas, Matplotlib, Seaborn

**分析步骤**：
1. **数据探索**
   - 加载数据集
   - 检查数据类型和缺失值
   - 基本统计摘要

2. **数据清洗**
   - 处理缺失值
   - 处理异常值
   - 数据类型转换

3. **探索性数据分析 (EDA)**
   - 销售趋势分析（时间序列）
   - 产品类别分析
   - 地区销售分析
   - 客户行为分析

4. **统计分析和可视化**
   - 关键指标计算（总销售额、平均订单值等）
   - 相关性分析
   - 趋势可视化
   - 热力图和分布图

5. **洞察和建议**
   - 识别关键趋势
   - 发现机会和风险
   - 提供可操作的洞察

**输出要求**：
- 清洗后的数据摘要
- Jupyter Notebook 代码
- 可视化图表（至少5个）
- 统计分析结果
- 关键洞察列表
- 改进建议

**请包含**：
- 完整代码实现
- 数据可视化示例
- 结果解释说明
```

---

## 示例 3: 机器学习 - 模型训练

### 场景
用户要训练一个图像分类模型。

### 用户输入
```
"train an image classifier"
```

### Claude 提取的上下文
```json
{
  "task": "train an image classification model",
  "tech_stack": ["Python", "PyTorch", "TensorFlow"],
  "domain": "machine_learning",
  "history_summary": "User wants to classify product images"
}
```

### 优化结果
```
作为机器学习工程师，请训练一个图像分类模型：

**技术栈**: Python, PyTorch, TensorFlow

**领域要求**: 包含数据处理、模型训练和评估的完整流程

**实现步骤**：
1. **数据准备**
   - 数据集加载和探索
   - 数据预处理和增强
   - 训练/验证/测试集划分

2. **模型设计**
   - 选择合适的架构（CNN/ResNet/EfficientNet）
   - 定义模型结构
   - 配置损失函数和优化器

3. **训练流程**
   - 实现训练循环
   - 添加早停（Early Stopping）
   - 学习率调度
   - 检查点保存

4. **模型评估**
   - 准确率、精确率、召回率
   - 混淆矩阵
   - ROC 曲线
   - 错误分析

5. **模型部署**
   - 模型保存和加载
   - 推理脚本
   - 性能优化

**输出要求**：
- 完整的训练代码
- 模型评估报告
- 可视化结果（训练曲线、混淆矩阵）
- 预测示例
- 模型文件

**请包含**：
- 代码实现
- 超参数说明
- 性能指标
- 改进建议
```

---

## 示例 4: DevOps - Docker 配置

### 场景
用户需要为应用创建 Docker 配置。

### 用户输入
```
"create docker setup for my app"
```

### Claude 提取的上下文
```json
{
  "task": "create Docker configuration for application",
  "tech_stack": ["Docker", "Node.js", "MongoDB", "Nginx"],
  "domain": "devops",
  "history_summary": "User has a Node.js web application that needs containerization"
}
```

### 优化结果
```
作为 DevOps 工程师，请为应用创建完整的 Docker 配置：

**技术栈**: Docker, Node.js, MongoDB, Nginx

**领域要求**: 遵循基础设施即代码原则，确保配置的可重复性

**实现内容**：
1. **Dockerfile**
   - 多阶段构建优化
   - 安全最佳实践
   - 环境变量管理
   - 健康检查配置

2. **docker-compose.yml**
   - 应用服务配置
   - MongoDB 服务配置
   - Nginx 反向代理
   - 网络和卷管理
   - 环境变量文件

3. **配置文件**
   - Nginx 配置
   - .env.example
   - 忽略文件 (.dockerignore)

4. **部署脚本**
   - 构建脚本
   - 启动/停止脚本
   - 健康检查脚本

**最佳实践**：
- 最小化镜像大小
- 安全扫描
- 日志管理
- 资源限制

**输出要求**：
- 完整的 Dockerfile
- docker-compose.yml
- 所有配置文件
- 部署文档
- 使用说明

**请包含**：
- 代码实现
- 构建和运行命令
- 故障排除指南
```

---

## 示例 5: API 设计 - RESTful 接口

### 场景
用户需要设计一个博客系统的 API。

### 用户输入
```
"design a blog API"
```

### Claude 提取的上下文
```json
{
  "task": "design RESTful API for blog system",
  "tech_stack": ["Node.js", "Express", "MongoDB"],
  "domain": "web_development",
  "history_summary": "User needs a complete blog system with posts, comments, and user management"
}
```

### 优化结果
```
作为后端架构师，请设计一个完整的博客系统 RESTful API：

**技术栈**: Node.js, Express, MongoDB

**领域要求**: 遵循 RESTful 最佳实践，确保代码可维护和可扩展

## API 端点设计

### 用户管理
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/users/:id` - 获取用户信息
- `PUT /api/users/:id` - 更新用户信息

### 文章管理
- `GET /api/posts` - 获取文章列表（支持分页、筛选、排序）
- `GET /api/posts/:id` - 获取文章详情
- `POST /api/posts` - 创建文章（需认证）
- `PUT /api/posts/:id` - 更新文章（需认证，仅作者）
- `DELETE /api/posts/:id` - 删除文章（需认证，仅作者）

### 评论管理
- `GET /api/posts/:postId/comments` - 获取文章评论
- `POST /api/posts/:postId/comments` - 添加评论（需认证）
- `PUT /api/comments/:id` - 更新评论（需认证，仅作者）
- `DELETE /api/comments/:id` - 删除评论（需认证，仅作者）

### 标签管理
- `GET /api/tags` - 获取所有标签
- `GET /api/tags/:id` - 获取标签详情
- `POST /api/tags` - 创建标签（需认证）

**数据模型要求**：
- User: id, username, email, passwordHash, role, createdAt
- Post: id, title, content, author, tags, status, createdAt, updatedAt
- Comment: id, post, author, content, createdAt
- Tag: id, name, slug, createdAt

**API 规范**：
- 使用合适的 HTTP 方法（GET/POST/PUT/DELETE）
- 统一的响应格式
- 错误处理和状态码
- 分页支持（page, limit）
- 排序和筛选参数
- API 版本控制

**安全要求**：
- JWT 认证
- 密码哈希（bcrypt）
- 输入验证和清理
- SQL/NoSQL 注入防护
- CORS 配置

**输出要求**：
- API 端点完整列表
- 请求/响应示例（JSON 格式）
- 数据模型定义
- 错误处理规范
- 认证流程说明

**请包含**：
- OpenAPI/Swagger 文档
- 代码示例（Express 路由）
- 测试用例示例
```

---

## 示例 6: 代码审查 - 安全检查

### 场景
用户请求代码安全审查。

### 用户输入
```
"review this code for security issues"
```

### Claude 提取的上下文
```json
{
  "task": "perform security code review",
  "tech_stack": ["Python", "Django"],
  "domain": "security",
  "history_summary": "User wants to ensure their Django application follows security best practices"
}
```

### 优化结果
```
作为安全专家，请对这段 Django 代码进行全面的安全审查：

**技术栈**: Python, Django

**领域要求**: 遵循安全最佳实践，考虑常见漏洞防护

## 审查检查清单

### 1. 注入漏洞
- [ ] SQL 注入（使用 ORM 参数化查询）
- [ ] 命令注入（避免 subprocess/shell=True）
- [ ] 模板注入（自动转义）

### 2. 认证和授权
- [ ] 密码存储（使用 Django 的 make_password）
- [ ] 会话管理（安全配置）
- [ ] CSRF 保护（{% csrf_token %}）
- [ ] 权限检查（@login_required, @permission_required）

### 3. 数据验证
- [ ] 表单验证（Django Forms/ModelForms）
- [ ] 输入长度限制
- [ ] 文件上传验证（类型、大小）

### 4. 敏感数据处理
- [ ] 密码不在日志中
- [ ] API 密钥使用环境变量
- [ ] 错误消息不泄露敏感信息

### 5. HTTPS 和传输安全
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] HSTS 配置

### 6. 依赖项安全
- [ ] 更新到最新稳定版本
- [ ] 使用 pip audit 或 safety

### 7. 配置安全
- [ ] DEBUG = False（生产环境）
- [ ] ALLOWED_HOSTS 配置
- [ ] 自定义错误页面

**输出格式**：
- 发现的问题列表（按严重程度排序）
- 每个问题的详细说明
- 修复建议和代码示例
- 优先级建议（高/中/低）
- 预防措施清单

**请包含**：
- 安全漏洞描述
- 攻击场景说明
- 修复代码示例
- 最佳实践建议
```

---

## 示例 7: 移动开发 - React Native 功能

### 场景
用户需要为 React Native 应用添加功能。

### 用户输入
```
"add push notifications to my app"
```

### Claude 提取的上下文
```json
{
  "task": "implement push notifications in React Native app",
  "tech_stack": ["React Native", "Firebase", "TypeScript"],
  "domain": "mobile_development",
  "history_summary": "User has a React Native app and wants to add push notification capability"
}
```

### 优化结果
```
作为移动应用开发工程师，请在 React Native 应用中实现推送通知功能：

**技术栈**: React Native, Firebase Cloud Messaging (FCM), TypeScript

**实现要求**：
1. **项目配置**
   - 安装必要的依赖（@react-native-firebase/app, @react-native-firebase/messaging）
   - iOS 配置（APNs 证书, Firebase 配置文件）
   - Android 配置（google-services.json）

2. **权限处理**
   - 请求通知权限（iOS 和 Android）
   - 处理权限拒绝情况
   - 权限状态管理

3. **Token 管理**
   - 获取 FCM token
   - Token 刷新处理
   - 发送 token 到后端服务器

4. **通知处理**
   - 前台通知处理
   - 后台通知处理
   - 通知点击事件
   - 数据消息处理

5. **主题订阅**
   - 订阅特定主题
   - 取消订阅
   - 主题管理

6. **后端集成**
   - 发送通知的 API 设计
   - 目标用户选择
   - 通知调度

**TypeScript 类型定义**：
- Notification 类型
- Permission 状态类型
- Token 管理接口

**输出要求**：
- 完整的代码实现（TypeScript）
- iOS 和 Android 配置说明
- 权限处理代码
- 通知处理逻辑
- 后端 API 示例
- 测试代码

**请包含**：
- 代码实现
- 配置步骤
- 错误处理
- 最佳实践
- 测试方法
```

---

## 对比表格

| 场景 | 原始提示词长度 | Minimal | Moderate | Aggressive |
|-----|-------------|---------|----------|------------|
| Web 开发 | 8 词 | ~40 词 | ~90 词 | ~200 词 |
| 数据科学 | 5 词 | ~35 词 | ~100 词 | ~180 词 |
| 机器学习 | 4 词 | ~30 词 | ~110 词 | ~200 词 |
| DevOps | 6 词 | ~30 词 | ~90 词 | ~170 词 |
| API 设计 | 4 词 | ~25 词 | ~130 词 | ~220 词 |

**建议**：
- 简单任务：使用 `minimal` 或 `moderate`
- 复杂任务：使用 `moderate`
- 详细需求：使用 `aggressive`

---

## 技巧提示

### 1. 提供更详细的上下文
上下文越详细，优化效果越好：

```json
// 上下文较少
{
  "tech_stack": ["Python"]
}

// 上下文详细
{
  "tech_stack": ["Python", "FastAPI", "Pydantic", "SQLAlchemy"],
  "domain": "web_development",
  "project_type": "RESTful API",
  "specific_requirements": ["async/await", "dependency injection"]
}
```

### 2. 明确优化目标
在提示词中说明优化目标：

```
"帮我写个登录功能，优化" // 一般优化
"帮我写个登录功能，优化，重点在安全性" // 安全重点
"帮我写个登录功能，优化，要简洁明了" // 简洁重点
```

### 3. 渐进式优化
先使用 minimal，然后逐步增加：

```bash
# 第一步：minimal
python scripts/optimize.py optimize --mode minimal ...

# 如果不够，第二步：moderate
python scripts/optimize.py optimize --mode moderate ...

# 如果还不够，第三步：aggressive
python scripts/optimize.py optimize --mode aggressive ...
```

### 4. 自定义策略组合
根据任务特点选择合适的策略：

```bash
# 代码实现任务
--strategies "clarity,context,examples"

# 概念解释任务
--strategies "clarity,examples"

# 简洁重写任务
--strategies "clarity,conciseness"
```
