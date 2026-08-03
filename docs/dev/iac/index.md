# 系统级 IaC

quanttide 体系**系统级共享基础设施**的 Terraform 代码（阿里云），位于 [manifests/terraform/](../../../manifests/terraform/)。

## 定位

本仓库只管理系统级共享资源；应用级资源（应用数据库/账号、FC 函数、RAM 角色）由各应用仓库管理（如 quanttide-pay），通过本仓库的 `outputs` 引用系统级资源。

## 资源清单

- 网络：VPC（10.0.0.0/16）、交换机（cn-hangzhou-k）、安全组
- 数据库：RDS PostgreSQL Serverless（PG 18，共享实例，各应用自建库）
- 资源组：`quanttide`（不存在时自动创建）
- 命名：`quanttide-<env>`（dev / staging / prod，默认 prod）

## 输出引用

应用仓库通过 terraform_remote_state 或 data source 引用系统级输出：

- `vpc_id` — 系统级 VPC ID
- `vswitch_id` — 交换机 ID（cn-hangzhou-k）
- `security_group_id` — 安全组 ID（应用 FC 挂载用）
- `rds_instance_id` — 共享 RDS 实例 ID
- `rds_connection_string` — RDS 内网连接地址（应用建库/连接用）
- `rds_port` — RDS 端口
- `resource_group_id` — quanttide 资源组 ID（应用资源归入同一组）

## 使用与前置条件

使用步骤、账号级一次性前置条件与踩坑记录见 [manifests/terraform/README.md](../../../manifests/terraform/README.md)。
