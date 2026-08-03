# quanttide-platform IaC（系统级）

quanttide 体系**系统级共享基础设施**的 Terraform 代码（阿里云）：

- 网络：VPC / 交换机（cn-hangzhou-k）/ 安全组
- 数据库：RDS PostgreSQL Serverless（PG 18，共享实例，各应用自建库）
- 资源组：`quanttide`
- 命名：`quanttide-<env>`（命名规则见 quanttide-pay 的 docs/dev-guide/iac.md）

**管理边界**：本仓库只管理系统级共享资源；应用级资源（数据库/账号、FC 函数、RAM 角色）由各应用仓库管理（如 quanttide-pay），通过本仓库的 `outputs` 引用。

## 使用

```sh
# 凭证：本地 ~/.aliyun/config.json + ALICLOUD_PROFILE；CI 经 ALIYUN_ACCESS_KEY_ID/SECRET
terraform init \
  -backend-config="bucket=quanttide-terraform-state" \
  -backend-config="key=quanttide-platform/terraform.tfstate" \
  -backend-config="region=cn-hangzhou"
cp terraform.tfvars.example terraform.tfvars
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

## 前置条件（账号级一次性）

- RDS 服务关联角色（两个都需存在）：
  ```sh
  aliyun rds CreateServiceLinkedRole --RegionId cn-hangzhou --ServiceLinkedRole AliyunServiceRoleForRdsPgsqlOnEcs
  aliyun rds CreateServiceLinkedRole --RegionId cn-hangzhou --ServiceLinkedRole AliyunServiceRoleForRDSProxyOnEcs
  ```
- OSS 状态桶 `quanttide-terraform-state`（含版本控制）

## 踩坑记录

- **可用区**：cn-hangzhou-b 无 RDS Serverless 库存（工单确认），固定使用 cn-hangzhou-k
- **PayType**：Serverless 实例 `instance_charge_type` 必须为 `Serverless`，否则报 `InvalidSaleComponentFault`
- **SLR**：`ServiceLinkedRole.NotExist` 需两个角色都存在，错误信息不指向第二个
- **版本**：官方文档称 Serverless 暂不支持 PG 18（已过时）；大版本升级预检查确认 17→18 合法，实例可直接建 18
