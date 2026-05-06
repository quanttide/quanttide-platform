# CHANGELOG

## [0.4.1] - 2026-05-06

### Added
- apps/qtconsult — 量潮咨询子模块，含 .gitignore、业务数据目录 data/、README

### Changed
- apps/qtadmin 更新至 v0.0.3（含 studio/v0.0.2）
- apps/qtcloud-write、qtcloud-product、qtcloud-infra 子模块更新

### Docs
- docs-deploy skill 新增 pages-before-push 顺序约束与部署经验记录

## [0.4.0] - 2026-05-04

仓库结构定型为 apps/manifests/docs 三级，确立开发者视角的声明式配置目录哲学。

### Added
- manifests/ 目录骨架（terraform/kubernetes/docker）
- manifests/terraform/vault.tf — Vault 本地部署配置模板

### Changed
- README 重构为 apps/manifests/docs 三级结构，标注 Google 单仓规范
- `infra/` → `manifests/` 重命名（开发者视角，声明式而非运维式）

### Chore
- 更新 qtcloud-write 子模块（config 重构为 env-based，移除 Vault 依赖）

## [0.3.2] - 2026-05-04

Skill 约束强化与 qtcloud-write 子模块功能交付。

### Added
- devops-release SKILL 硬约束：不执行预检查禁止发布
- AGENTS.md 执行规则：调用 Skill 必须逐条执行 SKILL.md 工作流
- qtcloud-write: Provider API（文章叙事分析 + 风格对比）
- qtcloud-write: Studio Flutter Web 客户端（全平台支持）
- qtcloud-write: 端到端集成测试（真实 Provider + Flutter 客户端）
- qtcloud-write: scripts/run-tests.sh 测试脚本
- qtcloud-write: 子模块独立 CHANGELOG（provider/、studio/）

### Changed
- devops-release SKILL 重写 description，强调必须先写 CHANGELOG 再打 tag

### Chore
- 同步 qtcloud-write 子模块（v0.1.0-alpha.1 发布：provider + studio）

## [0.3.1] - 2026-04-30

ADD 文档整合与厂商解绑。

### Added
- 新增 docs-deploy SKILL（MyST + GitHub Pages 部署经验）
- 新增 docs/add/CONTRIBUTING.md（ADD 工作经验总结）
- 新增主仓库 MyST 文档站及 GitHub Pages 部署

### Changed
- ADD 文档整合：cloud_services → infra，applications → layers/apps → apps，topics+general → intro，languages_and_frameworks → packages
- 移除所有占位符和空文档
- 基础设施文档彻底解绑腾讯云，MySQL 替换为 PostgreSQL
- CONTRIBUTING.md 精简，去除干扰性产品示例
- ROADMAP.md 重写为三个范式方向

### Chore
- 同步 qtcloud-data 子模块（接收 ADD 文档）
- 同步 qtadmin 子模块

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