# Bloc 架构定义

## 概念分层

Bloc 的输入侧和输出侧分属不同概念层级，不应混用一个类型体系。

### 输入侧：Command（意图）

表达"外界想做什么"。来自 UI 或外部调用方，是命令式的——带有方向性，不承诺结果。

- 命令的命名使用**祈使句**：`ShowPipeline`、`RefreshPipeline`、`SubmitTask`
- 命令可以携带执行所需的参数
- Bloc 收到命令后**不保证**它能被执行——可能被校验拒绝、可能被权限拦截

### 输出侧：Domain Event（事实）

表达"系统发生了什么"。来自 Bloc 内部，是声明式的——系统已发生事实的记录。

- 领域事件的命名使用**过去时或进行时**：`PipelineDisplayed`、`PipelineDisplayFailed`、`PipelineLoading`
- 事件是 Bloc 对外界的单向通知
- 事件携带的数据是**结果**而非请求

### 关系

```
UI ──Command──→ Bloc ──Domain Event──→ UI
```

UI 发送命令，Bloc 根据业务逻辑产出领域事件，UI 根据领域事件渲染。

---

## 示例定义

以 pipeline 展示为例：

```dart
// ── 命令（输入侧）──

sealed class PipelineCommand {}

class ShowPipeline extends PipelineCommand {
  final Pipeline pipeline;

  ShowPipeline(this.pipeline);
}

// ── 领域事件（输出侧）──

sealed class PipelineEvent {}

class PipelineDisplaying extends PipelineEvent {}
class PipelineDisplayed extends PipelineEvent {
  final Pipeline pipeline;

  PipelineDisplayed(this.pipeline);
}
class PipelineDisplayFailed extends PipelineEvent {
  final String error;

  PipelineDisplayFailed(this.error);
}
```

### 三态覆盖

即使当前实现是同步的（`ShowPipeline` 发生后立即 `Displayed`），也定义完整的三个事件：

- `Displaying` — "开始展示"，UI 可用于显示 loading 指示器
- `Displayed` — "展示成功"，携带数据
- `DisplayFailed` — "展示失败"，携带错误信息

定义三态的意义：当前 handler 是同步的 `void`，未来改为异步 `Future<void>` 时不需要修改状态契约，只需要在 handler 体内插入 await 和 try-catch。

```dart
class PipelineBloc extends Bloc<PipelineCommand, PipelineEvent> {
  PipelineBloc() : super(PipelineDisplaying()) {
    on<ShowPipeline>(_onShowPipeline);
  }

  void _onShowPipeline(ShowPipeline event, Emitter<PipelineEvent> emit) {
    emit(PipelineDisplayed(event.pipeline));
  }
}
```

未来异步版本仅 handler 内部变化：

```dart
Future<void> _onShowPipeline(ShowPipeline event, Emitter<PipelineEvent> emit) async {
  emit(PipelineDisplaying());
  try {
    final pipeline = await repository.fetch(event.pipelineId);
    emit(PipelineDisplayed(pipeline));
  } catch (e) {
    emit(PipelineDisplayFailed(e.toString()));
  }
}
```

三态在 UI 层通过 `switch` 穷举被编译器强制处理所有情况，不会遗漏 loading 和 error。
