output "stack_auth_dir" {
  description = "Stack Auth 配置文件目录"
  value       = local.stack_auth_dir
}

output "stack_db_password" {
  description = "Stack Auth 数据库密码"
  value       = local.db_password
  sensitive   = true
}

output "stack_server_secret" {
  description = "Stack Auth 服务端签名密钥"
  value       = local.server_secret
  sensitive   = true
}
