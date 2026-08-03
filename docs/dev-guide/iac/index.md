# 基础设施与 IaC

## 设计原则

### 供应商可互换

阿里云、腾讯云、本地 NAS 在架构中地位等价，通过标准 IaaS 协议（S3 兼容对象存储、OIDC 认证、k8s 标准 API）解耦。任一供应商可被替换，不产生架构级影响。

## 计算

大型系统以 k8s 为主，以服务器和函数为辅。主要是考虑 k8s 既具备兼容性又具备弹性。

## 存储

以对象存储为主、数据库为辅。主要考虑适应 AI 的读写方式。

## DevOps 平台

采用三地冗余策略保障代码与配置安全：

| 层级 | 平台 | 用途 |
|------|------|------|
| 主平台 | GitHub | DevOps 工作流主阵地：CI/CD、Issue 管理、Code Review |
| 热备 | GitLink | 国内访问低延迟镜像，主平台不可用时的应急通道 |
| 冷备 | 本地 NAS | 全量仓库定期归档，不依赖任何外部服务 |

所有环境通过 GitOps 工作流（声明式配置 + 自动化同步）驱动，变更可审计、可回滚、可复现。

## 身份服务

采用自托管身份方案作为基础设施，提供 OAuth/OIDC 认证、用户管理和角色权限。底层实现按阶段演进：初期 Stack Auth（速度），中期 SuperTokens（稳定性），远期 Authlib（完全控制）。详见 [身份云](https://github.com/quanttide/quanttide-profile-of-product-development/blob/main/products/default/apps/auth.md)。

## 系统级 IaC

quanttide 体系**系统级共享基础设施**的 Terraform 代码（阿里云），位于 [manifests/terraform/](../../../manifests/terraform/)。

### 定位

本仓库只管理系统级共享资源；应用级资源（应用数据库/账号、FC 函数、RAM 角色）由各应用仓库管理（如 quanttide-pay），通过本仓库的 `outputs` 引用系统级资源。

### 资源清单

- 网络：VPC（10.0.0.0/16）、交换机（cn-hangzhou-k）、安全组
- 数据库：RDS PostgreSQL Serverless（PG 18，共享实例，各应用自建库）
- 资源组：`quanttide`（不存在时自动创建）
- 命名：`quanttide-<env>`（dev / staging / prod，默认 prod）

### 输出引用

应用仓库通过 terraform_remote_state 或 data source 引用系统级输出：

- `vpc_id` — 系统级 VPC ID
- `vswitch_id` — 交换机 ID（cn-hangzhou-k）
- `security_group_id` — 安全组 ID（应用 FC 挂载用）
- `rds_instance_id` — 共享 RDS 实例 ID
- `rds_connection_string` — RDS 内网连接地址（应用建库/连接用）
- `rds_port` — RDS 端口
- `resource_group_id` — quanttide 资源组 ID（应用资源归入同一组）

### 使用与前置条件

使用步骤、账号级一次性前置条件与踩坑记录见 [manifests/terraform/README.md](../../../manifests/terraform/README.md)。

### 注意事项

- RDS Serverless 实例空闲自动暂停（`auto_pause`），`terraform plan` 的 refresh 阶段查询实例会触发唤醒，plan 可能卡住数分钟甚至超时，属正常现象，等待唤醒完成即可

## 各领域文档

| 文档 | 内容 |
|------|------|
| [access_control.md](access_control.md) | 访问管理（子账号划分、最小授权） |
| [databases.md](databases.md) | 数据库（PostgreSQL 选型、实例/库/schema 划分） |
| [logging_services.md](logging_services.md) | 日志服务（日志集、日志主题划分） |
| [microservers.md](microservers.md) | 微服务（部署、编排、API 网关、事件治理） |
| [secrets.md](secrets.md) | 密钥管理（Vault 架构、解封策略） |
| [storages.md](storages.md) | 存储（对象存储、桶命名与标签） |
| [websites.md](websites.md) | 静态网站托管（域名、部署规则） |
