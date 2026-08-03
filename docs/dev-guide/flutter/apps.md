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
