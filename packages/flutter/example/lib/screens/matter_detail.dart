/// 事项详情页面示例

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';


class MatterDetailScreen extends StatelessWidget {
  const MatterDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('事项详情页面示例'),
        ),
      body: const MatterDetailView(),
    );
  }
}


class MatterDetailView extends StatelessWidget {
  const MatterDetailView({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    throw UnimplementedError();
  }

}


class MatterDetailBloc {

}