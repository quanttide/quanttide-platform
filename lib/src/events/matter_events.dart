/// 事项领域事件

import '../models/matter.dart';


/// 抽象类，表示 `Matter` 详情页面的事件
sealed class MatterEvent {}

/// 获取详情事件，表示获取 `Matter` 详情
class MatterRetrieved extends MatterEvent {
  final Matter matter;

  MatterRetrieved(this.matter);
}

/// 获取详情事件，表示获取 `Matter` 详情
class MatterListed extends MatterEvent {
  final List<Matter> matters;
  MatterListed(this.matters);
}

/// 已创建事件，表示成功创建了新的 `Matter`
class MatterCreated extends MatterEvent {
  final Matter matter;

  MatterCreated(this.matter);
}

/// 已更新事件，表示成功更新了现有的 `Matter`
class MatterUpdated extends MatterEvent {
  final Matter matter;

  MatterUpdated(this.matter);
}


/// 已部分更新事件，表示成功部分更新了现有的 `Matter`
class MatterPartialUpdated extends MatterEvent {
  final Matter matter;
  MatterPartialUpdated(this.matter);
}

/// 已分配事件，表示成功分配了 `Matter` 到负责人
class MatterAssigned extends MatterPartialUpdated {
  MatterAssigned(Matter matter) : super(matter);
}

/// 已删除事件，表示成功删除了现有的 `Matter`
class MatterDestroyed extends MatterEvent {
  final Matter matter;

  MatterDestroyed(this.matter);
}