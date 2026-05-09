// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'matter.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#custom-getters-and-methods');

Matter _$MatterFromJson(Map<String, dynamic> json) {
  return _Matter.fromJson(json);
}

/// @nodoc
mixin _$Matter {
  String get id => throw _privateConstructorUsedError;
  int get number => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime get updatedAt => throw _privateConstructorUsedError;
  set updatedAt(DateTime value) => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  set title(String value) => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  set description(String value) => throw _privateConstructorUsedError;
  String get priority => throw _privateConstructorUsedError;
  set priority(String value) => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  set status(String value) => throw _privateConstructorUsedError;
  String get type => throw _privateConstructorUsedError;
  set type(String value) => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $MatterCopyWith<Matter> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $MatterCopyWith<$Res> {
  factory $MatterCopyWith(Matter value, $Res Function(Matter) then) =
      _$MatterCopyWithImpl<$Res, Matter>;
  @useResult
  $Res call(
      {String id,
      int number,
      DateTime createdAt,
      DateTime updatedAt,
      String title,
      String description,
      String priority,
      String status,
      String type});
}

/// @nodoc
class _$MatterCopyWithImpl<$Res, $Val extends Matter>
    implements $MatterCopyWith<$Res> {
  _$MatterCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? number = null,
    Object? createdAt = null,
    Object? updatedAt = null,
    Object? title = null,
    Object? description = null,
    Object? priority = null,
    Object? status = null,
    Object? type = null,
  }) {
    return _then(_value.copyWith(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as String,
      number: null == number
          ? _value.number
          : number // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      type: null == type
          ? _value.type
          : type // ignore: cast_nullable_to_non_nullable
              as String,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$_MatterCopyWith<$Res> implements $MatterCopyWith<$Res> {
  factory _$$_MatterCopyWith(_$_Matter value, $Res Function(_$_Matter) then) =
      __$$_MatterCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String id,
      int number,
      DateTime createdAt,
      DateTime updatedAt,
      String title,
      String description,
      String priority,
      String status,
      String type});
}

/// @nodoc
class __$$_MatterCopyWithImpl<$Res>
    extends _$MatterCopyWithImpl<$Res, _$_Matter>
    implements _$$_MatterCopyWith<$Res> {
  __$$_MatterCopyWithImpl(_$_Matter _value, $Res Function(_$_Matter) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? number = null,
    Object? createdAt = null,
    Object? updatedAt = null,
    Object? title = null,
    Object? description = null,
    Object? priority = null,
    Object? status = null,
    Object? type = null,
  }) {
    return _then(_$_Matter(
      id: null == id
          ? _value.id
          : id // ignore: cast_nullable_to_non_nullable
              as String,
      number: null == number
          ? _value.number
          : number // ignore: cast_nullable_to_non_nullable
              as int,
      createdAt: null == createdAt
          ? _value.createdAt
          : createdAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      updatedAt: null == updatedAt
          ? _value.updatedAt
          : updatedAt // ignore: cast_nullable_to_non_nullable
              as DateTime,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      priority: null == priority
          ? _value.priority
          : priority // ignore: cast_nullable_to_non_nullable
              as String,
      status: null == status
          ? _value.status
          : status // ignore: cast_nullable_to_non_nullable
              as String,
      type: null == type
          ? _value.type
          : type // ignore: cast_nullable_to_non_nullable
              as String,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$_Matter implements _Matter {
  _$_Matter(
      {required this.id,
      required this.number,
      required this.createdAt,
      required this.updatedAt,
      this.title = '',
      this.description = '',
      this.priority = 'low',
      this.status = 'drafting',
      this.type = 'default'});

  factory _$_Matter.fromJson(Map<String, dynamic> json) =>
      _$$_MatterFromJson(json);

  @override
  final String id;
  @override
  final int number;
  @override
  final DateTime createdAt;
  @override
  DateTime updatedAt;
  @override
  @JsonKey()
  String title;
  @override
  @JsonKey()
  String description;
  @override
  @JsonKey()
  String priority;
  @override
  @JsonKey()
  String status;
  @override
  @JsonKey()
  String type;

  @override
  String toString() {
    return 'Matter(id: $id, number: $number, createdAt: $createdAt, updatedAt: $updatedAt, title: $title, description: $description, priority: $priority, status: $status, type: $type)';
  }

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$_MatterCopyWith<_$_Matter> get copyWith =>
      __$$_MatterCopyWithImpl<_$_Matter>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$_MatterToJson(
      this,
    );
  }
}

abstract class _Matter implements Matter {
  factory _Matter(
      {required final String id,
      required final int number,
      required final DateTime createdAt,
      required DateTime updatedAt,
      String title,
      String description,
      String priority,
      String status,
      String type}) = _$_Matter;

  factory _Matter.fromJson(Map<String, dynamic> json) = _$_Matter.fromJson;

  @override
  String get id;
  @override
  int get number;
  @override
  DateTime get createdAt;
  @override
  DateTime get updatedAt;
  set updatedAt(DateTime value);
  @override
  String get title;
  set title(String value);
  @override
  String get description;
  set description(String value);
  @override
  String get priority;
  set priority(String value);
  @override
  String get status;
  set status(String value);
  @override
  String get type;
  set type(String value);
  @override
  @JsonKey(ignore: true)
  _$$_MatterCopyWith<_$_Matter> get copyWith =>
      throw _privateConstructorUsedError;
}
