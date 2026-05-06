---
name: product-studio
description: Flutter Studio 客户端开发流程。从需求到发布，覆盖项目初始化、数据模型、UI 开发、构建、录制演示的完整工作流。
---

# product-studio

Flutter Studio 客户端开发流程。

## 参考技能

- devops-commit: 提交代码变更

## 工作流

### 1. 初始化 Flutter 项目

```bash
flutter create --project-name <name> --org com.quanttide --platforms android,ios,web,macos,linux <path>
```

必须的参数：
- `--project-name`: 包名，也是 Linux 产物名（如 `qtconsult_studio` → 产物 `qtconsult-studio`）
- `--org`: Android 包名前缀
- `--platforms`: 目标平台列表

### 2. 配置 pubspec.yaml

```yaml
name: qtconsult_studio
description: <中文描述>

dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.5

flutter:
  assets:
    - assets/<data>.json
```

必须添加的依赖：
- `provider`：状态管理
- `assets/`：数据源 JSON 文件

### 3. 搭建目录结构

```
lib/
  main.dart             # 入口 + Provider 初始化
  models/               # 数据模型
  services/             # JSON 加载器 + ChangeNotifier
  screens/              # 页面级组件
  widgets/              # 可复用 UI 组件
assets/
  <data>.json           # 模拟数据
scripts/
  run-studio-linux.sh   # 构建运行脚本
  record-studio-linux.sh # 录制演示视频
```

### 4. 设计数据模型

每条模型必须包含：
- `const` 构造函数
- `factory fromJson(Map<String, dynamic>)` 工厂方法
- `copyWith` 方法（可选）
- 关联的枚举类型

### 5. 开发 OODA 四栏看板

布局结构：

```
调研 · Observe  分析 · Orient  决策 · Decide  执行 · Act
```

列宽比例：调研 1.4 / 分析 1.0 / 决策 1.2 / 执行 0.4

调研栏特殊要求：业务理想（左半区）与现实状况（右半区）**左右并列**，不同底色区分，各自独立滚动。

信息密度规则：
- 正文 ≤ 2 行 (`maxLines: 2`)
- 标题简明，去掉冗余前缀
- 卡片 padding 14-16px，间距 10-12px
- 标题 14px，正文 13px，meta 12px

### 6. 修改应用名称

**必须执行，不可跳过**

Flutter 默认用项目目录名作为显示名称，需手动修改以下文件：

| 平台 | 文件 | 修改内容 |
|------|------|---------|
| Linux | `linux/runner/my_application.cc` | `gtk_header_bar_set_title(header_bar, "量潮咨询")` 和 `gtk_window_set_title(window, "量潮咨询")` |
| Android | `android/app/src/main/AndroidManifest.xml` | `android:label="量潮咨询"` |
| iOS | `ios/Runner/Info.plist` | `CFBundleDisplayName` 和 `CFBundleName` 改为中文名 |

### 7. 验证构建

```bash
cd src/<project>
dart analyze lib/
flutter build linux
```

必须满足：
- `dart analyze lib/` 零报错
- `flutter build linux` 构建成功

### 8. 创建录制脚本

创建 `scripts/record-studio-linux.sh`：

```bash
# 核心流程
cleanup() { ... }
trap cleanup EXIT

# 启动 App
"$STUDIO_BIN" &
sleep 4

# 查找窗口
WID=$(xdotool search --name "量潮咨询" 2>/dev/null | head -1)

# 调整窗口
xdotool windowsize "$WID" 1440 900

# 录制
ffmpeg -f x11grab -video_size "${WIDTH}x${HEIGHT}" \
  -i ":0.0+${X},${Y}" -framerate 30 \
  -c:v libx264 -preset ultrafast -crf 18 "$VIDEO_OUT"

# 鼠标交互
xdotool mousemove --window "$WID" <X> <Y> click 1
```

依赖：`xdotool`、`ffmpeg`。

### 9. 提交流程

遵循 devops-commit 规范，提交类型：
- `feat`: 新功能
- `fix`: 修复
- `chore`: 构建/配置变更
- `docs`: 文档

子模块提交流程：

```bash
# 子模块内
cd apps/<submodule>
git add -A && git commit -m "feat: <描述>" && git push

# 主仓库
cd ../..
git add apps/<submodule>
git commit -m "chore: update <submodule> submodule (<描述>)" && git push
```
