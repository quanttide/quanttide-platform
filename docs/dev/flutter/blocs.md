# Bloc 架构定义

## 1. Bloc 术语与 DDD 术语的对应

| Bloc 框架用词 | 输入/输出 | 开发者日常理解 | DDD 类比 |
|---------------|-----------|---------------|----------|
| `Event` | 输入 | "外界想做的事" | Command（命令） |
| `State` | 输出 | "发生了什么" | Domain Event（领域事件，概念类比） |

Flutter Bloc 框架用 `Event` 和 `State` 命名泛型参数。这两个词在日常用语中有歧义：

- **`Event` 作为输入**：日常用语中"事件"往往表示"已经发生的事"，但 Bloc 的输入实际上是"外界想做什么"——更像是命令而非事件。使用时把它理解成"命令"即可。
- **`State` 作为输出**：日常用语中"状态"暗示静态快照，但实际使用时输出类型常被命名为过去时（如 `PipelineDisplayed`），更像"已发生的事实"。使用时把它理解成"事实"即可。

代码中仍使用 Bloc 框架原生的 `Event`/`State`，不做重命名。


## 2. Bloc 命名风格及含义

### 输入输出模型

Bloc 是一个函数：输入是 Event（命令），输出是 State（事实）。

```
UI ──Event──→ Bloc ──State──→ UI
```

Event 是"请做某事"，不保证执行——可能被校验拒绝、被权限拦截。State 是"发生了什么"，UI 据此渲染。

### Event（输入）的命名

输入使用**祈使句**，表达"请做某事"：

```
ShowPipeline, RefreshPipeline, SubmitTask
```

Event 可以携带参数（如 `pipelineId`），但参数是"请求"而非"结果"。

### State（输出）的命名

输出使用**过去时或进行时**，表达"发生了什么"：

```
PipelineDisplaying, PipelineDisplayed, PipelineDisplayFailed
```

每个操作定义对应的三个 State，UI 层通过 `switch` 穷举——编译器强制处理所有情况：

| 时序 | State | 含义 | UI 层行为 |
|------|-------|------|----------|
| 开始时 | `Displaying` | 正在进行中 | 显示加载指示器 |
| 成功时 | `Displayed` | 已完成 | 展示数据 |
| 失败时 | `DisplayFailed` | 已失败 | 展示错误信息 |

即使当前实现是同步的也要定义全部三个。原因：未来改为异步时不需要修改 State 类型，只需改 handler 内部逻辑。

三态的开销极低（几行代码），而漏掉 loading/error 状态的代价很高。

## 3. 场景讨论：什么时候用三态

### 三态的意义

定义三态不是为了异步兼容（那是附带效果），而是把操作的生命周期写进类型系统。

sealed class + switch 穷举意味着：新增一个状态时编译器会提示所有未处理的 case，不会遗漏 loading 或 error。如果不定义三态，loading 和 error 就只能靠开发者记忆——有人用 boolean 标记、有人用 nullable、有人干脆不处理，每种方式都是运行时隐患。

将状态显式定义出来，UI 层就是一个无可争议的 switch：所有可能的情况都列在代码里，编译器替你保障完整性，不需要靠 Code Review 来补漏。

### 必须用三态的场景

操作具有等待阶段，且失败是可预期的 UI 反馈：

- 网络请求（获取列表、提交表单）
- 文件读写
- 数据库查询
- 异步验证（检查用户名是否可用）

这类操作天然有 loading → success / error 三阶段，三态是直接映射。


### 不需要三态的场景

没有等待阶段的操作，三态中的 "ing" 态没有实际意义：

- **同步计算**（校验、数据转换、纯函数）——没有 loading 阶段，失败是异常而非状态
- **纯 UI 交互**（切换 tab、展开折叠、选中/取消）——用户直接操作即时响应，不存在"进行中"
- **同步缓存读取**（从内存 Map 取值）——命中即返回，不命中属于逻辑错误而非等待

这类操作只需要零态（事件本身即结果）或两态（成功 + 带错误信息的失败），不需要虚构 loading 态。

### 判断方法

**是否有等待阶段？**

- 是 → 三态（Displaying / Displayed / DisplayFailed）
- 否 → 一态（事件本身已是结果）或两态（成功数据 / 错误信息）

注意：等待不一定来自异步 I/O。需要用户确认的交互（弹窗确认后再执行）也有等待阶段，只是等待的并非 IO 而是用户决策。

## 4. Bloc 实现细节

### 完整示例

```dart
// ── Event（输入）──

sealed class PipelineEvent {}

class ShowPipeline extends PipelineEvent {
  final String pipelineId;
  ShowPipeline(this.pipelineId);
}

// ── State（输出）──

sealed class PipelineState {}

class PipelineDisplaying extends PipelineState {}
class PipelineDisplayed extends PipelineState {
  final Pipeline pipeline;
  PipelineDisplayed(this.pipeline);
}
class PipelineDisplayFailed extends PipelineState {
  final String error;
  PipelineDisplayFailed(this.error);
}

// ── Bloc ──

class PipelineBloc extends Bloc<PipelineEvent, PipelineState> {
  PipelineBloc() : super(PipelineDisplaying()) {
    on<ShowPipeline>(_onShowPipeline);
  }

  Future<void> _onShowPipeline(
    ShowPipeline event,
    Emitter<PipelineState> emit,
  ) async {
    emit(PipelineDisplaying());
    try {
      final pipeline = await repository.fetch(event.pipelineId);
      emit(PipelineDisplayed(pipeline));
    } catch (e) {
      emit(PipelineDisplayFailed(e.toString()));
    }
  }
}
```

UI 层消费：

```dart
builder: (context, state) {
  return switch (state) {
    PipelineDisplaying() => LoadingIndicator(),
    PipelineDisplayed(:final pipeline) => PipelineView(pipeline: pipeline),
    PipelineDisplayFailed(:final error) => ErrorView(error: error),
  };
}
```
