import 'package:quanttide_docs/quanttide_docs.dart';
import 'package:test/test.dart';

class FakeRepository implements DocumentRepository {
  String? lastWritten;
  String? fileContent;
  String? lastReadPath;

  @override
  Future<String> read() async => fileContent ?? '';

  @override
  Future<String> readFrom(String path) async {
    lastReadPath = path;
    return fileContent ?? 'file content from $path';
  }

  @override
  Future<void> write(String content) async {
    lastWritten = content;
  }

  @override
  Stream<String> watch() => const Stream.empty();

  @override
  Future<void> dispose() async {}
}

void main() {
  group('DocumentCubit', () {
    test('starts with empty content', () {
      final cubit = DocumentCubit(repository: FakeRepository());
      expect(cubit.state, '');
    });

    test('fromFile reads from repository and emits content', () async {
      final repo = FakeRepository();
      repo.fileContent = 'file text';
      final cubit = DocumentCubit(repository: repo);
      await cubit.fromFile('/path/to/doc.md');
      expect(cubit.state, 'file text');
      expect(repo.lastReadPath, '/path/to/doc.md');
    });

    test('fromEditor emits content and persists', () {
      final repo = FakeRepository();
      final cubit = DocumentCubit(repository: repo);
      cubit.fromEditor('Editor content');
      expect(cubit.state, 'Editor content');
      expect(repo.lastWritten, 'Editor content');
    });

    test('fromAgent emits content and persists', () {
      final repo = FakeRepository();
      final cubit = DocumentCubit(repository: repo);
      cubit.fromAgent('Agent content');
      expect(cubit.state, 'Agent content');
      expect(repo.lastWritten, 'Agent content');
    });
  });
}
