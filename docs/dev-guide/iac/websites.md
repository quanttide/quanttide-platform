# 静态网站托管

部署在云平台对象存储，通过手动配置静态网站。

## 存储桶

命名规范为`<service>-web-<env>`，比如`qtclass-web-prod`。由于存储桶名称限制在20个以内，因此环境变量使用缩写`dev`、`test`、`prod`，或者`d`、`t`、`p`。

创建存储桶以后，打开静态网站设置，如果有必要则打开自定义源站域名和自定义CDN域名。

## 域名

### 一级域名

- quanttide.com用于生产环境。
- quanttidetech.com用于预生产环境。
- 开发环境使用云平台默认域名。

### 二级域名

- <hostname>用于企业官网（site 用主域名）。
- class.<hostname>用于课程平台（量潮课堂APP）。
- services.<hostname>用于数据服务平台（量潮数据服务APP）。
- admin.<hostname>用于内部管理平台（量潮企业后台APP）。

### 前端应用域名规则（2026-08-12 果总决策）

**一域名、一存储桶、一前端应用一一对应**：前端客户端统一用 `studio.<hostname>` 子域名。

- `studio.class.quanttide.com`：课程平台客户端（qtclass studio）
- `studio.delib.cloud.quanttide.com`：议事云客户端（qtcloud-delib studio）
- 其余应用客户端同理（`studio.<应用主域名>`）

即：应用主域名（如 class.quanttide.com）承载站点/服务端入口，`studio.` 前缀承载该应用的前端应用。

### 已分配域名

- 管理后台客户端：`admin.quanttide.com`
- 管理后台服务端：`api.admin.quanttide.com`
- 课程平台客户端：`studio.class.quanttide.com`
- 系统级 API 网关：`api.quanttide.com`

## 部署规则

![静态网站部署规则](images/websites_deployment.jpg)

## 日志投递

每个环境一个固定存储桶，命名规范为`qtapps-web-<env>`，比如`qtapps-web-prod`。

存储桶内以应用隔离文件夹，以应用标识为文件夹名称，如`qtclass`、`qtadmin`。

## CDN 缓存策略与 SPA 深链回退

### 缓存策略分离

对象存储 + CDN 静态托管时，缓存策略按文件类型分离（清单见 flutter/apps.md「Web 发布与缓存」）：

- 入口/引导/固定文件名产物（如 `index.html`、`main.dart.js`）→ `Cache-Control: no-cache`
- 带内容哈希的产物（`assets/` 等）→ 长缓存

CDN 刷新只能清 CDN 边缘缓存，清不掉浏览器本地缓存——发布后"没变化"通常是历史长缓存策略留下的存量浏览器，需版本化引用破环（给入口文件里的 JS 引用附加构建哈希查询串）。

### Path URL 策略需要 SPA 深链回退改写

客户端改用 Path URL 策略（地址栏无 `#`，Flutter 用 `usePathUrlStrategy()`）后，直接访问或刷新子路由（如 `/record`）会回源 404。CDN 增加回源改写规则，把"非真实产物"的路径统一改写为 `/index.html`：

- 函数：`back_to_origin_url_rewrite`，`flag: break`
- source 用负向断言正则排除真实产物（阿里云 CDN 实测支持）：

```
^/(?!index\.html$|main\.dart\.js$|flutter\.js$|flutter_bootstrap\.js$|flutter_service_worker\.js$|manifest\.json$|version\.json$|favicon\.png$|assets/|icons/|canvaskit/).*
```

- 真实产物清单以 `flutter build web --release` 产物目录为准，Flutter 版本升级后需复查

### 多状态文件与 -target 局部应用

同一仓库多个站点各自独立状态文件（如 `qthealth/site.tfstate`、`qthealth/studio.tfstate`），CI 用 `-target` 只应用本站点资源，避免互相创建重复资源。

教训：`terraform init` 更换后端 key 后必须加 `-reconfigure`，否则 init 报错且 apply 仍按旧指针执行（会尝试创建已存在的资源，报 `DomainAlreadyExist` 等幂等错误——虽无害但状态指针混乱）。多状态文件下不要用整目录 apply。
