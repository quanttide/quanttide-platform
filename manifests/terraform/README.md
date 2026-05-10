# Terraform — 系统基础设施

Terraform 负责生成各组件的本地配置，通过 Vault 注入敏感信息。

```bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=your-root-token
terraform init
terraform apply -var="home=$HOME"
```

## Vault

生成 `~/.vault-data/config/vault.hcl`，用户自行启动：

```bash
vault server -config=~/.vault-data/config/vault.hcl
# 另开终端
vault operator unseal  # 输入 3 个 unseal key 中的任意一个
export VAULT_TOKEN=your-root-token
```

terraform 会确保 KV v2 secrets engine 已挂载到 `secret/`。

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

terraform 将密钥写入 Vault（`secret/stack-auth/`），生成 `~/.stack-auth/start.sh` 启动包装脚本。

```bash
terraform apply -var="home=$HOME"
# 密钥写入 Vault，生成 start.sh

# 启动 Stack Auth（Vault 注入环境变量）
~/.stack-auth/start.sh pnpm dev
```

### 变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `stack_server_secret` | 自动生成 | 服务端签名密钥（写入 Vault） |
| `stack_vault_mount` | `secret` | Vault KV 引擎挂载路径 |
| `stack_db_user` | `postgres` | 数据库用户 |
| `stack_db_password` | 自动生成 | 数据库密码（写入 Vault） |
| `stack_db_name` | `stackframe` | 数据库名 |
| `stack_db_port` | `8128` | 数据库端口 |
