# 契约测试

跨语言数据模型一致性验证。

## 方案

以语言无关的 JSON Schema 作为单一事实来源（SSOT），各语言在自身包内编写契约测试，统一引用根 `tests/` 下的 Schema 和 Fixture。

```
tests/
  README.md
  schemas/
  fixtures/
packages/
  python/tests/
  flutter/test/
```
