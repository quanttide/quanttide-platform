# CHANGELOG

## [0.3.0] - 2026-04-30

逆向文档化与 MyST 文档站点。

### Added
- 新增逆向文档化流程：代码 → ADD → PRD → BRD
- 新增 qtcloud-hr Salary/Recruitment 完整 BRD→PRD→ADD 文档链
- 新增 qtcloud-hr/qtcloud-asset MyST 文档站配置及 GitHub Pages CI/CD
- 新增 qtcloud-hr AGENTS.md、CONTRIBUTING.md（含经验记录）
- 新增 qtcloud-asset docs/index.md 产品简介
- 新增 CHANGELOG.md Release 格式规范

### Changed
- qtcloud-hr Salary 模块：剥离 FastAPI/ORM/DB 依赖，只留纯领域逻辑
- qtcloud-hr CONTRIBUTING.md 与 README.md 按认知角色重组
- qtcloud-asset scripts → run-cli 目录重命名，README.cli 迁入 src/cli/

### Chore
- 同步 qtcloud-hr 子模块（文档体系建立）
- 同步 qtcloud-asset 子模块（目录重构 + 文档站）
- 同步 qtadmin 子模块（清理遗留代码）

## [0.2.2] - 2026-04-30

文档架构重构与领域归位。

### Added
- 新增 CONTRIBUTING.md 领域归位原则及检查清单
- 新增 AGENTS.md 文档地图（文档认知角色索引）

### Changed
- AGENTS.md 仅保留元认知信息（技能索引、文档地图、子模块指引）
- CONTRIBUTING.md 补充项目约定（版本与发布）
- README.md 作为陈述记忆（仓库结构、产品清单）
- ROADMAP.md 去重，产品清单引用 README.md

### Chore
- 同步 qtadmin 子模块（迁出 asset_contract 到 qtcloud-asset）
- 同步 qtcloud-asset 子模块（接收 asset_contract 模块）

## [0.2.1] - 2026-04-29

子模块与示例文件更新。

### Added
- 新增 qtcloud-devops examples/default/code.md
- 新增 qtdata examples/default/ 目录（asset/cli/data/project 示例）

### Removed
- 移除 qtadmin 过时的 docs/add、docs/prd、docs/user 文件

### Chore
- 同步 qtadmin 子模块（清理过时文档）
- 同步 qtcloud-devops 子模块（新增示例）
- 同步 qtdata 子模块（新增默认示例）

## [0.2.0] - 2026-04-16

仓库层级重构与产品边界定义。

### Added
- 新增 docs/index.md 说明仓库层级关系
- 新增 docs/prd/relations/index.md 说明产品边界
- 新增 CONTRIBUTING.md 产品设计语言
- 新增 qtcloud-sales 子模块（报价与合同管理）
- 新增 qtcloud 产品组合 relations 说明

### Changed
- 精简 AGENTS.md 至核心内容
- 重新定义商务云（报价+合同）与销售云（获客）边界
- qtcloud/docs/prd/ 从 spec 迁移至 add

### Removed
- 删除 docs/prd/qtcloud-write.md（已移至子模块）

### Chore
- 同步 qtcloud-business 子模块
- 同步 qtcloud-sales 子模块
- 同步 qtcloud 子模块

## [0.1.2] - 2026-04-12

数字资产契约体系与 Agent Skills。

### Added
- 新增主仓库数字资产契约 `.quanttide/asset/contract.yaml`
- 新增产品边界契约 `.quanttide/product/contract.yaml`
- 新增 Agent Skills：docs-format、devops-commit、devops-release

### Changed
- 资产契约 operations 改为 skills
- 契约字段 name 统一改为 title
- 产品契约分层：应用层（qtcloud/qtadmin）与领域层（qtcloud-*）

### Chore
- 同步 qtcloud-asset 子模块（新增产品契约、Studio 原型、IaC）
- 同步 qtcloud-agent 子模块（Skill 审查器示例）
- 清理 src 目录，迁移至 apps 子模块架构

## [0.1.1] - 2023-02-09

最小可用版本。

### Features

- 增加云服务选型、语言和框架、应用体系。

## [0.1.0] - 2022-10-23