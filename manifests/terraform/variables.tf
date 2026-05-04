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
