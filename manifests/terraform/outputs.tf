output "stack_auth_dir" {
  description = "Stack Auth 配置文件目录"
  value       = local.stack_auth_dir
}

output "stack_db_password" {
  description = "Stack Auth 数据库密码"
  value       = local.db_password
  sensitive   = true
}

output "stack_db_connection" {
  description = "Stack Auth 数据库连接串（不含密码）"
  value       = "postgres://${local.db_user}:****@127.0.0.1:${local.db_port}/${local.db_name}"
}
