# Dart & Flutter 包开发经验

## 发布策略

### 先发纯 Dart 包，后发 Flutter 包

Dart 包编译更快、CI 成本更低。如果领域模型不需要 `BuildContext`，就不要让它依赖 Flutter SDK。

### Flutter 包可独立于 Dart 包发布

即使逻辑上相关，也无需在 pubspec 中强依赖。`flutter_quanttide_project` 不依赖 `quanttide_project`，因为其组件只取 Widget 插槽，不取数据模型。

### 发布前检查清单

`dart pub publish --dry-run` → 确认 LICENSE → `dart pub publish`。`publish_to: none` 的包不会被发布，发布前检查 pubspec。包名、homepage、repository、issue_tracker 提前填好。

## 数据模型设计

### 平面 List 优于嵌套树结构

旧结构 `Board(BoardList(BoardCard))` 三层嵌套。代码路径是 `project.board.lists[i].cards[j]`——必须先拿到 `Project`，再访问 `.board`，再从 `.board` 找到某个 `list`，再从 `list` 找某个 `card`。新增 filter（如"只看 observe 阶段的任务"）需要遍历 `board.lists` 再遍历 `list.cards`，或者写新的 getter 钻进嵌套。

新结构 `List<Task>`。`tasks.where((t) => t.type == 'observe').toList()`。数据在哪层，算法就在哪层——不需要理解嵌套结构内部的层级关系。filter、sort、group by 全是标准 list 操作，与业务语义解耦。

嵌套树的唯一优势是保留父→子层级语义。但如果"属于哪个层级"只是节点的一个可变属性（如 `Task.type` 决定 OODA 阶段，且任务可在阶段间移动），用树结构强行表达这种关系反而是失真。

**判断标准**：我真的需要树的操作语义（深度优先遍历、子树升降级）吗？还是只需要根据某些属性做查询和分组？

不确定是否需要树时，先用 `List`。发现确实需要树语义时再加嵌套，比一开始就选嵌套然后发现不需要简单得多。

### Map<String, String> 与显式字段的选择

字段未稳定时，用 `tags` map 比定义大量 `String?` 字段更抗变化——改 key 名不涉及构造函数签名变更。代价是丢失编译期检查。选哪边取决于对字段稳定性的信心。

## 跨包修改原则

### 一次性跨层修改比分步迁移更高效

前提是对改动范围有清晰认知。"先改模型不动 UI，再改 UI"会产生中间态技术债务。Flutter 的编译期检查让一次性切完更加可行。

### 提交顺序：domain → adapter → app

但放在同一个 commit 里。如需分步，每步必须编译通过。

## 测试

### Flutter 业务库测试模式

`provider` + `Consumer` widget 可通过 `pumpWidget` + 注入 mock 状态完成，不需要启动真实后端。
