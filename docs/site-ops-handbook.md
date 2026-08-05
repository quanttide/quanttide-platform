# 量潮静态站点运维手册

> 最后更新：2026-08-05 | 维护者：黎想 → 郝子腾

---

## 一、架构总览

量潮的对象存储体系分三类功能，统一通过阿里云 OSS API 操作：

| 类型 | 用途 | 示例桶 |
|------|------|--------|
| **网盘**（private） | 业务数据存储：录屏、文档、数据集。通过 API 灵活操作，未来可部署到云端或保持本地，但数据管理一致性不变 | `qtdata-private` |
| **后台数据库**（provider） | 平台 API 的数据底座，CI 自动部署 | `qtadmin-provider` |
| **静态网站**（site/studio） | 网站托管，GitHub Release → Actions → OSS → CDN | `qtweb-site` |

核心原则：**GitHub 仓库与 OSS 桶一一对齐**，桶自身做权限隔离。无论数据在云端还是本地，管理方式一致。

### 静态网站部署架构

```
GitHub Release
    ↓ 触发
GitHub Actions（.github/workflows/deploy-*.yml）
    ↓ 构建 + ossutil 上传
OSS 桶（*-site / *-studio）
    ↓ CDN 回源
阿里云 CDN（*.*.w.kunlunaq.com）
    ↓ HTTPS（Let's Encrypt 泛域名证书）
用户浏览器
```

## 二、站点清单

| 站点 | 域名 | 桶 | 技术栈 | IaC |
|------|------|-----|--------|-----|
| qtweb | quanttide.com | qtweb-site | React | qtweb/deploy.yml |
| qtfounder | founder.quanttide.com | qtfounder-site | React/Vite | qtfounder/deploy.yml |
| qtdata | data.cloud.quanttide.com | qtdata-studio | Flutter Web | qtdata/deploy.yml |

### 备用域名

- `data.quanttide.com` → 同样指向 `qtdata-studio`
- `quanttide.tank.com` — 预生产环境（待部署）

## 三、日常操作

### 3.1 发布新版本

直接打 GitHub Release，CI 自动构建部署。不需要手动操作。

1. 进入对应仓库（如 qtweb）
2. Releases → Draft a new release
3. Tag 版本号（如 v0.1.0），点 Publish
4. GitHub Actions 自动运行，构建 + 上传 + 刷新 CDN
5. 等 2-5 分钟，刷新网站验证

### 3.2 手动部署（CI 挂了时用）

```bash
# React 站点
cd /path/to/repo
npm install && npm run build
aliyun oss cp build/ oss://qtweb-site/ -r -f

# Flutter 站点
cd /path/to/repo/src/studio
flutter build web
aliyun oss cp build/web/ oss://qtdata-studio/ -r -f
```

### 3.3 刷新 CDN 缓存

```bash
aliyun cdn RefreshObjectCaches --ObjectPath https://quanttide.com/ --ObjectType Directory
```

### 3.4 检查站点状态

```bash
curl -s -o /dev/null -w "%{http_code}" https://quanttide.com
# 应返回 200
```

## 四、阿里云 CLI 配置

```bash
# 安装
curl -o /usr/local/bin/aliyun https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz

# 配置凭证（从 GitHub Secrets 或密码本获取）
aliyun configure set --access-key-id <AK> --access-key-secret <SK> --region cn-hangzhou
```

## 五、SSL 证书

- 类型：ZeroSSL（通过 acme.sh 签发）
- 覆盖：`*.quanttide.com` + `quanttide.com`
- 有效期：90 天，自动续期
- 位置：`~/.acme.sh/quanttide.com_ecc/`
- 手动续期：`acme.sh --renew -d quanttide.com --force`

## 六、OSS 桶清单

| 桶 | 类型 | 用途 |
|------|------|------|
| qtweb-site | 公共读 | 官网 |
| qtfounder-site | 公共读 | 创始人站 |
| qtdata-studio | 公共读 | 数据云工作台 |
| qtadmin-private | 私有 | 内部资料 |
| qtdata-private | 私有 | 业务数据 |
| qtclass-private | 私有 | 课程资料 |
| qtrecruit-private | 私有 | 招聘资料 |
| qtcloud-private | 私有（空） | 预留 |
| qtconsult-private | 私有（空） | 预留 |
| qtadmin-provider | 私有 | 管理后台（即将上线） |
| quanttide-terraform-state | 私有 | IaC 状态 |

## 七、常见问题

### 网站访问空白
**原因**：桶被设为私有，CDN 无法回源。
**解决**：OSS 控制台 → 对应桶 → 权限管理 → 读写权限 → 公共读。

### HTTPS 证书过期
**现象**：浏览器提示证书错误。
**解决**：SSH 到服务器，运行 `acme.sh --cron` 强制续期，然后重新上传到 CDN。

### CDN 缓存未更新
**现象**：发布了新版本但网站还是旧的。
**解决**：执行 CDN 刷新（见 3.3）。

### 新增站点
参照 `.github/workflows/deploy-site.yml` 模板，三步：
1. 建 OSS 桶 + 设公共读
2. 加 CDN 域名 + 绑 SSL
3. 配 DNS CNAME
4. 仓库加 deploy.yml

## 八、数据管理规范（重点学习）

### 8.1 为什么用对象存储管理数据

对象存储通过 API 灵活操作，天然适合程序化管理。未来数据处理流程有两种模式：
- **本地模式**：数据在本地处理，通过 `ossutil cp` 同步到云端
- **云端模式**：数据直接在 OSS 上处理，配合函数计算等云产品

两种模式下**管理规则完全一致**——桶命名、权限策略、归档规范不变。

### 8.2 核心操作：qtdata-private

业务数据主桶。当前内容：
- `data/garment-factory/` — 服装厂项目
- `datasets/` — 天眼查、百度贴吧、判决书、速冻水饺

常用命令：
```bash
# 查看桶内容
aliyun oss ls oss://qtdata-private/

# 上传数据
aliyun oss cp ./local-data/ oss://qtdata-private/project-name/ -r -f

# 下载数据
aliyun oss cp oss://qtdata-private/datasets/ ./local-datasets/ -r
```

### 8.3 命名规则速查

| 规则 | 示例 |
|------|------|
| `{业务}-private` | `qtdata-private`, `qtclass-private` |
| `{仓库}-site` | `qtweb-site` |
| `{仓库}-studio` | `qtdata-studio` |
| `qtadmin-private/archive/` | 历史归档 |

## 九、TODO：郝子腾学习任务

1. **安装 CLI** — 配置 `aliyun-cli`，跑通 `oss ls`
2. **熟悉上传下载** — 在 `qtdata-private` 创建测试目录，上传下载几个文件
3. **理解命名规范** — 说出 6 个 private 桶分别对应什么业务
4. **了解 IaC** — 读一遍 `deploy-site.yml` 模板
5. **跑通部署** — 在 qtfounder 打一个 Release，观察 CI 自动部署

## 十、相关资源

- CI 模板：https://github.com/quanttide/.github/tree/main/workflows
- 详细文档：`/home/lx/量潮/对象存储治理-任务大纲.md`
- 阿里云账号：account@quanttide.com（密码在机密档案密码本）
- RAM 用户：lixiang6662333（CI 用的 AccessKey 在 GitHub Secrets）