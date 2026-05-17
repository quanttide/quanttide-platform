# 项目约定

## 目录结构

```
quanttide-platform/
├── apps/       → 独立可部署的应用/产品（子模块）
│   └── qtconsult/ 等 31 个
├── packages/   → 跨应用共享的 SDK/工具包（子模块）
│   ├── quanttide-connect-toolkit/ — 沟通工程工具包（Dart）
│   ├── quanttide-course-toolkit/  — 课程 SDK
│   ├── quanttide-data-toolkit/    — 数据 SDK（Django/Flutter/Python）
│   ├── quanttide-docs-toolkit/    — 文档工程工具包（Dart/Python/Flutter）
│   └── quanttide-project-toolkit/ — 项目工具包
├── manifests/  → 系统声明配置
└── docs/       → 文档
```

### apps/ vs packages/

| 维度 | apps/ | packages/ |
|------|-------|-----------|
| 定位 | 独立可部署的产品/应用 | 跨应用复用的 SDK/工具包 |
| 消费者 | 终端用户 | apps/ 中的应用开发者 |
| 生命周期 | 随产品迭代独立发布 | 随底层需求更新，被多个 app 依赖 |

**关键规则**：
- `apps/` 中的项目可以依赖 `packages/` 中的包，反之不可
- `packages/` 不包含业务逻辑，只提供通用能力和工具函数
- **packages 不强制 apps 使用**：新增 app 时先检查 `packages/` 是否有可复用的能力，避免重复造轮；但如果通用模型无法满足业务需求，app 应创建自己的私有包，不必扭曲业务代码去适配通用包
- app 可以在内部建私有包（如 `qtconsult` 的 `src/studio/packages/qtconsult-project`），这属于 app 内部职责，与平台级 `packages/` 无关

**packages 的设计哲学：服务而非管控**
- packages 用**质量和便利性赢得采纳**，而不是靠规则强制使用
- 当多个 app 都需要同类能力时，packages 提供一个经过打磨的起点，降低重复建设成本
- 如果多个 app 都自愿用了同一个 package，跨 app 的数据互通和协作自然形成
- 本质是用**市场逻辑代替架构管控**：不好用的 package 会被自然淘汰，反向驱动 package 保持高质量

### 何时需要 packages（以 Dart 库为例）

实践来自 `quanttide-project-toolkit`（packages/）与 `qtconsult`（apps/）：

**packages/ 满足三个条件才升至平台层：**
1. **跨平台** — 同一领域模型需在 Dart + Flutter + Django 等多端共存
2. **跨应用** — 不止一个 app 需要该能力（如项目模型 qtconsult / qtdata 都可能用）
3. **独立版本** — 领域模型有自己的迭代节奏，不绑定任何一个 app 的发布周期

**反之，留在 app 内部的场景：**
- 仅单 app 使用的特化逻辑（如 `qtconsult-project` 的 OODA 适配层）
- 带业务或技术栈绑定的私有包（Flutter UI 依赖、业务定制逻辑）

**依赖链示例（Dart）：**
```
packages/quanttide-project-toolkit/packages/dart/
  → pub.dev 发布为 quanttide_project: ^0.1.0
  → 纯 Dart，无 Flutter 依赖，通用领域模型
  ↑
apps/qtconsult/src/studio/packages/qtconsult-project/
  → 依赖 quanttide_project: ^0.1.0
  → Flutter 私有包，OODA 特化适配
  ↑
apps/qtconsult/src/studio/
  → 主应用
```

**判断标准：能被两个以上 app 在纯 Dart 层共用的 → packages/；带业务或平台特化且单 app 独占的 → 留在 app 内部。**

---

设计原则与版本策略等见 [docs/prd/index.md](docs/prd/index.md)。
