locals {
  stack_auth_dir = "${var.home}/.stack-auth"
  db_user        = var.stack_db_user != null ? var.stack_db_user : "postgres"
  db_password    = var.stack_db_password != null ? var.stack_db_password : random_password.stack_db.result
  db_name        = var.stack_db_name != null ? var.stack_db_name : "stackframe"
  db_port        = var.stack_db_port != null ? var.stack_db_port : 8128
  api_port       = 8102
  dashboard_port = 8101
  server_secret  = var.stack_server_secret != null ? var.stack_server_secret : random_password.stack_secret.result
  server_image   = var.stack_server_image != null ? var.stack_server_image : "stack-auth-server:latest"
}

resource "random_password" "stack_db" {
  length  = 16
  special = false
}

resource "random_password" "stack_secret" {
  length  = 32
  special = false
}

resource "local_file" "stack_auth_env" {
  filename = "${local.stack_auth_dir}/.env"
  content  = templatefile("${path.module}/templates/stack-auth.env.tftpl", {
    db_user         = local.db_user
    db_password     = local.db_password
    db_name         = local.db_name
    db_port         = local.db_port
    api_port        = local.api_port
    dashboard_port  = local.dashboard_port
    server_secret   = local.server_secret
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
    server_image  = local.server_image
  })
}
