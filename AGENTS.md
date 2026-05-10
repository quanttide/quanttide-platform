# AGENTS.md - quanttide-platform

Skills provide specialized instructions and workflows for specific tasks.
Use the skill tool to load a skill when a task matches its description.

## SKILL 快速索引

| Skill | 用途 | 约束 |
|-------|------|------|
| devops-commit | 规范提交 | 先 `git status` 再 `git diff`，确认无误后提交 |
| devops-release | 发布 Release | **必须逐行执行**，跳过预检查则禁止发布 |
| devops-review | 流程审查 | — |
| docs-deploy | MyST 文档站构建与 GitHub Pages 部署 | — |

### 执行规则

调用 Skill 后，必须按 SKILL.md 中的工作流**从头到尾逐条执行**。标有"必须执行，不可跳过"的步骤不得省略。AI 视为在逐一执行命令，而非阅读参考。若无法完成某一步（如工具不可用），必须向用户说明并等待指示，不可自行跳过。

## 文档地图

| 文档 | 认知角色 | 内容概要 |
|------|----------|----------|
| [docs/prd/index.md](docs/prd/index.md) | 程序记忆 | 设计原则、版本策略 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 程序记忆 | 目录结构、apps/packages 约定 |
| [README.md](README.md) | 陈述记忆 | 项目定位、仓库结构、产品清单 |
| [ROADMAP.md](ROADMAP.md) | 方向 | 当前阶段目标、待办事项、优先级 |
| [CHANGELOG.md](CHANGELOG.md) | 记忆 | 版本变更历史、发布记录 |
| [docs/index.md](docs/index.md) | 架构 | 仓库层级关系、文档类型（add/dev/brd/prd） |

## AI 执行指引

开始工作前，先阅读 [docs/prd/index.md](docs/prd/index.md) 的设计原则与 [CONTRIBUTING.md](CONTRIBUTING.md) 的项目约定。

过往经验表明 AI 最容易在这些地方犯错，请特别注意：

- **替换 vs 并存**：修改内容前先确认旧内容怎么处理，不要默认替换
- **改内容 vs 改名字**：操作前明确目标是文件/目录的内容还是名称
- **子仓库 vs 主仓库**：不要在子仓库里做主仓库的事（如改其 ROADMAP），也不要反过来
- **减法优先**：删除无效内容的优先级高于新增，宁可空着不放不确定的东西
- **目录即语义**：目录名使用代码实际结构，不用抽象概念。有实体才建目录，但预留目录也是有效的架构声明——不要擅自移除用户放置的空目录和占位文件
- **提交即推送**：提交后默认推送到远端（主仓库和子模块都推），除非用户明确说"只提交不推"

### Vault 密钥命名风格

**不要**让 Vault key 名 = Python 字段名。它们是不同层的命名：

| 层级 | 命名原则 | 例子 |
|------|---------|------|
| Vault 路径 | 标识提供商/范围 | `secret/deepseek` |
| Vault key | 简短自描述，路径已做区隔 | `api_key`、`base_url` |
| Python 字段 | 遵循应用自有命名 | `llm_api_key` |

Vault key 只需在路径范围内自描述即可，不要跟应用字段名强行一致。

### 特殊文档提醒

完成重要变更后，检查是否需要同步更新以下文档：

| 文档 | 触发条件 |
|------|---------|
| [CHANGELOG.md](CHANGELOG.md) | 对用户可见的变更（新功能、重构、修复） |
| [ROADMAP.md](ROADMAP.md) | 方向调整、阶段性成果达成 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 目录结构或 packages/apps 约定变化 |
| [docs/prd/index.md](docs/prd/index.md) | 工作方式或原则发生变化 |
| [README.md](README.md) | 产品功能或仓库结构变化 |
| [AGENTS.md](AGENTS.md) | AI 工作经验增加 |

AI 应在完成工作后主动提醒用户是否需要更新这些文档，而非等用户提出。

## 子模块

各子模块有自己的 AGENTS.md，开发前查阅具体模块。
