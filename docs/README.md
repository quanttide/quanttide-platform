# 文档说明

## 仓库层级关系

```
quanttide-platform (主仓库)
├── apps/qtcloud      → quanttide/qtcloud (组合所有 qtcloud-*)
├── apps/qtadmin      → quanttide/qtadmin (组合部分子仓库)
├── apps/qtdata      → quanttide/qtdata (组合部分子仓库)
├── apps/qtclass     → quanttide/qtclass (组合部分子仓库)
└── apps/qtcloud-*  → quanttide/qtcloud-* (独立产品)
```

## 文档类型

| 目录 | 角色 |
|------|------|
| `docs/add/` | 架构决策（why、约束、原则） |
| `docs/dev/` | 开发操作指南（how、命令、代码示例） |
| `docs/brd/` | 业务需求 |
| `docs/prd/` | 产品需求 |

## 设计逻辑

### 1. 组合与被组合

- **主仓库**（qtcloud, qtadmin, qtdata, qtclass）：组合多个子仓库
- **子仓库**（qtcloud-*）：独立产品，有自己的 PRD

### 2. 文档层级

- **子仓库**：`docs/prd/` 存放自己的 PRD
- **主仓库**：`docs/prd/relations/` 存放产品边界说明

### 3. 边界文档

每个主仓库需要有 `docs/prd/relations/` 说明：
- 自己组合了哪些子仓库
- 各子仓库的功能边界

→ [qtcloud 产品边界](apps/qtcloud/docs/prd/relations/index.md)