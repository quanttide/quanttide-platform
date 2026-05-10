# 基础设施状态

## Vault

| 操作 | 方式 |
|------|------|
| 启动 + 解封 | 手动 |
| 配置生成 | 自动（Terraform）|
| token 写入 `~/.vault-token` | 手动 |
| 引擎挂载 | 自动（Terraform）|

## PostgreSQL

| 操作 | 方式 |
|------|------|
| 安装 | 手动 |
| 设密码 + 建库 | 引导脚本手动 sudo，之后 Terraform TCP 自动创建 |

## Stack Auth

| 操作 | 方式 |
|------|------|
| 克隆 + 安装依赖 | 脚本手动运行 |
| 密钥注入 Vault | 自动（Terraform）|
| 启动 | 手动 |
