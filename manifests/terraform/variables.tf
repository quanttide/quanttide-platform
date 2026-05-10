variable "bind_ip" {
  description = "Vault 监听 IP"
  type        = string
  default     = "127.0.0.1"
}

variable "container_port" {
  description = "Vault 监听端口"
  type        = number
  default     = 8200
}

variable "tls_disable" {
  description = "是否关闭 TLS"
  type        = bool
  default     = true
}

variable "home" {
  description = "用户家目录（不含 ~，需传绝对路径）"
  type        = string
}

variable "data_dir" {
  description = "存储数据目录"
  type        = string
  default     = null
}

variable "logs_dir" {
  description = "审计日志目录"
  type        = string
  default     = null
}

# --- Stack Auth ---

variable "stack_server_secret" {
  description = "Stack Auth 服务端签名密钥（留空自动生成）"
  type        = string
  default     = null
  sensitive   = true
}

variable "stack_db_user" {
  description = "Stack Auth 数据库用户"
  type        = string
  default     = null
}

variable "stack_db_password" {
  description = "Stack Auth 数据库密码（留空自动生成）"
  type        = string
  default     = null
  sensitive   = true
}

variable "stack_db_name" {
  description = "Stack Auth 数据库名"
  type        = string
  default     = null
}

variable "stack_vault_mount" {
  description = "Vault KV secrets engine 挂载路径"
  type        = string
  default     = null
}

variable "stack_api_port" {
  description = "Stack Auth API 端口"
  type        = number
  default     = null
}

variable "stack_dashboard_port" {
  description = "Stack Auth Dashboard 端口"
  type        = number
  default     = null
}

variable "stack_db_port" {
  description = "Stack Auth 数据库映射端口"
  type        = number
  default     = null
}
