# Vault 操作指南

## 文件路径约定

| 路径 | 角色 | 内容 | 创建者 |
|------|------|------|--------|
| `~/.vault-token` | **文件** — CLI token | vault CLI 凭据（纯文本 token） | 手动写入 |
| `~/.vault-data/` | **目录** — Vault 服务器数据 | `config/vault.hcl`、`data/`、`logs/` | Terraform + 用户启动 |

### token 读取顺序

vault CLI 读取 token 的顺序：

1. `VAULT_TOKEN` 环境变量（已废弃，不设）
2. `~/.vault-token` 文件

开发者终端操作 `vault xxx` 或 `terraform apply` 时，CLI 自动从 `~/.vault-token` 取 token，无需 export。

## 快速启动

```bash
# 1. 生成 Vault 配置（首次或配置变更后）
export VAULT_TOKEN=$(cat ~/.vault-token)
terraform apply -var="home=$HOME"

# 2. 启动 Vault 服务器
vault server -config=~/.vault-data/config/vault.hcl

# 3. 另开终端，检查状态
vault status                           # 应为 Sealed: true
vault operator unseal                  # 输入任意一个 unseal key
vault status                           # 应为 Sealed: false

# 4. 验证
vault kv get secret/stack-auth
```

## Secret 路径组织

### 规则

```
secret/<name>
```

一个路径下放一个逻辑单元的 key，不分层级。路径按来源分两类：

| 路径 | 类型 | 谁读 | 例子 |
|------|------|------|------|
| `secret/<app>/` | 应用私有 | 仅该应用 | `secret/stack-auth/`、`secret/qtcloud-write/` |
| `secret/<provider>/` | 公共供应商 | 多个应用共享 | `secret/deepseek/` |

### Key 命名

| 消费者 | Key 命名 | 例子 |
|--------|---------|------|
| Python 自研应用 | snake_case（匹配 Settings 字段） | `deepseek_api_key` |
| 第三方应用 | 按对方期望的 env var 名 | `STACK_SERVER_SECRET` |

### API 路径约定

KV v2 引擎强制 API 路径带 `/data/`，代码中与实际路径的写法不同：

| 场景 | 写法 | 例子 |
|------|------|------|
| 大脑里想 | `secret/<name>` | `secret/deepseek` |
| CLI 操作 | `secret/<name>` | `vault kv get secret/deepseek` |
| Python 代码 | `secret/data/<name>` | `vault_secret_path: "secret/data/deepseek"` |
| Terraform | `secret/data/<name>` | `vault_kv_secret_v2` 的 data_path |

## Nutstore 备份

`~/Nutstore Files/secrets/` 包含：

| 文件 | 内容 |
|------|------|
| `vault-init-keys.json` | unseal keys × 5 + root token |
| `stack-auth-secrets.json` | Stack Auth 连接串和服务端密钥 |

## 应用集成（Python）

Python 应用通过 `pydantic-settings-vault` 库从 Vault 读取密钥。

### 依赖

```bash
pip install pydantic-settings-vault
```

### 用法

在 Settings 类的字段上标注 Vault 路径和键名：

```python
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_vault import VaultSettingsSource


class Settings(BaseSettings):
    llm_api_key: str = Field(
        json_schema_extra={
            "vault_secret_path": "secret/data/deepseek",
            "vault_secret_key": "api_key",
        },
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            VaultSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )
```

### 优先级

init 参数 → Vault → 环境变量 → .env 文件。Vault 不可用时静默回退到环境变量或默认值。

### 认证

`VaultSettingsSource` 自动读取 `VAULT_ADDR` 和 `~/.vault-token`，与开发者终端所用凭证一致。当前阶段应用和开发者共用 root token。

## 常用命令

```bash
vault status                         # Vault 运行状态
vault kv get secret/stack-auth       # 读取密钥
vault kv put secret/stack-auth k=v   # 写入密钥
vault operator unseal                # 解封
vault operator seal                  # 封箱
```
