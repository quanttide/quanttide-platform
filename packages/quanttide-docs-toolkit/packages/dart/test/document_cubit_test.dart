import 'package:quanttide_docs/quanttide_docs.dart';
import 'package:test/test.dart';

void main() {
  group('DocumentCubit', () {
    test('fromEditor creates cubit with initial content', () {
      final cubit = DocumentCubit.fromEditor('Hello');
      expect(cubit.state.content, 'Hello');
    });

    test('updateContent emits new state', () {
      final cubit = DocumentCubit.fromEditor('');
      cubit.updateContent('Updated');
      expect(cubit.state.content, 'Updated');
    });

    test('default state has empty content', () {
      final cubit = DocumentCubit();
      expect(cubit.state.content, '');
    });

    test('fromAgent uses content from config', () {
      final cubit = DocumentCubit.fromAgent({'content': 'Agent content'});
      expect(cubit.state.content, 'Agent content');
    });

    test('fromAgent defaults to empty content when no config key', () {
      final cubit = DocumentCubit.fromAgent({});
      expect(cubit.state.content, '');
    });
  });
}
