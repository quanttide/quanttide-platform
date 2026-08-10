# API 网关（系统级）：传统版 Serverless，统一入口 api.quanttide.com
#
# 用途：所有云服务 FC 的统一公网入口（/qtcloud-auth、/qtcloud-pay 等路径前缀），
# 后续可在此层做统一鉴权/限流/WAF。
# 计费：传统版 Serverless——前 100 万次/月免费，无固定实例费（果总选型：选便宜的）。
#
# 管理边界（2026-08 现状）：
#   - 本文件：分组 + 自定义域名（terraform 管理）
#   - API 定义/DNS 记录：scripts/api-gateway/deploy.sh + dns.py（幂等脚本，CLI 已打通；
#     alicloud provider 的 api_gateway_api 定义复杂且本地 init 受网络限制，先脚本化）
#   - 证书：*.quanttide.com 泛域名证书由 acme.sh 签发，CI ssl-cert.yml 绑定网关
#
# 域名：api.quanttide.com（CNAME → 分组子域名，DNS 记录由 dns.py 管理）

resource "alicloud_api_gateway_group" "qtcloud" {
  name        = "qtcloud"
  description = "量潮云 API 网关（系统级）"
}

# 域名绑定：api.quanttide.com → 本分组（需 DNS CNAME 先生效，所有权校验）
resource "alicloud_api_gateway_domain" "api" {
  group_id       = alicloud_api_gateway_group.qtcloud.id
  domain_name    = "api.quanttide.com"
  certificate_id = "" # 证书由 CI ssl-cert.yml 经 SetDomainCertificate 绑定（acme 续期自动更新）
}
