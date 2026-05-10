# Terraform — 系统基础设施

文件按组件划分：

| 文件 | 管理层 | 部署层 |
|------|--------|--------|
| `main.tf` | provider 声明 | — |
| `vault.tf` | `vault_mount.kv_secret` | `local_file.vault_config` |
| `postgres.tf` | — | 密码生成、建库、备份、连通性验证 |
| `stack_auth.tf` | — | 密钥写入 Vault、克隆脚本、启动脚本 |

## 依赖

```
Vault (手动启动, unseal)
    └→ terraform apply
        ├→ vault_mount.kv_secret (KV v2 引擎)
        ├→ random_password.stack_db → vault_kv_secret_v2.stack_auth (密钥入 Vault)
        ├→ random_password.stack_db → postgres_bootstrap (TCP 建库)
        └→ local_file.* (配置脚本)

PostgreSQL (手动安装)
    └→ sudo bootstrap-postgres.sh (设密码, 建库, 一次性)
```

## 首次部署

```bash
# 1. 启动 Vault
vault server -config=~/.vault-data/config/vault.hcl
vault operator unseal

# 2. 手动安装 PostgreSQL
sudo apt-get install -y postgresql postgresql-client
sudo bash ~/.local/bin/bootstrap-postgres.sh

# 3. 运行 Terraform
VAULT_TOKEN=$(cat ~/.vault-token) terraform apply

# 4. 克隆 Stack Auth 并启动
bash ~/.local/bin/clone-stack-auth.sh
cd ~/repos/stack-auth && ~/.stack-auth/start.sh pnpm dev
```

## 变量

| 变量 | 默认 | 说明 |
|------|------|------|
| `home` | **(必填)** | 用户家目录 |
| `backup_dir` | `null` | Nutstore 备份目录 |
| `bind_ip` | `127.0.0.1` | Vault 监听 IP |
| `container_port` | `8200` | Vault 端口 |
| `stack_db_user` | `postgres` | 数据库用户 |
| `stack_db_password` | 自动生成 | 数据库密码（入 Vault） |
| `stack_db_name` | `stackframe` | 数据库名 |
| `stack_db_port` | `5432` | 数据库端口 |
| `stack_api_port` | `8102` | Stack Auth API 端口 |
| `stack_dashboard_port` | `8101` | Dashboard 端口 |
| `stack_target_dir` | `~/repos/stack-auth` | Stack Auth 源码目录 |
| `stack_repo_url` | `https://github.com/stack-auth/stack-auth.git` | 仓库地址 |
