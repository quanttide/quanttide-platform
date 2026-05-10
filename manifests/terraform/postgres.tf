# ================================================================
# 部署层
# 本地：PostgreSQL 手工安装，Terraform 生成引导脚本 + 验证连通性
# 云上：整块替换为 aws_db_instance / tencentcloud_db_instance
# ================================================================

locals {
  db_user     = var.stack_db_user != null ? var.stack_db_user : "postgres"
  db_password = var.stack_db_password != null ? var.stack_db_password : random_password.stack_db.result
  db_name     = var.stack_db_name != null ? var.stack_db_name : "stackframe"
  db_port           = var.stack_db_port != null ? var.stack_db_port : 5432
  db_connection_string = "postgres://${local.db_user}:${local.db_password}@127.0.0.1:${local.db_port}/${local.db_name}"
}

resource "random_password" "stack_db" {
  length  = 16
  special = false
}

# 引导脚本（首次 sudo 执行一次后不再需要）
resource "local_file" "bootstrap_postgres" {
  filename = "${var.home}/.local/bin/bootstrap-postgres.sh"
  content = templatefile("${path.module}/templates/bootstrap-postgres.sh.tftpl", {
    user     = local.db_user
    password = local.db_password
    db       = local.db_name
  })
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
