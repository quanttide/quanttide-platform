---
name: product-tests
description: 三层测试体系：单元测试、服务测试、端到端测试
---

# product-tests

## 三层测试体系

```
单元测试         → 隔离测试单个模块
服务测试         → 测试 HTTP API 链路，不启动外部依赖。
端到端测试       → 启动真实服务，验证前后端互通。在项目根目录的`tests/`文件夹实现。
```

### 单元测试

隔离测试单个模块，mock 外部依赖。

#### 服务端

| 位置 | 框架 | 测试对象 |
|------|------|---------|
| `src/<service>/test/` | pytest | Python 模块 |

#### 客户端

| 位置 | 框架 | 测试对象 |
|------|------|---------|
| `src/<app>/packages/<pkg>/test/` | flutter_test | Dart 模块 |

### 服务测试

#### 服务端

使用 `TestClient`（FastAPI）测试完整 HTTP 请求—响应链路。

| 位置 | 框架 | 测试内容 |
|------|------|---------|
| `src/<service>/test/test_main.py` | pytest | 路由注册、健康检查、CRUD 端点、JSON 序列化 |

#### 客户端

使用 `integration_test`（Flutter）启动 mock server，渲染 widget 树，验证网络到 UI 全链路。

| 位置 | 框架 | 测试内容 |
|------|------|---------|
| `src/<app>/integration_test/` | flutter_test + shelf | 数据加载、看板渲染、错误/重试状态 |

### 端到端测试

启动真实 APP 和真实服务，验证真实数据存储下的前后端互通。

- 服务端：运行 `uvicorn`，连接真实数据库（非内存 dict）
- 客户端：运行 `flutter run`，连接真实服务地址
- 数据：验证 CRUD 操作经过存储 → API → UI 完整链路

端到端测试只测试实际业务逻辑是否有效。
