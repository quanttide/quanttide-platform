# AGENTS.md - quanttide-platform

Skills provide specialized instructions and workflows for specific tasks.
Use the skill tool to load a skill when a task matches its description.

## SKILL 快速索引

| Skill | 用途 |
|-------|------|
| devops-commit | 规范提交 |
| devops-release | 发布 Release |
| devops-review | 流程审查 |
| docs-deploy | MyST 文档站构建与 GitHub Pages 部署 |

## 文档地图

| 文档 | 认知角色 | 内容概要 |
|------|----------|----------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | 程序记忆 | 设计原则、版本策略、检查清单 |
| [README.md](README.md) | 陈述记忆 | 项目定位、仓库结构、产品清单 |
| [ROADMAP.md](ROADMAP.md) | 方向 | 当前阶段目标、待办事项、优先级 |
| [CHANGELOG.md](CHANGELOG.md) | 记忆 | 版本变更历史、发布记录 |
| [docs/index.md](docs/index.md) | 架构 | 仓库层级关系、边界文档索引 |

## 工作原则

详见 [CONTRIBUTING.md](CONTRIBUTING.md) 完整阐述，此处为 AI 执行摘要：

### 分层即分工
- 主仓库只做范式（原则、规范、技能），不持有子仓库的具体工作项
- 子仓库做产品，主仓库做编排
- 测试分层：单元测试 `src/*/tests/` → 集成测试 `tests/` → 系统测试 `主仓库 tests/`

### 目录即语义
- 目录名映射实际代码结构，不使用抽象概念（如"领域层"）
- 有实体就建目录，没有就不建，不保留空占位符

### 先确认后执行
- 替换 vs 并存：修改前确认旧内容怎么处理
- 改内容 vs 改名字：操作前明确目标是文件还是目录
- 列出操作清单，标注风险等级，等待确认

### 减法优先
- 删除无效内容的优先级高于新增
- 宁可空着也不放不确定的东西

## 子模块

各子模块有自己的 AGENTS.md，开发前查阅具体模块。
