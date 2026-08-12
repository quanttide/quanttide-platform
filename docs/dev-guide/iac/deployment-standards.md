# 部署统一规范（IaC 标准）

> 2026-08-12 果总指示：确保所有云在统一的模式之下进行部署；与现有规范不一致的全部干掉重跑。
> IaC 核心作用：避免手动操作/不同人操作导致不一致——不一致就干掉重来。

## 一、统一账号与资源归属

| 资源 | 归属账号 | 说明 |
|------|----------|------|
| 阿里云（RDS/FC/OSS/API 网关/DNS） | **量潮主账号**（公司账号） | 所有云统一用公司账号，**不允许个人账号部署** |
| ACR 容器镜像 | **量潮主账号下的统一 ACR 个人版实例** | registry 地址统一（勿用个人账号实例）；固定凭证（控制台生成），不用 AK 当 docker 密码 |
| GitHub org secrets | quanttide org（公共云）+ quanttide-tech org（业务云） | **两个 org 配置相同的部署 secrets**（避免跨 org 缺失） |
| OSS 状态桶 | quanttide-terraform-state | 各应用独立 key：`<service>/terraform.tfstate` |

## 二、secrets 清单（每 org 必备）

| Secret 名 | 用途 |
|-----------|------|
| `ALIYUN_ACCESS_KEY_ID` / `ALIYUN_ACCESS_KEY_SECRET` | 阿里云 RAM 凭据（terraform/aliyun CLI） |
| `ALIYUN_ACR_USERNAME` / `ALIYUN_ACR_PASSWORD` | ACR 固定凭证（docker login，**非 AK**） |
| `ALIYUN_ACR_REGISTRY` | ACR 实例地址（统一公司实例） |
| `DOCKERHUB_USERNAME` / `DOCKERHUB_PASSWORD` | Docker Hub（可选，双通道） |
| `DB_PASSWORD` / `DB_PASSWORD_DEV` | RDS 数据库密码（dev/prod 分开） |
| `ADMIN_TOKEN` | 运维端点保护（粘贴勿带换行） |
| `JWT_PRIVATE_KEY` | JWT RS256 私钥（**base64 单行**——GitHub Actions env 不支持多行 PEM） |

## 三、部署前置检查清单（新服务上线前）

- [ ] ACR 仓库已由主账号创建（PUBLIC，FC 免凭证直拉）
- [ ] org secrets 齐全（见上表；业务云在 quanttide-tech org 也要配）
- [ ] tfstate key 独立（`<service>/terraform.tfstate`）
- [ ] 网关 API 定义经 `scripts/api-gateway/deploy.sh`（幂等脚本，含 Authorization 头透传）
- [ ] FC 环境变量按各服务规范（JWT 相关用 base64 单行）

## 四、不一致处理原则（果总）

- 与规范不一致的配置/资源：**全部干掉旧的，按统一规范重跑**（IaC 精神）
- 不修复单个不一致（会累积差异），直接重做

## 五、已知踩坑（详见各仓库 docs/dev-guide/ci.md）

- GitHub Actions env 不支持多行（PEM 用 base64 单行）
- 传统 API 网关丢 Authorization 头（需 HEAD 参数透传）
- 个人版 ACR 用固定密码登录（AK 当密码无效）
