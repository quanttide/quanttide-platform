# Terraform — 系统基础设施

Terraform 负责生成各组件的本地配置，用户自行选择运行方式。

```bash
terraform init
terraform apply -var="home=$HOME"
```

## Vault

生成 `~/.vault-data/config/vault.hcl`，用户自行启动 `vault server -config=~/.vault-data/config/vault.hcl`。

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

生成 `~/.stack-auth/.env`，用户自行选择运行方式（直接 `pnpm dev` 或 Docker）。

### 变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `stack_server_secret` | 自动生成 | 服务端签名密钥 |
| `stack_db_user` | `postgres` | 数据库用户 |
| `stack_db_password` | 自动生成 | 数据库密码 |
| `stack_db_name` | `stackframe` | 数据库名 |
| `stack_db_port` | `8128` | 数据库端口 |
