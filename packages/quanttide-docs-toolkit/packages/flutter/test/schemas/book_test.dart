import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_quanttide_docs/flutter_quanttide_docs.dart';


void main() {
  group('Book', () {
    test('fromJson creates a Book object from valid JSON', () {
      final json = {
        'id': '1',
        'name': 'Book 1',
        'title': 'Document 1',
        'description': 'Description 1',
      };

      final book = Book.fromJson(json);

      expect(book.id, '1');
      expect(book.name, 'Book 1');
      expect(book.title, 'Document 1');
      expect(book.description, 'Description 1');
    });

    test('toJson converts a Book object to JSON', () {
      final book = Book(
        id: '1',
        name: 'Book 1',
        title: 'Document 1',
        description: 'Description 1',
      );

      final json = book.toJson();

      expect(json['id'], '1');
      expect(json['name'], 'Book 1');
      expect(json['title'], 'Document 1');
      expect(json['description'], 'Description 1');
    });
  });
}
