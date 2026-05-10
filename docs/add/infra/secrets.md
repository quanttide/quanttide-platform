# 密钥管理

使用 HashiCorp Vault 提供统一密钥服务，本地和云端采用适配各自环境的解封方案，对研发保持一致的 API 接口。

## 架构

```
业务层 (应用 A/B、CI/CD)
    ↓          ↑ 受限 token，直接读 Vault
Vault 层 (加密微服务)
    ↓
存储层：本地 file / 云端 S3 兼容存储
```

密钥由应用直接从 Vault 获取，不经过 shell 环境变量或中间层。

## 解封策略

- 本地环境：Shamir 默认，unseal keys 备份至 Nutstore
- 云端环境：对接云 KMS 实现 Auto-unseal

## 应用访问约定

应用通过受限 token 直接从 Vault 读取自己的密钥。

| 约定 | 值 | 说明 |
|------|----|------|
| Token 存放路径 | `~/.vault/tokens/<app>` | 由 Terraform 写入，权限 0600 |
| Vault secret 路径 | `secret/<app>` | 每个应用独占 |
| Vault policy 名 | `read-<app>` | 只读 `secret/data/<app>` |
| 应用标识符 | 目录名 | 与 repo 中 `apps/<app>` 一致 |

Terraform 通过 `for_each` 循环声明所有应用的 policy 和 token，无需逐一手写。

## 共享库

所有 Python 应用共用 `qtcloud-vault`（待建），提供：

```python
from qtcloud_vault import vault_settings

extra = vault_settings("qtcloud-write", "secret/deepseek")
```

非 Python 应用各自实现 HTTP 调用（Vault REST API），协议不变。

## 设计要点

- Vault 层无状态，存储后端可切换
- Token 泄漏可吊销，不影响底层密钥
- Vault 不可用时应用静默回退到 `.env` / 环境变量
