# ================================================================
# 部署层（本地环境）
# 生成随机密码、启动脚本，并将配置写入 Vault。
# 上云时整块替换为云数据源 + vault_kv_secret_v2。
# ================================================================

locals {
  vault_mount      = var.stack_vault_mount != null ? var.stack_vault_mount : "secret"
  stack_auth_dir   = "${var.home}/.stack-auth"
  api_port         = var.stack_api_port != null ? var.stack_api_port : 8102
  dashboard_port   = var.stack_dashboard_port != null ? var.stack_dashboard_port : 8101
  server_secret    = var.stack_server_secret != null ? var.stack_server_secret : random_password.stack_secret.result
  stack_target_dir = var.stack_target_dir != null ? var.stack_target_dir : "${var.home}/repos/stack-auth"
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

resource "local_file" "stack_auth_backup" {
  count    = var.backup_dir != null ? 1 : 0
  filename = "${var.backup_dir}/stack-auth-secrets.json"
  content = jsonencode({
    STACK_SERVER_SECRET              = local.server_secret
    STACK_DATABASE_CONNECTION_STRING = local.db_connection_string
  })
}

resource "local_file" "clone_stack_auth" {
  filename = "${var.home}/.local/bin/clone-stack-auth.sh"
  content = templatefile("${path.module}/templates/clone-stack-auth.sh.tftpl", {
    repo_url    = var.stack_repo_url
    target_dir  = local.stack_target_dir
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
