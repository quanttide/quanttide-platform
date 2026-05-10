# ================================================================
# 部署层
# 本地：PostgreSQL 手工安装，Terraform 通过 TCP 管理数据库
# 云上：整块替换为 aws_db_instance / tencentcloud_db_instance
# ================================================================

locals {
  db_user              = var.stack_db_user != null ? var.stack_db_user : "postgres"
  db_password          = var.stack_db_password != null ? var.stack_db_password : random_password.stack_db.result
  db_name              = var.stack_db_name != null ? var.stack_db_name : "stackframe"
  db_port              = var.stack_db_port != null ? var.stack_db_port : 5432
  db_connection_string = "postgres://${local.db_user}:${local.db_password}@127.0.0.1:${local.db_port}/${local.db_name}"
}

resource "random_password" "stack_db" {
  length  = 16
  special = false
}

# 引导脚本（仅首次安装 PG 后执行一次需 sudo）
resource "local_file" "bootstrap_postgres" {
  filename = "${var.home}/.local/bin/bootstrap-postgres.sh"
  content = templatefile("${path.module}/templates/bootstrap-postgres.sh.tftpl", {
    user     = local.db_user
    password = local.db_password
    db       = local.db_name
  })
}

# 新应用加库（走 TCP，无需 sudo）
resource "null_resource" "postgres_bootstrap" {
  triggers = {
    password = local.db_password
    user     = local.db_user
  }

  provisioner "local-exec" {
    command = <<-EOT
      PGPASSWORD='${local.db_password}' psql -h 127.0.0.1 -p ${local.db_port} -U ${local.db_user} -c "SELECT 1 FROM pg_database WHERE datname='${local.db_name}'" 2>/dev/null | grep -q 1 || \
        PGPASSWORD='${local.db_password}' psql -h 127.0.0.1 -p ${local.db_port} -U ${local.db_user} -c "CREATE DATABASE ${local.db_name} OWNER ${local.db_user};"
    EOT
  }
}

# PG 凭据备份
resource "local_file" "postgres_backup" {
  count    = var.backup_dir != null ? 1 : 0
  filename = "${var.backup_dir}/postgres-creds.json"
  content = jsonencode({
    user     = local.db_user
    password = local.db_password
    db       = local.db_name
    port     = local.db_port
  })
}

# 连通性验证（每次 apply 检查）
resource "null_resource" "postgres_verify" {
  triggers = {
    conn_string = local.db_connection_string
  }

  provisioner "local-exec" {
    command = <<-EOT
      PGPASSWORD='${local.db_password}' psql -h 127.0.0.1 -p ${local.db_port} -U ${local.db_user} -d ${local.db_name} -c 'SELECT 1;' >/dev/null 2>&1 || \
        echo "WARN: PG 不可达 — 执行 sudo bash ${var.home}/.local/bin/bootstrap-postgres.sh"
    EOT
  }
}
