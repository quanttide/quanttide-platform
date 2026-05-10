# 密钥管理

使用 HashiCorp Vault 提供统一密钥服务，本地和云端采用适配各自环境的解封方案，对研发保持一致的 API 接口。

## 架构

```
Vault 层 (加密微服务)
    ↓
存储层：本地 file / 云端 S3 兼容存储
```

密钥由应用直接从 Vault 获取，不经过 shell 环境变量或中间层。操作指南见 [dev/infra/vault.md](../../dev/infra/vault.md)。

## 解封策略

- 本地环境：Shamir 默认，unseal keys 备份至 Nutstore
- 云端环境：对接云 KMS 实现 Auto-unseal

## 设计要点

- Vault 层无状态，存储后端可切换
- Token 泄漏可吊销，不影响底层密钥
- Vault 不可用时应用静默回退到 `.env` / 环境变量
