variable "region" {
  description = "阿里云地域"
  type        = string
  default     = "cn-hangzhou"
}

variable "environment" {
  description = "环境：dev / staging / prod"
  type        = string
  default     = "prod"
}

variable "vpc_cidr" {
  description = "VPC 网段"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vswitch_cidr" {
  description = "交换机网段（FC 等应用资源所在子网）"
  type        = string
  default     = "10.0.1.0/24"
}

variable "db_engine_version" {
  description = "RDS PostgreSQL 版本（Serverless 支持 18.0，官方文档过时；预检查已确认 17→18 合法）"
  type        = string
  default     = "18.0"
}

variable "db_category" {
  description = "RDS 系列：serverless_basic（Serverless 基础版，可用区 cn-hangzhou-k）"
  type        = string
  default     = "serverless_basic"
}

variable "db_min_capacity" {
  description = "RDS Serverless 最小算力（RCU）"
  type        = number
  default     = 0.5
}

variable "db_max_capacity" {
  description = "RDS Serverless 最大算力（RCU）"
  type        = number
  default     = 4
}
