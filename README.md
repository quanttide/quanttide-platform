# 量潮工作平台

## 仓库结构

```
quanttide-platform/
├── apps/              → 产品/应用（子模块）
├── packages/          → 跨应用 SDK/工具包（子模块）
├── manifests/         → 系统声明配置
└── docs/              → 文档
```

→ [产品边界说明](docs/index.md)

版本策略、设计原则见 [quanttide-profile-of-product-development](https://github.com/quanttide/quanttide-profile-of-product-development) 仓库的 `products/default/prd/index.md`，目录结构与 packages/apps 约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 产品清单

| 产品 | 定位 | 版本 |
|------|------|------|
| qtadmin | 管理后台 | studio/v0.2.0-alpha.1 |
| qtclass | 课堂服务 | site/v0.1.1 |
| qtcloud | 产品线主仓库 | studio/v0.1.0-alpha.1 |
| qtcloud-agent | 智能体云 | site/v0.1.0 |
| qtcloud-asset | 数字资产管理 | cli/v0.1.0-alpha.2 |
| qtcloud-audit | 审计云 | — |
| qtcloud-auth | 身份云 | provider/v0.1.0-alpha.18 |
| qtcloud-business | 报价与合同管理 | studio/v0.1.0-alpha.2 |
| qtcloud-code | 编程云 | cli/v0.2.1 |
| qtcloud-connect | 智能体协作 | cli/v0.0.1 |
| qtcloud-course | 课程云 | provider/v0.1.3 |
| qtcloud-data | 数据云 | cli/v0.3.0 |
| qtcloud-delib | 议事云 | provider/v0.1.3 |
| qtcloud-devops | DevOps 基础设施 | cli/v0.11.0 |
| qtcloud-econ | 经济云 | studio/v0.1.0-beta.5 |
| qtcloud-finance | 财务云 | provider/v0.1.0 |
| qtcloud-growth | 增长云 | — |
| qtcloud-health | 心理健康 | studio/v0.1.0-alpha.1 |
| qtcloud-human | 人力资源云 | provider/v0.1.0 |
| qtcloud-infra | 基础设施云 | — |
| qtcloud-knowl | 知识云 | cli/v0.2.2 |
| qtcloud-media | 媒体云 | — |
| qtcloud-org | 组织云 | studio/v0.1.0-alpha.2 |
| qtcloud-pay | 支付云 | provider/v0.1.0-alpha.8 |
| qtcloud-product | 产品云 | studio/v0.1.0-beta.3 |
| qtcloud-project | 项目管理云 | studio/v0.1.0-alpha.2 |
| qtcloud-read | 阅读 | — |
| qtcloud-sales | 获客与客户管理 | — |
| qtcloud-support | 示例文档 | — |
| qtcloud-think | 知识收集 | cli/v0.1.0-alpha.1 |
| qtcloud-write | 写作辅助 | studio/v0.1.0-alpha.5 |
| qtconsult | 咨询 | studio/v0.3.0 |
| qtcrowd | 众包销售 | site/v0.1.1-beta.5 |
| qtdata | 数据服务 | studio/v0.1.0-beta.4 |
| qtfiction | 小说平台 | site/v0.1.0-alpha.2 |
| qtfounder | 创始人项目（创作现场） | site/v0.1.0-beta.2 |
| qtmedia | 媒体中心 | site/v0.1.7 |
| qtrecurit | 招聘 | site/v0.1.0-beta.4 |
| qtweb | 官网 | v0.1.0-alpha.1 |

> 版本列为该仓库最近创建的 git tag（scope 前缀如 `cli/`、`studio/`、`provider/`、`site/`），`—` 表示尚无 tag。

## 系统声明

`manifests/` 声明系统级共享资源，与 `apps/` 中的应用模块一一对应但职责分离。

```
manifests/
└── terraform/         → Terraform 配置（OpenTofu 兼容）
    └── templates/     → 配置文件模板
└── kubernetes/        → 集群部署清单（预留）
    ├── overlays/      → 环境差异覆盖
    └── base/          → 基准配置
└── docker/            → 本地开发编排（预留）
```

- 每类工具一层（`terraform/`、`kubernetes/`、`docker/`），不跨层混合
- 多环境差异用变量文件区分，不复制目录
