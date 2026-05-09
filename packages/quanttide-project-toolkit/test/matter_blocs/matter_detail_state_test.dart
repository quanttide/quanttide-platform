import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_quanttide_projects/flutter_quanttide_projects.dart';


void main() {
  group('MatterDetailState', () {
    test('Default status is initial', () {
      const state = MatterDetailState();

      expect(state.status, MatterDetailStatus.initial);
    });

    test('Status is set correctly', () {
      const state = MatterDetailState(status: MatterDetailStatus.loading);

      expect(state.status, MatterDetailStatus.loading);
    });

    test('Equality testing', () {
      const state1 = MatterDetailState(status: MatterDetailStatus.success);
      const state2 = MatterDetailState(status: MatterDetailStatus.success);
      const state3 = MatterDetailState(status: MatterDetailStatus.loading);

      expect(state1, state2);
      expect(state1, isNot(state3));
    });
  });
}