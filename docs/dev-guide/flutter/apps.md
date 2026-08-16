# Flutter 应用升级经验

## 数据迁移

### 反序列化路径必须有 fallback

模型变更（增删字段、改类型）后，所有读数据的代码路径都要能处理旧格式，不能假设持久化数据和当前代码永远兼容。

常见路径：

- 缓存加载
- 本地 fixture 加载
- 远端 API 响应

保护手段：

- `fromJson` 中对可能缺失的字段用 `as String?` + 默认值，而非 `as String`
- 缓存加载路径加 try-catch，失败时降级到 fixture 或远端
- 预留数据迁移脚本，处理字段改名、格式重构等场景

### 数据契约在库层验证，在应用层使用

先在库层（`quanttide_project`）用 fixture 定义 JSON 格式、写测试验证序列化/反序列化正确性，再在应用层加载同格式数据。顺序不要反过来——先改应用代码再调 fixture 容易漏掉兼容性问题。

### 缓存键要考虑版本

如果缓存数据格式会随版本变化，考虑在缓存 key 或 value 中附带版本号，启动时检查版本不一致则清缓存重拉。

## 异常处理

### 数据加载函数整体保护

入口加载函数（如 `_loadData()`）应当用外层 try-catch 包裹全部逻辑，确保任何未预料的异常不会导致整个 Future 失败，而是返回一个带错误信息的结果供 UI 展示。

### FutureBuilder 必须处理 hasError

```dart
if (snapshot.hasError) {
  return ErrorWidget('加载失败: ${snapshot.error}');
}
```

不处理 `hasError` 时，异常导致 `snapshot.data` 为 null，用户看到的是"数据为空"而非具体错误，排查困难。

## fixture 管理

- fixture 同步维护两份（应用 assets + 库测试 fixtures）时，用复制命令确保一致，而非手动编辑
- fixture 修改后立即运行两侧测试（库的 `dart test` + 应用的 `flutter test`），覆盖加载路径和解析路径

## Web 发布与缓存

### 入口文件必须 no-cache，产物文件长缓存

OSS 静态桶 + CDN 部署 Flutter Web 时，缓存策略必须按文件类型分离：

- **no-cache**：`index.html`、`flutter_bootstrap.js`、`flutter_service_worker.js`、`manifest.json`、`favicon.png`、`main.dart.js`
- **长缓存**（`Cache-Control: public,max-age=31536000`）：仅 `assets/`、`canvaskit/`、`icons/` 下带内容哈希的文件

`main.dart.js` 是固定文件名、不带内容哈希，每次构建内容都变——曾因误设长缓存，发布后浏览器一直运行旧 JS，线上"看起来没有变化"。**必须 no-cache**。

### 已被长缓存的存量浏览器：版本化引用强制破环

no-cache 只对未来生效；已被长缓存（如 max-age=1 年）的浏览器不会重新校验，永远跑旧代码。强制破环手段：给 bootstrap 中 `main.dart.js` 引用附加构建哈希查询串（缓存键变化 → 强制重新拉取）：

```bash
VERSION=$(md5sum build/web/main.dart.js | cut -c1-10)
sed -i "s|\"main.dart.js\"|\"main.dart.js?v=${VERSION}\"|g" build/web/flutter_bootstrap.js
```

配合入口文件 no-cache，存量浏览器下次普通刷新即自愈：index.html 重新校验 → 新 bootstrap → 新 URL → 拉新 JS。

### Service Worker 不再提供离线缓存

新版 Flutter（3.44 实测）生成的 `flutter_service_worker.js` 是"自卸载"模板：install 后 `skipWaiting`，activate 时**注销自身并重载客户端**——不提供持久离线缓存。不要依赖 SW 做版本更新或缓存破环。

### 排查"线上没有变化"的诊断链

1. 对比 OSS 对象 ETag 与 CDN 返回内容的 MD5（非分片上传时 ETag 即内容 MD5）
2. 与本地 `flutter build web --release` 产物比对（大小 + 哈希）
3. 确认入口文件响应头 `Cache-Control: no-cache`（`curl -sI`）
4. 服务器内容为新 → 问题在浏览器本地缓存 → 用无痕窗口验证

### 功能下线保留组件代码

下线功能（如情绪日记/状态页/练习）时：文件保留在 lib/ 下不动，仅在路由表中移除注册、在导航中移除入口，文件头注明「已下线」及恢复方式。未来重新启用只需恢复路由注册，无需重写组件。

