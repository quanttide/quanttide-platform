locals {
  stack_auth_dir    = "${var.home}/.stack-auth"
  db_user           = var.stack_db_user != null ? var.stack_db_user : "stack"
  db_password       = var.stack_db_password != null ? var.stack_db_password : random_password.stack_db.result
  db_name           = var.stack_db_name != null ? var.stack_db_name : "stack"
  db_port           = var.stack_db_port != null ? var.stack_db_port : 5433
  api_port          = var.stack_api_port != null ? var.stack_api_port : 8100
  dashboard_port    = var.stack_dashboard_port != null ? var.stack_dashboard_port : 8101
  secret_key        = var.stack_secret_key != null ? var.stack_secret_key : random_password.stack_secret.result
  admin_key         = var.stack_admin_key != null ? var.stack_admin_key : random_password.stack_admin.result
}

resource "random_password" "stack_db" {
  length  = 16
  special = false
}

resource "random_password" "stack_secret" {
  length  = 32
  special = false
}

resource "random_password" "stack_admin" {
  length  = 24
  special = false
}

resource "local_file" "stack_auth_env" {
  filename = "${local.stack_auth_dir}/.env"
  content  = templatefile("${path.module}/templates/stack-auth.env.tftpl", {
    db_user      = local.db_user
    db_password  = local.db_password
    db_name      = local.db_name
    db_port      = local.db_port
    api_port     = local.api_port
    secret_key   = local.secret_key
    admin_key    = local.admin_key
  })
}

resource "local_file" "stack_auth_compose" {
  filename = "${local.stack_auth_dir}/docker-compose.yml"
  content  = templatefile("${path.module}/templates/docker-compose.stack-auth.yml.tftpl", {
    db_port       = local.db_port
    db_user       = local.db_user
    db_password   = local.db_password
    db_name       = local.db_name
    api_port      = local.api_port
    dashboard_port = local.dashboard_port
  })
}
