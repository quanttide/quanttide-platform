# Terraform Modules — 收敛后的部署 IaC

> 共享的部署基础设施模块，收敛自各仓库重复的 `cdn.tf` / `site-bucket.tf` /
> `studio-bucket.tf` / `fc.tf`。各仓库的 `manifests/terraform/` 只保留**薄声明**
> （`main.tf` 的 module 调用），不再复制基础设施代码。

## 模块清单

| 模块 | 用途 | 部署形态 |
|------|------|---------|
| [`static-site`](static-site) | 静态站点：OSS 桶 + CDN + DNS + SPA 回退 + 私有回源 + 强制 HTTPS | `site` / `studio` / `docs` |
| [`fc`](fc) | 后端服务（provider / API）：Aliyun Function Compute 3.0（custom-container） | `provider` |
| [`cdn-auth`](cdn-auth) | 账号级 CDN 回源私有 OSS 授权（RAM 角色/策略） | 全账号 **只需调用一次** |

## 使用

每个仓库的 `manifests/terraform/main.tf` 以 git 源引用共享模块，如：

```hcl
# 系统级账号资源（一次性）：CDN 回源私有 OSS 授权
module "cdn_auth" {
  source = "git::https://github.com/quanttide/quanttide-platform.git//manifests/terraform/modules/cdn-auth?ref=v1"
}

# 静态站点（studio）
module "studio" {
  source  = "git::https://github.com/quanttide/quanttide-platform.git//manifests/terraform/modules/static-site?ref=v1"
  name    = "studio"
  domain  = "studio.quanttide.com"
  bucket  = "qtcloud-devops-studio"
  project = "qtcloud-devops"
}

# 后端服务（provider）
module "provider" {
  source = "git::https://github.com/quanttide/quanttide-platform.git//manifests/terraform/modules/fc?ref=v1"
  name   = "qtcloud-devops-provider"
  image  = "<registry>/qtcloud-devops-provider:latest"
  resource_group_id = data.terraform_remote_state.platform.outputs.resource_group_id
  vpc_id            = data.terraform_remote_state.platform.outputs.vpc_id
  vswitch_ids      = [data.terraform_remote_state.platform.outputs.vswitch_id]
  security_group_id = data.terraform_remote_state.platform.outputs.security_group_id
}
```

## 已知坑（模块已内置/需注意）

- **SSL 证书**：terraform 不管理证书内容（避免私钥入库），复用 `*.quanttide.com` 泛域名证书；
  单层子域可直接覆盖，`certificate_config` 留注释占位，未配置前域名仅 HTTP 可用。
- **SPA 回退**：`static-site` 模块内置 `back_to_origin_url_rewrite`，子路由刷新不再 404。
- **私有 OSS 回源**：`static-site` 模块开启 `l2_oss_key private_oss_auth=on`，对应的账号级
  RAM 角色/策略由 `cdn-auth` 模块（调用一次）创建。
- **缓存策略分离**：assets 长缓存 + `index.html` no-cache 由 workflow 侧（上传步骤）处理，
  不在 IaC 内。

## 验证

```bash
for m in cdn-auth static-site fc; do
  (cd "$m" && terraform fmt -check && terraform validate)
done
```
