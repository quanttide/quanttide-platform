---
name: product-python
description: 完整实现一个Python库，涵盖脚手架、数据模型、序列化、测试、发布全流程
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

## 职责

从零完整实现一个 Python 库，涵盖项目初始化、代码实现、测试、文档、发布。

## 工作流

### 1. 脚手架

```bash
uv init --package --lib --name <pkg-name> --description "<desc>" --build-backend hatch --author-from none <path>
cd <path>
uv add pydantic
uv add --dev pytest pytest-cov ruff
```

- 包名用连字符（如 `quanttide-project`），导入名下划线（如 `quanttide_project`）
- src 布局：`src/<import_name>/`
- 配置 `pyproject.toml`：`license`、`authors`、`[tool.ruff]`、`[tool.pytest.ini_options]`
- 写入 `.gitignore`，内容如下：

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/
cover/
*.log
instance/
.webassets-cache
.scrapy
docs/_build/
.pybuilder/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.python-version
Pipfile.lock
poetry.lock
pdm.lock
.pdm.toml
__pypackages__/
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.ruff_cache/
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
.idea/
*.iml
.DS_Store
```

### 2. 数据模型

- 使用 Pydantic `BaseModel`，`frozen=True` 实现不可变
- 字段类型完整注解，可选字段 `Optional[T] = None`
- 空值默认使用 `""` / `{}` 等不可变类型
- 枚举类使用 Python `Enum` 或 `StrEnum`
- `ConfigDict(populate_by_name=True)` 支持别名

### 3. 序列化

- `model_validate(data)` 反序列化（等效 from_json）
- `model_dump(mode="json", exclude_none=True)` 序列化
- 按需实现 `to_dict()` 方法，处理空集合排除等 Dart 兼容逻辑
- datetime 序列化使用 `@field_serializer`

### 4. 更新模式

- 不可变模型通过 `replace()` 方法（等效 copyWith）返回新实例
- 只暴露允许修改的字段为参数

### 5. 测试

- `tests/` 目录，每模块一个测试文件
- 测试覆盖：构造、反序列化、序列化、更新、往返

### 6. 质量

```bash
uv run ruff check src/ tests/
uv run pytest --cov=src/
```

### 7. 文档与发布

- `README.md` 含使用示例
- `CHANGELOG.md` 按语义版本记录
- 发布：`uv build` + `uv publish`

## 特殊情况：参考现有包实现

若参考其他语言包（如 Dart），需额外步骤：

1. 先阅读原包的所有源文件，理解完整 API 表面
2. 建立映射表（字段名、类型、方法签名）
3. 语言惯例对齐：camelCase → snake_case，语言原生类型
4. 不照搬不适合 Python/Pydantic 的习惯

## 包结构模板

```
<import_name>/
├── __init__.py          # barrel export
├── models/
│   ├── __init__.py
│   ├── foo.py
│   └── bar.py
├── enums.py             # 枚举定义（可选）
└── ...                  # 其他模块
```
