variable "name" {
  description = "资源前缀（site / studio / docs），用于标识与标签"
  type        = string
}

variable "domain" {
  description = "CDN 域名，如 studio.quanttide.com 或 studio.health.quanttide.com"
  type        = string
}

variable "bucket" {
  description = "OSS 桶名（全局唯一；静态网站模式）"
  type        = string
}

variable "root_domain" {
  description = "根域名（用于推导 DNS rr，如 quanttide.com）"
  type        = string
  default     = "quanttide.com"
}

variable "project" {
  description = "项目名（资源命名前缀与标签）"
  type        = string
  default     = ""
}

variable "environment" {
  description = "环境：dev / staging / prod"
  type        = string
  default     = "prod"
}

variable "region" {
  description = "阿里云地域"
  type        = string
  default     = "cn-hangzhou"
}

variable "resource_group_id" {
  description = "系统级资源组 ID（来自 quanttide-platform 根 IaC 输出）"
  type        = string
  default     = ""
}

variable "enable_spa_fallback" {
  description = "是否配置 SPA 回退改写（React/Router 子路由刷新 404）"
  type        = bool
  default     = true
}

variable "enable_private_back" {
  description = "是否配置私有 OSS 回源鉴权（l2_oss_key private_oss_auth=on）"
  type        = bool
  default     = true
}

variable "enable_https" {
  description = "是否强制 HTTPS 301 跳转"
  type        = bool
  default     = true
}
