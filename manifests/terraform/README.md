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

生成 `~/.stack-auth/` 下的 docker-compose 和环境配置：

```bash
# 自动生成所有密钥
terraform apply -var="home=$HOME"

# 查看生成的密钥（后续 apply 自动从 state 读取，不会重新生成）
terraform output stack_admin_key

# 指定密钥（可复现）
terraform apply -var="home=$HOME" \
  -var="stack_secret_key=xxx" \
  -var="stack_admin_key=xxx" \
  -var="stack_image_tag=0.9.0"

# 启动
docker compose -f ~/.stack-auth/docker-compose.yml up -d
```

### 变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `stack_db_user` | `stack` | 数据库用户 |
| `stack_db_password` | 自动生成 | 数据库密码 |
| `stack_db_name` | `stack` | 数据库名 |
| `stack_db_port` | `5433` | 数据库映射端口 |
| `stack_api_port` | `8100` | API 端口 |
| `stack_dashboard_port` | `8101` | Dashboard 端口 |
| `stack_secret_key` | 自动生成 | 服务端密钥 |
| `stack_admin_key` | 自动生成 | 管理员 API Key |
| `stack_image_tag` | `latest` | Docker 镜像标签（上线后应锁定到具体版本） |

### Outputs

自动生成的密钥通过 `terraform output` 查看：

```bash
terraform output stack_admin_key    # 敏感，显示后需记录
terraform output stack_db_password  # 敏感
terraform output stack_auth_dir     # 配置文件路径
```
