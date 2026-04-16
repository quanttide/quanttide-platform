# 量潮应用系统架构文档

量潮应用系统（`qtapps`），是量潮科技旗下软件应用体系的总称。

## 仓库层级

```
quanttide-platform/
├── apps/qtcloud/     → qtcloud (组合所有 qtcloud-*)
├── apps/qtadmin/     → qtadmin
├── apps/qtdata/      → qtdata
├── apps/qtclass/    → qtclass
└── apps/qtcloud-*   → 独立产品
```

→ [仓库层级说明](docs/index.md)

## 产品清单

| 产品 | 定位 | 状态 |
|------|------|------|
| qtcloud | 产品线主仓库 | 完善中 |
| qtcloud-sales | 获客与客户管理 | 待开发 |
| qtcloud-business | 报价与合同管理 | 待开发 |
| qtcloud-think | 思维收集与澄清 | 探索期 |
| qtcloud-write | 写作辅助 | 探索期 |
| qtcloud-health | CBT 工具 | 探索期 |
| qtcloud-asset | 数字资产管理 | 探索期 |
| qtcloud-connect | 智能体协作 | 探索期 |
| qtadmin | 管理后台 | 待开发 |
| qtdata | 数据服务 | 待开发 |
| qtclass | 课堂服务 | 待开发 |

→ [ROADMAP](ROADMAP.md)

## 快速链接

- [产品设计语言](CONTRIBUTING.md)
- [产品边界说明](apps/qtcloud/docs/prd/relations/index.md)
- [CHANGELOG](CHANGELOG.md)