# PostgreSQL

## 初始化

PostgreSQL 不在 Terraform 编排内，需手动安装：

```bash
sudo apt-get install -y postgresql postgresql-client
```

Terraform 生成引导脚本后执行：

```bash
sudo bash ~/.local/bin/bootstrap-postgres.sh
```

脚本密码由 Terraform 注入，存于 Vault。
