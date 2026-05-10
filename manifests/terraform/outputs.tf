output "stack_auth_dir" {
  description = "Stack Auth 配置文件目录（含 start.sh）"
  value       = local.stack_auth_dir
}

output "stack_auth_start_command" {
  description = "Stack Auth 启动命令"
  value       = "cd ${local.stack_target_dir} && ~/.stack-auth/start.sh pnpm dev"
}

output "stack_setup_commands" {
  description = "首次部署步骤"
  value = <<-EOT
    sudo bash ~/.local/bin/bootstrap-postgres.sh
    bash ~/.local/bin/clone-stack-auth.sh
    cd ${local.stack_target_dir} && ~/.stack-auth/start.sh pnpm dev
  EOT
}

output "stack_db_password" {
  description = "Stack Auth 数据库密码（已写入 Vault）"
  value       = local.db_password
  sensitive   = true
}

output "stack_server_secret" {
  description = "Stack Auth 服务端签名密钥（已写入 Vault）"
  value       = local.server_secret
  sensitive   = true
}
