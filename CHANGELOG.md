# CHANGELOG

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

初始版本。
