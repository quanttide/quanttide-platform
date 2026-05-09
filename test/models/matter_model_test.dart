import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_quanttide_projects/flutter_quanttide_projects.dart';


void main() {
  group('Matter', () {
    test('Create Matter object', () {
      final matter = Matter(
        id: '1',
        number: 2,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        title: 'Sample Matter',
        description: 'This is a sample matter',
        priority: 'high',
        status: 'in progress',
        type: 'custom',
      );

      expect(matter.id, '1');
      expect(matter.number, 2);
      expect(matter.createdAt, isA<DateTime>());
      expect(matter.updatedAt, isA<DateTime>());
      expect(matter.title, 'Sample Matter');
      expect(matter.description, 'This is a sample matter');
      expect(matter.priority, 'high');
      expect(matter.status, 'in progress');
      expect(matter.type, 'custom');
    });

    test('Serialize to JSON', () {
      final matter = Matter(
        id: '1',
        number: 2,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
        title: 'Sample Matter',
        description: 'This is a sample matter',
        priority: 'high',
        status: 'in progress',
        type: 'custom',
      );

      final json = matter.toJson();

      expect(json['id'], '1');
      expect(json['number'], 2);
      expect(json['createdAt'], isA<String>());
      expect(json['updatedAt'], isA<String>());
      expect(json['title'], 'Sample Matter');
      expect(json['description'], 'This is a sample matter');
      expect(json['priority'], 'high');
      expect(json['status'], 'in progress');
      expect(json['type'], 'custom');
    });

    test('Deserialize from JSON', () {
      final json = {
        'id': '1',
        'number': 2,
        'createdAt': '2022-01-01T10:00:00Z',
        'updatedAt': '2022-01-02T15:30:00Z',
        'title': 'Sample Matter',
        'description': 'This is a sample matter',
        'priority': 'high',
        'status': 'in progress',
        'type': 'custom',
      };

      final matter = Matter.fromJson(json);

      expect(matter.id, '1');
      expect(matter.number, 2);
      expect(matter.createdAt, isA<DateTime>());
      expect(matter.updatedAt, isA<DateTime>());
      expect(matter.title, 'Sample Matter');
      expect(matter.description, 'This is a sample matter');
      expect(matter.priority, 'high');
      expect(matter.status, 'in progress');
      expect(matter.type, 'custom');
    });
  });
}