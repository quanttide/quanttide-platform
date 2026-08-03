# 凭证：本地走 ~/.aliyun/config.json + ALICLOUD_PROFILE；CI 经 ALIYUN_ACCESS_KEY_ID/SECRET 注入
provider "alicloud" {
  region = var.region
}

# 远程状态：OSS（系统级与应用级 IaC 分离，key 按仓库隔离）
terraform {
  backend "oss" {}
}
