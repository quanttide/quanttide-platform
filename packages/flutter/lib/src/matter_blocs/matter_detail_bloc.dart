import 'dart:async';
import 'package:bloc/bloc.dart';

import '../api.dart';
import '../models/matter.dart';
import '../events/matter_events.dart';
import 'matter_detail_state.dart';



class MatterDetailBloc extends Bloc<MatterEvent, MatterDetailState> {
  final ProjectsAPIClient apiClient;

  MatterDetailBloc(this.apiClient) : super(const MatterDetailState());

  Stream<Matter> mapEventToState(MatterEvent event) async* {
    if (event is MatterRetrieved) {
      // Handle matter detail retrieval
    } else if (event is MatterListed) {
      // Handle matter listing
    } else if (event is MatterCreated) {
      // Handle matter creation
    } else if (event is MatterUpdated) {
      // Handle matter updating
    } else if (event is MatterPartialUpdated) {
      // Handle partial matter updating
    } else if (event is MatterAssigned) {
      // Handle matter assignment
    } else if (event is MatterDestroyed) {
      // Handle matter deletion
    }
  }
}
