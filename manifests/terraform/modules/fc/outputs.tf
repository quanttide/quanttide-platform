output "function_name" {
  description = "FC 函数名"
  value       = alicloud_fcv3_function.this.function_name
}

output "role_arn" {
  description = "FC 默认角色 ARN"
  value       = alicloud_ram_role.fc.arn
}

output "trigger_url" {
  description = "HTTP 触发器 URL"
  value       = "https://${alicloud_fcv3_function.this.function_name}.${var.region}.fc.aliyuncs.com"
}
