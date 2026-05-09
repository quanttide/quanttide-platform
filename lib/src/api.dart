/// 项目管理API

import "package:flutter_quanttide/api_client.dart";

import "models/project.dart";
import "models/matter.dart";


/// 项目管理API Mixin类
mixin ProjectsAPIMixin on APIClient {
  /// 获取项目列表
  Future<List<Project>> listProjects() async {
    List<dynamic> data = await requestAPI(apiPath: '/projects', httpMethod: 'GET');
    List<Project> projects = data.map((dynamic e) {
      return Project.fromJson(Map<String, dynamic>.from(e as Map));
    }).toList();
    return projects;
  }

  /// 获取事项列表
  Future<List<Matter>> listMatters({required String projectName, required String apiRoot}) async {
    List<dynamic> data = await requestAPI(apiPath: '/matters', httpMethod: 'GET');
    List<Matter> matters = data.map((dynamic e) {
      return Matter.fromJson(Map<String, dynamic>.from(e as Map));
    }).toList();
    return matters;
  }
}


/// 项目管理API Client类
class ProjectsAPIClient extends APIClient with ProjectsAPIMixin {
  ProjectsAPIClient({required super.apiRoot});
}
