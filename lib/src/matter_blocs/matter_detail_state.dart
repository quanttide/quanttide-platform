/// 事项详情状态

import 'package:equatable/equatable.dart';


enum MatterDetailStatus { initial, loading, success, error }


final class MatterDetailState extends Equatable {
  final MatterDetailStatus status;
  const MatterDetailState({this.status = MatterDetailStatus.initial});

  @override
  List<Object?> get props => [status];
}
