variable "name" {
  description = "应用/服务名（资源命名前缀，如 qtcloud-auth）"
  type        = string
}

variable "description" {
  description = "函数描述"
  type        = string
  default     = ""
}

variable "image" {
  description = "容器镜像（FC 3.0 custom-container）"
  type        = string
}

variable "port" {
  description = "容器监听端口（对齐 provider 约定，默认 8080）"
  type        = number
  default     = 8080
}

variable "cpu" {
  description = "CPU（vCPU，如 0.5）"
  type        = number
  default     = 0.5
}

variable "memory_size" {
  description = "内存（MB）"
  type        = number
  default     = 512
}

variable "timeout" {
  description = "函数超时（秒）"
  type        = number
  default     = 60
}

variable "environment_variables" {
  description = "环境变量（注意：会以明文进 tfstate，生产建议用配置中心）"
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "阿里云地域"
  type        = string
  default     = "cn-hangzhou"
}

variable "project" {
  description = "项目名（标签）"
  type        = string
  default     = ""
}

variable "environment" {
  description = "环境：dev / staging / prod"
  type        = string
  default     = "prod"
}

variable "resource_group_id" {
  description = "系统级资源组 ID（来自 quanttide-platform 根 IaC 输出）"
  type        = string
  default     = ""
}

variable "vpc_id" {
  description = "VPC ID（来自 quanttide-platform 根 IaC 输出）"
  type        = string
  default     = ""
}

variable "vswitch_ids" {
  description = "交换机 ID 列表（来自 quanttide-platform 根 IaC 输出）"
  type        = list(string)
  default     = []
}

variable "security_group_id" {
  description = "安全组 ID（来自 quanttide-platform 根 IaC 输出）"
  type        = string
  default     = ""
}
