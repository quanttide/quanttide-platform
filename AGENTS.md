# AGENTS.md - quanttide-platform

## SKILL 快速索引

| Skill | 用途 |
|-------|------|
| devops-commit | 规范提交 |
| devops-release | 发布 Release |
| devops-review | 流程审查 |

## 仓库结构

```
quanttide-platform/
├── apps/qtcloud/     → 产品线主仓库
├── apps/qtadmin/     → 管理后台
├── apps/qtcloud-*    → 独立产品
└── docs/             → 架构文档
```

→ [产品边界说明](docs/index.md)

## 版本与发布

- **SemVer**: `v{major}.{minor}.{patch}`
- **Phase**: Exploration (0.0.x) → Validation (0.x.y) → Release (x.y.z)
- **Changelog**: Keep a Changelog 格式
- **Commits**: Conventional Commits

## 子模块

各子模块有自己的 AGENTS.md，开发前查阅具体模块。