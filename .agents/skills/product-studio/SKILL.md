# Skill: product-studio

量潮产品客户端（Flutter Studio）研发经验总结。

## 项目定位

`qtconsult-studio` 和 `qtadmin-studio` 是量潮产品的 Flutter 桌面客户端，面向管理层/咨询顾问，以看板形式聚合信息。非通用移动端 App，而是**桌面优先**的管理工具。

## 架构模式

### 技术栈
- **状态管理**: Provider + ChangeNotifier
- **数据源**: JSON 资产文件（`assets/`），客户端直接加载渲染，无需后端
- **数据模型**: 手写 `fromJson` 工厂 + `copyWith`（不用 freezed 代码生成）
- **布局**: LayoutBuilder 做响应式判断，桌面端 Row 多栏，移动端单列流式

### 项目结构
```
lib/
  main.dart                  # 入口，数据加载，Provider 注册
  models/                    # 数据模型 + 枚举 + 视觉工具函数
  services/                  # JSON 加载器 + ChangeNotifier 状态
  screens/                   # 页面级组件（组装各栏）
  widgets/                   # 栏级组件 + 卡片组件
assets/
  *.json                     # 模拟数据源
```

## OODA 看板设计经验

### 四栏布局（调研 · 分析 · 决策 · 执行）

```
调研 · Observe  分析 · Orient  决策 · Decide  执行 · Act
```

- 宽高比：调研 1.4 / 分析 1.0 / 决策 1.2 / 执行 0.4
- 各栏独立纵向滚动
- 桌面端：`Row` + `SizedBox` 定宽
- 移动端：`SingleChildScrollView` + `Column` 堆叠

### 调研栏：业务需求与技术现实并列

- 左右两半：左"业务理想"，右"现实状况"
- 不同底色区分（白底 vs 浅灰底），便于直观对比 gap
- 各自独立纵向滚动
- 每张卡片：标题 + 1-2 行正文 + 来源 + 确认状态 + 勾选框

### 信息密度控制（关键经验）

| 规则 | 说明 |
|------|------|
| 正文 ≤ 2 行 | `maxLines: 2` + `TextOverflow.ellipsis` |
| 标题 ≤ 8 字 | 去掉 "模拟 · " 等冗余前缀 |
| 间距充足 | card padding 14-16px，gap 10-12px，行高 1.6 |
| 字号偏大 | 标题 14px，正文 13px，meta 12px |
| 操作元素醒目 | checkbox 22x22px，progress bar 4px 高 |

### 决策栏：方案卡片

- 每张卡片：名称 + 优先级标签 + 优势 + 概要 + 资源 + 关键假设
- 底部：勾选框"倾向本方案" + 文本输入框（填顾虑/条件）
- 选中态：深色边框 + 浅灰底色

### 执行栏：任务卡片

- 状态色：待开始（灰）/ 进行中（深灰边框）/ 已完成（深色）/ 受阻（虚线）
- 进度条：底部 4px 高
- 元信息紧凑排列

## 命名规范

### 应用名称
修改以下位置（Flutter 默认用项目目录名 "studio"，需替换为中文名）：

| 平台 | 文件 | 键/行 |
|------|------|-------|
| Linux | `linux/runner/my_application.cc` | `gtk_header_bar_set_title` + `gtk_window_set_title` |
| Android | `android/app/src/main/AndroidManifest.xml` | `android:label` |
| iOS | `ios/Runner/Info.plist` | `CFBundleDisplayName` + `CFBundleName` |

### 打包产物名
`pubspec.yaml` 的 `name` 字段决定 Dart 包名和 Linux 构建产物名：
- `name: qtconsult_studio` → 产物 `build/linux/x64/release/bundle/qtconsult-studio`
- 若项目目录名为 `studio`，产物名为 `studio`（不推荐，与包名不一致）

## 录制演示视频

使用 `scripts/record-studio-linux.sh`：

```bash
# 构建
cd src/studio && flutter build linux

# 录制（自动启动 App → 调整窗口 → 交互 → 结束）
bash scripts/record-studio-linux.sh
```

依赖：`xdotool` + `ffmpeg`。坐标基于 1440×900 窗口，如需调整需同步修改 `click` 坐标。

## 常见问题

- **dart analyze 零警告**：提交前必须运行
- **JSON 数据变更后需重跑 `flutter build`**：assets 不会热重载
- **窗口标题搜不到**：检查 `my_application.cc` 中的字符串，中文需用 UTF-8
- **录制时 BadWindow 错误**：xdotool windowsize 在某些 WM 下失效，加 `2>/dev/null || true`
