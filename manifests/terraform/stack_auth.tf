locals {
  stack_auth_dir       = "${var.home}/.stack-auth"
  db_user              = var.stack_db_user != null ? var.stack_db_user : "postgres"
  db_password          = var.stack_db_password != null ? var.stack_db_password : random_password.stack_db.result
  db_name              = var.stack_db_name != null ? var.stack_db_name : "stackframe"
  db_port              = var.stack_db_port != null ? var.stack_db_port : 8128
  api_port             = var.stack_api_port != null ? var.stack_api_port : 8102
  dashboard_port       = var.stack_dashboard_port != null ? var.stack_dashboard_port : 8101
  server_secret        = var.stack_server_secret != null ? var.stack_server_secret : random_password.stack_secret.result
  db_connection_string = "postgres://${local.db_user}:${local.db_password}@127.0.0.1:${local.db_port}/${local.db_name}"
  vault_mount          = var.stack_vault_mount != null ? var.stack_vault_mount : "secret"
}

resource "random_password" "stack_db" {
  length  = 16
  special = false
}

resource "random_password" "stack_secret" {
  length  = 32
  special = false
}

resource "vault_kv_secret_v2" "stack_auth" {
  depends_on = [vault_mount.kv_secret]
  mount      = local.vault_mount
  name       = "stack-auth"
  data_json = jsonencode({
    STACK_SERVER_SECRET              = local.server_secret
    STACK_DATABASE_CONNECTION_STRING = local.db_connection_string
  })
}

resource "local_file" "stack_auth_start" {
  filename = "${local.stack_auth_dir}/start.sh"
  content = templatefile("${path.module}/templates/stack-auth-start.sh.tftpl", {
    vault_mount    = local.vault_mount
    api_port       = local.api_port
    dashboard_port = local.dashboard_port
  })
}
