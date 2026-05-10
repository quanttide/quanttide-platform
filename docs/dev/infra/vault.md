# Vault

## 维护

### 路径命名

路径按来源分两类：

| 类型 | 路径 | 谁读 | 例子 |
|------|------|------|------|
| 私有 | `secret/<app>/` | 仅该应用 | `secret/stack-auth/` |
| 公共 | `secret/<provider>/` | 多个应用共享 | `secret/deepseek/` |

## 使用

### API 路径差异

KV v2 引擎强制 API 路径带 `/data/`：

| 场景 | 写法 | 例子 |
|------|------|------|
| CLI | `secret/<name>` | `vault kv get secret/deepseek` |
| 代码 | `secret/data/<name>` | `"vault_secret_path": "secret/data/deepseek"` |

### 命名风格

**不要**让 Vault key 名 = 应用字段名。它们是不同层的命名：

| 层级 | 命名原则 | 例子 |
|------|---------|------|
| Vault 路径 | 标识提供商/范围 | `secret/deepseek` |
| Vault key | 简短自描述，路径已做区隔 | `api_key`、`base_url` |
| 应用字段 | 遵循应用自有命名 | `llm_api_key` |

Vault key 只需在路径范围内自描述即可，不要跟应用字段名强行一致。

## 语言与框架

### Python 应用接入

依赖：

```bash
pip install pydantic-settings-vault
```

在 Settings 类中声明字段的 Vault 来源：

```python
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_vault import VaultSettingsSource


class Settings(BaseSettings):
    llm_base_url: str = "https://api.deepseek.com"

    llm_api_key: str = Field(
        json_schema_extra={
            "vault_secret_path": "secret/data/deepseek",
            "vault_secret_key": "api_key",
        },
    )

    @classmethod
    def settings_customise_sources(
        cls, settings_cls, init_settings, env_settings,
        dotenv_settings, file_secret_settings,
    ):
        return (
            init_settings,
            VaultSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )
```

使用：

```python
settings = Settings()
client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
```

Vault 不可用时自动回退到环境变量或默认值。
