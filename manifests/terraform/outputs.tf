# 系统级输出：供应用仓库（quanttide-pay 等）通过 terraform_remote_state 或 data source 引用
output "vpc_id" {
  description = "系统级 VPC ID"
  value       = alicloud_vpc.this.id
}

output "vswitch_id" {
  description = "系统级交换机 ID（cn-hangzhou-k）"
  value       = alicloud_vswitch.this.id
}

output "security_group_id" {
  description = "系统级安全组 ID（应用 FC 挂载用）"
  value       = alicloud_security_group.this.id
}

output "rds_instance_id" {
  description = "共享 RDS 实例 ID"
  value       = alicloud_db_instance.this.id
}

output "rds_connection_string" {
  description = "共享 RDS 内网连接地址（应用建库/连接用）"
  value       = alicloud_db_instance.this.connection_string
}

output "rds_port" {
  description = "RDS 端口"
  value       = alicloud_db_instance.this.port
}
