# manifests

系统声明式配置，与 `apps/` 中的应用模块职责分离。

## 目录职责

| 目录 | 角色 | 说明 |
|------|------|------|
| `terraform/` | **组装层** | 声明式描述系统各组件的配置和依赖关系，输出可部署的配置产物。支持 `local_file`（本地）和云资源（未来）两种后端 |
| `docker/` | **产物层（预留）** | 可直接运行的 Docker Compose 编排文件。与 `terraform/templates/` 中的 compose 模板互补——模板需经 terraform 注入后输出至此，纯静态 compose 可直接放入 |
| `kubernetes/` | **产物层（预留）** | 可直接应用的 Kubernetes 清单 |

## 边界原则

- **terraform 不限于云资源**：它也可以生成本地配置文件（如 Vault HCL、docker-compose、`.env`），组装层的职责是"把组件组合为可部署状态"，不设后端限制
- **模板归组装，产物归对应目录**：terraform 里的模板不因输出格式而改变归属——输出 docker-compose 不意味着它属于 `docker/`
- **目录即声明**：`docker/` 和 `kubernetes/` 有 `.gitkeep` 即有效声明，定义将来内容的边界
