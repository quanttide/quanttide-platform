# =============================================================================
# cdn-auth — 账号级 CDN 回源私有 OSS 授权（阿里云官方命名）
#
# 该模块创建「CDN/DCDN 回源私有 OSS Bucket」所需的账号级角色与策略，幂等，
# 全账号只需调用一次（由 quanttide-platform 根 IaC 调用），多个站点共享。
# 站点级（bucket / CDN / DNS）由 `modules/static-site` 负责，不重复创建本角色。
# =============================================================================

# 自定义策略：OSS 只读（List/Get）
resource "alicloud_ram_policy" "cdn_private_oss" {
  policy_name     = "AliyunCDNAccessingPrivateOSSRolePolicy"
  description     = "用于CDN/DCDN回源私有OSS Bucket角色的授权策略，包含OSS的只读权限"
  policy_document = <<-EOT
    {
      "Version": "1",
      "Statement": [
        { "Action": ["oss:List*", "oss:Get*"], "Resource": "*", "Effect": "Allow" }
      ]
    }
  EOT
}

# 角色：信任 CDN 服务（cdn.aliyuncs.com 可 AssumeRole）
resource "alicloud_ram_role" "cdn_private_oss" {
  role_name                   = "AliyunCDNAccessingPrivateOSSRole"
  description                 = "用于CDN回源私有OSS Bucket"
  assume_role_policy_document = <<-EOT
    {
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Effect": "Allow",
          "Principal": { "Service": ["cdn.aliyuncs.com"] }
        }
      ],
      "Version": "1"
    }
  EOT
}

# 策略绑定到角色
resource "alicloud_ram_role_policy_attachment" "cdn_private_oss" {
  role_name   = alicloud_ram_role.cdn_private_oss.role_name
  policy_name = alicloud_ram_policy.cdn_private_oss.policy_name
  policy_type = "Custom"
}

output "role_name" {
  value = alicloud_ram_role.cdn_private_oss.role_name
}

output "policy_name" {
  value = alicloud_ram_policy.cdn_private_oss.policy_name
}
