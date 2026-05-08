---
name: product-studio
description: Flutter Studio 客户端开发流程。从需求到发布，覆盖项目初始化、数据模型、UI 开发、构建、提交的完整工作流。
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
- `--project-name`: 包名，也是 Linux 产物名（如 `qtconsult_studio`）
- `--org`: Android 包名前缀
- `--platforms`: 目标平台列表

### 2. 配置 pubspec.yaml

```yaml
name: qtconsult_studio
description: <描述>

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
```

### 4. 设计数据模型

每条模型必须包含：
- `const` 构造函数
- `factory fromJson(Map<String, dynamic>)` 工厂方法
- `copyWith` 方法（可选）
- 关联的枚举类型

### 5. 修改应用显示名称

Flutter 默认用项目目录名作为应用名称，需手动修改以下文件：

| 平台 | 文件 | 修改内容 |
|------|------|---------|
| Linux | `linux/runner/my_application.cc` | `gtk_header_bar_set_title` 和 `gtk_window_set_title` |
| Android | `android/app/src/main/AndroidManifest.xml` | `android:label` |
| iOS | `ios/Runner/Info.plist` | `CFBundleDisplayName` 和 `CFBundleName` |

### 6. 编写测试

#### 目录结构

```
test/
  models/              # 模型单元测试，与 lib/models/ 一一对应
  screens/             # Widget 测试，与 lib/screens/ 一一对应
  widget_test.dart     # App 冒烟测试
```

#### 模型测试

每条模型的 fromJson、copyWith 和关联枚举都需要测试：

```dart
group('Lesson', () {
  test('fromJson parses all fields', () {
    final lesson = Lesson.fromJson({'id': 'l1', 'title': 'T'});
    expect(lesson.id, 'l1');
  });

  test('copyWith overrides specified fields', () {
    final copy = lesson.copyWith(title: 'new');
    expect(copy.title, 'new');
    expect(copy.id, lesson.id);
  });
});
```

测试要点：
- 全字段 JSON 解析
- 缺失字段使用默认值
- `copyWith` 覆盖指定字段、保持未指定字段

#### 枚举测试

```dart
test('fromString returns published for "published"', () {
  expect(ContentStatus.fromString('published'), ContentStatus.published);
});
test('fromString returns draft for unknown value', () {
  expect(ContentStatus.fromString(''), ContentStatus.draft);
});
test('label returns Chinese', () {
  expect(ContentStatus.draft.label, '草稿');
});
```

#### Widget 测试

Service 测试模式：提前注入数据，不加载真实 JSON 文件。

```dart
final service = CourseDataService();
service.programs.addAll([...]);
service.markLoaded();
```

提供者模式：

```dart
Widget createTest(CourseDataService service) {
  return MaterialApp(
    home: ChangeNotifierProvider.value(
      value: service,
      child: const MyScreen(),
    ),
  );
}
```

设置测试视口：

```dart
testWidgets('description', (tester) async {
  tester.view.physicalSize = const Size(1280, 800);
  tester.view.devicePixelRatio = 1.0;
  addTearDown(() {
    tester.view.resetPhysicalSize();
    tester.view.resetDevicePixelRatio();
  });
});
```

Widget 测试要点：
- 使用 `ChangeNotifierProvider.value` 而非 `ChangeNotifierProvider.create`
- 不调用 `service.load()`（它依赖 rootBundle 加载真实文件）
- 用 `addTearDown` 重置 view 参数，避免影响后续测试
- 使用 `pumpAndSettle()` 等待动画完成
- 先测试空状态，再测试有数据状态

#### 服务层辅助方法

`CourseDataService` 需要暴露 `markLoaded()` 方法用于测试：

```dart
class CourseDataService extends ChangeNotifier {
  bool _loaded = false;
  void markLoaded() {
    _loaded = true;
    notifyListeners();
  }
}
```

这避免了在测试中依赖 `rootBundle.loadString` 加载真实 JSON 文件。

### 7. 验证构建

```bash
cd src/<project>
dart analyze lib/
flutter test
flutter build linux
```

必须满足：
- `dart analyze lib/` 零报错
- `flutter test` 全部通过
- `flutter build linux` 构建成功

### 8. 提交流程

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
