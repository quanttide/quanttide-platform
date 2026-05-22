# 变更记录

## [0.1.0] - 2026-05-22

### 新增
- `AuditCriteria` — 审计标准，使用 IdField/NameField/TitleField/DescriptionField 定义规则
- `AuditFinding` — 审计发现，引用标准（criterion_name），包含多条支撑证据
- `AuditEvidence` — 审计证据，提供位置和数据（location + detail）作为可验证依据
- `AuditReport` — 审计报告，聚合多条 AuditFinding，提供 is_clean / exit_code 属性
- `AuditSeverity` / `AuditStatus` 枚举
- 所有模型使用 `quanttide` 标准字段
- 测试 19 个，覆盖率 100%
