output "bucket" {
  description = "OSS 桶名"
  value       = alicloud_oss_bucket.this.bucket
}

output "domain" {
  description = "CDN 域名"
  value       = var.domain
}

output "cdn_domain" {
  description = "CDN 域名详情"
  value       = alicloud_cdn_domain_new.this.domain_name
}

output "cdn_cname" {
  description = "CDN CNAME"
  value       = alicloud_cdn_domain_new.this.cname
}

output "host_record" {
  description = "DNS rr（host record）"
  value       = local.host_record
}
