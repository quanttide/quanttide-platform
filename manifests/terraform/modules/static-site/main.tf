# =============================================================================
# static-site — 静态站点（site / studio / docs）OSS + CDN + DNS
#
# 收敛自各仓库重复的 `site-bucket.tf` + `cdn.tf`（如 qtcrowd）。一个模块覆盖
# site / studio / docs 三种静态 web 部署，通过 `name` / `domain` / `bucket`
# 参数化。账号级 CDN 私有回源授权由 `modules/cdn-auth` 管理，本模块不重复创建。
#
# 已知坑处理（见 docs/handbook/stage/deploy.md）：
#   - SSL 证书：terraform 不管理证书内容，复用 *.quanttide.com 泛域名证书，
#     单层子域可直接覆盖；未配置前域名仅 HTTP 可用（certificate_config 留占位）。
#   - SPA 回退：React/Router 子路由刷新 404 → back_to_origin_url_rewrite 改写。
#   - 私有 OSS 回源鉴权：l2_oss_key private_oss_auth=on（角色在 cdn-auth）。
#   - 缓存策略：由 workflow 侧分离（assets 长缓存 / index.html no-cache）。
# =============================================================================

locals {
  # rr：domain 去掉 root_domain 后缀，如 studio.health.quanttide.com → studio.health
  host_record = replace(var.domain, ".${var.root_domain}", "")
  # OSS 源站主机名
  oss_host = "${var.bucket}.oss-${var.region}.aliyuncs.com"
}

# ── OSS 静态网站桶（私有；CDN 私有回源） ──────────────────────────────
resource "alicloud_oss_bucket" "this" {
  bucket            = var.bucket
  storage_class     = "Standard"
  resource_group_id = var.resource_group_id
  tags = {
    project     = var.project
    environment = var.environment
  }

  # 静态网站托管：index.html 为入口
  website {
    index_document = "index.html"
    error_document = "index.html"
  }
}

# ── CDN 域名 ────────────────────────────────────────────────────────
resource "alicloud_cdn_domain_new" "this" {
  domain_name = var.domain
  cdn_type    = "web"

  sources {
    content  = local.oss_host
    type     = "oss"
    port     = 80
    priority = 20
  }

  # HTTPS 证书：由 acme.sh 管理（*.quanttide.com 泛域名证书，90 天自动续期），
  # terraform 不管理证书内容（避免私钥入库）。
  # certificate_config {
  #   cert_type                  = "upload"
  #   server_certificate         = "<PEM 公钥，acme.sh 签发>"
  #   private_key                = "<PEM 私钥>"
  #   server_certificate_status  = "on"
  # }
}

# ── 私有 Bucket 回源开关（l2_oss_key：private_oss_auth=on，自动 STS 同账号回源） ──
resource "alicloud_cdn_domain_config" "private_back" {
  count         = var.enable_private_back ? 1 : 0
  domain_name   = alicloud_cdn_domain_new.this.domain_name
  function_name = "l2_oss_key"
  function_args {
    arg_name  = "private_oss_auth"
    arg_value = "on"
  }
}

# ── SPA 回退改写：子路由直接访问/刷新回源 OSS 404 → 改写为 /index.html ──
resource "alicloud_cdn_domain_config" "spa_fallback" {
  count         = var.enable_spa_fallback ? 1 : 0
  domain_name   = alicloud_cdn_domain_new.this.domain_name
  function_name = "back_to_origin_url_rewrite"
  function_args {
    arg_name  = "source_url"
    arg_value = "^/(?!index\\.html$|assets/|vite\\.svg$).*"
  }
  function_args {
    arg_name  = "target_url"
    arg_value = "/index.html"
  }
  function_args {
    arg_name  = "flag"
    arg_value = "break"
  }
}

# ── 强制 HTTPS：HTTP 请求 301 跳转 HTTPS ─────────────────────────────
resource "alicloud_cdn_domain_config" "https_force" {
  count         = var.enable_https ? 1 : 0
  domain_name   = alicloud_cdn_domain_new.this.domain_name
  function_name = "https_force"
  function_args {
    arg_name  = "enable"
    arg_value = "on"
  }
}

# ── DNS：CNAME 接入 ──────────────────────────────────────────────────
resource "alicloud_alidns_record" "this" {
  domain_name = var.root_domain
  rr          = local.host_record
  type        = "CNAME"
  value       = alicloud_cdn_domain_new.this.cname
  ttl         = 600
}
