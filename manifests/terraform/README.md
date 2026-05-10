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

生成 `~/.stack-auth/` 下的 docker-compose 和环境配置。

Stack Auth 是完整产品，可独立部署。镜像需要从源码构建（官方不发布预构建镜像）。

### 快速开始

```bash
# 1. 克隆 Stack Auth 源码并构建镜像
git clone https://github.com/hexclave/stack-auth.git
cd stack-auth
docker build -f docker/server/Dockerfile -t stack-auth-server .

# 2. 生成配置（自动生成密钥和数据库密码）
terraform apply -var="home=$HOME"

# 3. 启动
docker compose -f ~/.stack-auth/docker-compose.yml up -d

# 4. 访问
# Dashboard: http://localhost:8101
# API:       http://localhost:8102
```

### 使用预构建镜像

```bash
terraform apply -var="home=$HOME" \
  -var="stack_server_image=ghcr.io/your-org/stack-auth:v1.0.0"
```

### 变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `stack_server_image` | `stack-auth-server:latest` | Docker 镜像（默认本地构建） |
| `stack_server_secret` | 自动生成 | 服务端签名密钥 |
| `stack_db_user` | `postgres` | 数据库用户 |
| `stack_db_password` | 自动生成 | 数据库密码 |
| `stack_db_name` | `stackframe` | 数据库名 |
| `stack_db_port` | `8128` | 数据库映射端口 |
