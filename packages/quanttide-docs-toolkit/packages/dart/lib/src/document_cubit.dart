import 'package:bloc/bloc.dart';
import 'document_repository.dart';

class DocumentCubit extends Cubit<String> {
  final DocumentRepository _repository;

  DocumentCubit({
    required DocumentRepository repository,
  })  : _repository = repository,
        super('');

  Future<void> fromFile(String path) async {
    final content = await _repository.readFrom(path);
    emit(content);
  }

  void fromEditor(String content) {
    emit(content);
    _repository.write(content);
  }

  void fromAgent(String content) {
    emit(content);
    _repository.write(content);
  }
}
