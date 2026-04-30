# Flutter

本文档主要介绍量潮应用体系下的Flutter应用之间的依赖关系，帮助开发者和架构师组织Flutter客户端软件工程。

## 分类

根据Flutter框架提供的项目分类，量潮应用系统的Flutter项目可以分为以下三类：

- Flutter应用（Flutter Applications）：用户使用的客户端应用，包括**量潮课堂APP**、**量潮企业后台**及其子应用。
- Flutter包（Flutter Packages）：Flutter项目依赖的纯Dart包。
- Flutter插件（Flutter Plugins）：Flutter项目依赖的有Native平台代码的包。

## 分层

为了让开发者更方便地复用已有积累，我们把Flutter的组件库从底层到底层分为以下三层：

1. 应用内组件：Flutter应用内根据需求自定义的组件，通常维护在`lib/widgets`文件夹下。
2. 量潮组件：量潮设计语言指导下的组件及其风格，实现在开源项目部设计工程组负责维护的[`quanttide_design`](https://pub.dev/packages/quanttide_design)库。
3. 社区组件：官方组件、社区组件库和开源项目部Flutter组负责维护的自建开源组件库，相关实践在[量潮Flutter手册](https://quanttide.coding.net/public/quanttide-handbooks/quanttide-handbook-on-flutter/git/files)维护。
