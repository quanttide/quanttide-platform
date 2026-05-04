# 量潮工作平台

## 仓库结构

```
quanttide-platform/
├── apps/              → 应用模块
├── infra/             → 系统级基础设施（Google 单仓规范）
└── docs/              → 文档
```

→ [产品边界说明](docs/index.md)

版本策略、设计原则等项目约定见 [CONTRIBUTING.md](CONTRIBUTING.md#项目约定)。

## 产品清单

| 产品 | 定位 | 状态 |
|------|------|------|
| qtcloud | 产品线主仓库 | 完善中 |
| qtcloud-sales | 获客与客户管理 | 待开发 |
| qtcloud-business | 报价与合同管理 | 待开发 |
| qtcloud-think | 知识收集 | 探索期 |
| qtcloud-write | 写作辅助 | 探索期 |
| qtcloud-health | 心理健康 | 探索期 |
| qtcloud-asset | 数字资产管理 | 探索期 |
| qtcloud-connect | 智能体协作 | 探索期 |
| qtadmin | 管理后台 | 待开发 |
| qtdata | 数据服务 | 待开发 |
| qtclass | 课堂服务 | 待开发 |
| qtcloud-knowl | 知识云 | 探索期 |

## 基础设施

`infra/` 管理系统级共享资源，与 `apps/` 中的应用模块一一对应但职责分离。

```
infra/
└── terraform/         → Terraform 配置（OpenTofu 兼容）
    ├── environments/  → 环境变量文件（dev / staging / prod）
    └── modules/       → 可复用模块
└── kubernetes/        → 集群部署清单
    ├── overlays/      → 环境差异覆盖
    └── base/          → 基准配置
└── docker/            → 本地开发编排（预留）
```

- 每类工具一层（`terraform/`、`kubernetes/`、`docker/`），不跨层混合
- 多环境差异用变量文件区分，不复制目录
