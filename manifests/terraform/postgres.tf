# ================================================================
# 部署层（本地环境）
# PostgreSQL 安装与配置。
# 上云时整块替换为云 RDS 数据源。
# ================================================================

resource "local_file" "setup_postgres" {
  filename = "${var.home}/.local/bin/setup-postgres.sh"
  content = templatefile("${path.module}/templates/setup-postgres.sh.tftpl", {
    pg_user     = local.db_user
    pg_password = local.db_password
    pg_db       = local.db_name
    pg_port     = local.db_port
  })
}
