locals {
  stack_auth_dir = "${var.home}/.stack-auth"
  db_user        = var.stack_db_user != null ? var.stack_db_user : "stack"
  db_password    = var.stack_db_password != null ? var.stack_db_password : random_password.stack_db.result
  db_name        = var.stack_db_name != null ? var.stack_db_name : "stack"
  db_port        = var.stack_db_port != null ? var.stack_db_port : 5433
  project_id     = var.stack_project_id
  client_key     = var.stack_client_key
  secret_key     = var.stack_secret_key
}

resource "random_password" "stack_db" {
  length  = 16
  special = false
}

resource "local_file" "stack_auth_env" {
  filename = "${local.stack_auth_dir}/.env"
  content  = templatefile("${path.module}/templates/stack-auth.env.tftpl", {
    project_id  = local.project_id
    client_key  = local.client_key
    secret_key  = local.secret_key
    db_user     = local.db_user
    db_password = local.db_password
    db_name     = local.db_name
    db_port     = local.db_port
  })
}

resource "local_file" "stack_auth_compose" {
  filename = "${local.stack_auth_dir}/docker-compose.yml"
  content  = templatefile("${path.module}/templates/docker-compose.stack-auth.yml.tftpl", {
    db_port     = local.db_port
    db_user     = local.db_user
    db_password = local.db_password
    db_name     = local.db_name
  })
}
