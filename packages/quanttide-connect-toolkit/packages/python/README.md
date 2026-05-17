# quanttide-connect-toolkit (Python)

沟通工程工具包 Python SDK。提供人机沟通的核心数据模型和共识管理能力，供 `apps/` 中的各应用复用。

## 安装

```bash
uv add quanttide-connect-toolkit
```

## 模块

- `quanttide_connect.models` — Message、Consensus、Relation 数据模型
- `quanttide_connect.events` — 领域事件定义
- `quanttide_connect.repository` — 仓储接口（Repository Protocol）
- `quanttide_connect.services` — 应用服务
  - `services.message` — `MessageService`（发送、编辑消息）
  - `services.consensus` — `ConsensusService`（提议、确认、废弃共识）
  - `services.relation` — `RelationService`（关联、解除关联）
