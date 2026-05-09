import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_quanttide_projects/flutter_quanttide_projects.dart';


void main() {
  group('MatterEvent', () {
    test('MatterRetrieved event', () {
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

      final event = MatterRetrieved(matter);

      expect(event.matter, matter);
    });

    test('MatterListed event', () {
      final matters = [
        Matter(
          id: '1',
          number: 2,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
          title: 'Sample Matter 1',
          description: 'This is a sample matter 1',
          priority: 'high',
          status: 'in progress',
          type: 'custom',
        ),
        Matter(
          id: '2',
          number: 3,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
          title: 'Sample Matter 2',
          description: 'This is a sample matter 2',
          priority: 'low',
          status: 'completed',
          type: 'default',
        ),
      ];

      final event = MatterListed(matters);

      expect(event.matters, matters);
    });

    test('MatterCreated event', () {
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

      final event = MatterCreated(matter);

      expect(event.matter, matter);
    });

    test('MatterUpdated event', () {
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

      final event = MatterUpdated(matter);

      expect(event.matter, matter);
    });

    test('MatterPartialUpdated event', () {
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

      final event = MatterPartialUpdated(matter);

      expect(event.matter, matter);
    });

    test('MatterAssigned event', () {
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

      final event = MatterAssigned(matter);

      expect(event.matter, matter);
    });

    test('MatterDestroyed event', () {
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

      final event = MatterDestroyed(matter);

      expect(event.matter, matter);
    });
  });
}