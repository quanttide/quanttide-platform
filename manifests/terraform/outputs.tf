output "stack_auth_dir" {
  description = "Stack Auth 配置文件目录"
  value       = local.stack_auth_dir
}

output "stack_db_password" {
  description = "Stack Auth 数据库密码"
  value       = local.db_password
  sensitive   = true
}

output "stack_api_port" {
  description = "Stack Auth API 端口"
  value       = local.api_port
}

output "stack_dashboard_port" {
  description = "Stack Auth Dashboard 端口"
  value       = local.dashboard_port
}

output "stack_secret_key" {
  description = "Stack Auth 服务端密钥（注入 .env）"
  value       = local.secret_key
  sensitive   = true
}

output "stack_admin_key" {
  description = "Stack Auth 管理员 API Key（用于初始配置）"
  value       = local.admin_key
  sensitive   = true
}
