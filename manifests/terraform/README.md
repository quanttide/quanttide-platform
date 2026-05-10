# Terraform — 系统基础设施

```bash
terraform init
terraform apply -var="home=$HOME"
```

## Vault

生成 `~/.vault-data/config/vault.hcl`。

### 变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `home` | **(必填)** | 用户家目录绝对路径 |
| `bind_ip` | `127.0.0.1` | 监听 IP |
| `container_port` | `8200` | 监听端口 |
| `tls_disable` | `true` | 关闭 TLS |
| `data_dir` | `null`（派生自 home） | 存储数据目录 |
| `logs_dir` | `null`（派生自 home） | 审计日志目录 |

## Stack Auth

生成 `~/.stack-auth/` 下的 Postgres 数据库配置和环境变量。

Stack Auth 以 SDK 形式嵌入 qtcloud-auth 应用进程，不独立部署服务。Terraform 只管理 Postgres 数据库和配置注入。

```bash
# 先到 https://app.stack-auth.com 创建项目，获取 project_id / client_key / secret_key
terraform apply -var="home=$HOME" \
  -var="stack_project_id=your-project-id" \
  -var="stack_client_key=your-client-key" \
  -var="stack_secret_key=your-secret-key"

# 启动数据库
docker compose -f ~/.stack-auth/docker-compose.yml up -d
```

### 变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `stack_project_id` | **是** | Stack Auth 项目 ID |
| `stack_client_key` | **是** | Stack Auth 客户端密钥 |
| `stack_secret_key` | **是** | Stack Auth 服务端密钥 |
| `stack_db_user` | `stack` | 数据库用户 |
| `stack_db_password` | 自动生成 | 数据库密码 |
| `stack_db_name` | `stack` | 数据库名 |
| `stack_db_port` | `5433` | 数据库映射端口 |
