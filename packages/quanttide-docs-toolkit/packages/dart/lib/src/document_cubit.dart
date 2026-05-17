import 'dart:convert';
import 'dart:io';

import 'package:bloc/bloc.dart';

typedef DocumentState = ({String content});

class DocumentCubit extends Cubit<DocumentState> {
  DocumentCubit() : super((content: ''));

  factory DocumentCubit.fromFile(String path) {
    final cubit = DocumentCubit();
    final file = File(path);
    cubit.emit((content: file.readAsStringSync()));
    return cubit;
  }

  factory DocumentCubit.fromAgent(Map<String, dynamic> config) {
    final cubit = DocumentCubit();
    final content = config['content'] as String? ?? '';
    cubit.emit((content: content));
    return cubit;
  }

  factory DocumentCubit.fromEditor(String initialContent) {
    final cubit = DocumentCubit();
    cubit.emit((content: initialContent));
    return cubit;
  }

  void updateContent(String newContent) {
    emit((content: newContent));
  }
}
