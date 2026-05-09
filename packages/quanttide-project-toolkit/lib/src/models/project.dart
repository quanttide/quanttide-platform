import 'package:freezed_annotation/freezed_annotation.dart';

part 'project.freezed.dart';
part 'project.g.dart';


@unfreezed
class Project with _$Project {
  factory Project({
    required final String id,
    required final String name,
    required final DateTime createdAt,
    required DateTime updatedAt,
    String? verboseName,
    String? readme,
    @Default('drafting') String status,
    @Default('low') String priority,
  }) = _Project;

  factory Project.fromJson(Map<String, dynamic> json) => _$ProjectFromJson(json);
}
