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
  flutter_bloc: ^9.1.0
  freezed_annotation: ^3.1.0
  json_annotation: ^4.11.0
  go_router: ^14.0.0

dev_dependencies:
  freezed: ^3.2.5
  build_runner: ^2.4.6
  json_serializable: ^6.9.0

flutter:
  assets:
    - assets/<data>.json
```

必须添加的依赖：
- `flutter_bloc`：状态管理（替代 provider）
- `freezed_annotation` + `freezed` + `build_runner` + `json_serializable`：数据模型代码生成
- `go_router`：URL 路由
- `assets/`：数据源 JSON 文件

### 3. 搭建目录结构

```
lib/
  main.dart             # 入口 + BlocProvider
  router.dart           # RouteConfig + GoRouter + buildScreen
  theme.dart            # 颜色工具
  constants.dart        # UI 映射常量
  models/               # freezed 数据模型
  sources/              # 数据源抽象（base/file_source/bundle_source）
  blocs/                # BLoC 状态管理
  screens/              # 页面级组件
  views/                # 可复用 UI 组件
test/
  models/               # 模型单元测试
  sources/              # 数据源测试
  blocs/                # BLoC 状态管理测试
  views/                # Widget 测试
  screens/              # 页面级组件测试
```

数据源按来源类型分（base/file/bundle），不按模型分。`theme.dart` 和 `constants.dart` 直接放在 `lib/` 根目录。

#### 数据层架构

替代原始方案以规避以下问题：

- **不用每模型一个 Loader** — 6 个 loader 大量重复，新增模型需完整复制粘贴
- **不用散落 try-catch 处理异常** — 无统一错误类型，调用方遗漏处理导致运行时崩溃
- **不用 FileSource 为唯一实现** — Web 无 `dart:io`，直接文件 I/O 导致平台锁死

改用三层抽象：

```dart
sealed class DataResult<T> { const DataResult(); }
class DataSuccess<T> extends DataResult<T> {
  final T data;
  const DataSuccess(this.data);
}
class DataError<T> extends DataResult<T> {
  final String message; final Object? error;
  const DataError(this.message, {this.error});
}

abstract class DataSource {
  Future<String> load(String path);
}

class DataLoader<T> {
  final DataSource source;
  final String path;
  final T Function(Map<String, dynamic>) fromJson;
  const DataLoader(this.source, this.path, this.fromJson);
  Future<DataResult<T>> load() async { /* ... */ }
}
```

默认使用 `BundleSource`（基于 `rootBundle`，跨所有平台包括 Web），避免 `FileSource`（依赖 `dart:io`，Web 不可用）。

#### 路由架构

替代原始方案以规避以下问题：

- **不用 `buildScreen` 字符串 switch** — routeId→screen 双重映射，新增页面需改两处，遗漏则不生效
- **不用 ShellRoute 内嵌 AppState 判断** — 每个子路由手动检查权限，新增路由易遗漏导航守卫
- **不用各自拆解 raw JSON 传参** — 6 处重复 `json['params']` 拆解逻辑，字段名不一致导致隐蔽 bug

改用以下模式：

- **redirect-based GoRouter** — `redirect` 回调统一管理 AppLifecycle 和权限校验
- **`Map<String, RouteConfig>` 路由表** — 自包含，消除双重映射
- **`ScreenContext` 单 source 传参** — builder callback 统一解析 screen 参数

```dart
const routeConfigs = <String, RouteConfig>{
  'projects': RouteConfig(path: '/projects', title: '项目'),
};
```

### 4. 设计数据模型

使用 freezed 生成 `fromJson` / `copyWith` / `==` / `hashCode`。

```dart
@freezed
class Lesson with _$Lesson {
  const factory Lesson({
    required String id,
    required String title,
    @Default('') String description,
  }) = _Lesson;

  factory Lesson.fromJson(Map<String, dynamic> json) =>
      _$LessonFromJson(json);
}
```

编写后运行 `dart run build_runner build` 生成 `.freezed.dart` 和 `.g.dart`。

关键实践：
- 字段默认值用 `@Default`，枚举 fallback 用 `@JsonKey(fromJson:)`
- 自定义 getter/method 写成 `extension XxxX on Xxx`，不在 freezed 类里直接写
- 模型文件只放 freezed 类。颜色/图标/标签映射函数放在 `constants.dart`

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
  sources/             # 数据源/数据加载器测试
  blocs/
  views/             # Widget 测试，与 lib/screens/ + lib/views/ 一一对应
  screens/             # Widget 测试，与 lib/screens/ + lib/views/ 一一对应
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

Service 测试模式：用 `inject()` 或 `BlocProvider.value` 注入数据，不加载真实 JSON 文件。

```dart
// sources 测试：用 MockSource 注入
final source = _MockSource('{"id": "l1"}');
final loader = DataLoader<Lesson>(source, 'test.json', Lesson.fromJson);
final result = await loader.load();
expect((result as DataSuccess).data.id, 'l1');
```

```dart
// BLoC 测试：直接设置初始状态
final bloc = LessonBloc(LessonState(data: initialData));
bloc.add(UpdateTitle('new'));
await pumpEventQueue();
expect(bloc.state.data.title, 'new');
```

```dart
// Widget 测试：用 BlocProvider.value 注入
Widget createTest(LessonBloc bloc) {
  return MaterialApp(
    home: BlocProvider.value(
      value: bloc,
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
- 使用 `BlocProvider.value` 注入 BLoC 实例
- 不调用真实的 `load()` 方法（依赖文件 I/O）
- 用 `addTearDown` 重置 view 参数，避免影响后续测试
- 使用 `pumpAndSettle()` 等待动画完成
- 先测试空状态，再测试有数据状态
- BLoC 事件测试需 `await pumpEventQueue()` 等待异步处理

### 7. 验证构建

```bash
cd src/<project>
dart analyze lib/ test/
flutter test
dart run build_runner build   # freezed 模型变更后
flutter build linux
```

必须满足：
- `dart analyze lib/ test/` 零报错
- `flutter test` 全部通过
- `flutter build linux` 构建成功

> **注意**：pre-commit hook 仅运行 `dart analyze`，不包含 `flutter test`（非交互式 shell 中不稳定）。本地开发仍需以完整验证为目标。

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
