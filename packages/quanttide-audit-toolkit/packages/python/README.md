# quanttide-audit-toolkit

量潮审计工具箱 Python SDK，基于量潮标准字段（`quanttide`）提供审计领域数据模型。

## 安装

```bash
pip install quanttide-audit-toolkit
```

## 数据模型关系

```
AuditEvidence  +  AuditCriteria  →  AuditFinding  →  AuditReport
```

| 步骤 | 模型 | 角色 | 关键字段 |
|------|------|------|---------|
| ① 收集 | **AuditEvidence** | 原始证据，独立存在 | location, detail |
| ① 定义 | **AuditCriteria** | 检查规则，独立存在 | severity, category |
| ② 匹配 | **AuditFinding** | 证据匹配标准后产生的发现 | criterion_name, evidence_names |
| ③ 聚合 | **AuditReport** | 完整审计结论 | criteria[], evidence[], findings[] |

- `AuditFinding.criterion_name` → 指向被违反的 `AuditCriteria.name`
- `AuditFinding.evidence_names` → 指向触发该发现的 `AuditEvidence.name`
- `AuditReport` 同时持有 criteria / evidence / findings 三个独立列表，自包含全部上下文

## 快速开始

```python
from uuid import uuid4
from quanttide_audit import (
    AuditCriteria, AuditEvidence, AuditFinding,
    AuditReport, AuditSeverity, AuditStatus,
)

now = "2026-01-01T00:00:00"

criterion = AuditCriteria(
    id=uuid4(), name="line-length", title="Line length check",
    description="Lines should not exceed 88 characters",
    severity=AuditSeverity.ERROR, category="style",
)

evidence = AuditEvidence(
    id=uuid4(), name="ev-1",
    location="src/main.py:42",
    detail="Line has 92 chars, max is 88",
    created_at=now,
)

finding = AuditFinding(
    id=uuid4(), name="f-1", criterion_name="line-length",
    evidence_names=["ev-1"],
    message="Line too long", severity=AuditSeverity.ERROR,
    created_at=now,
)

report = AuditReport(
    id=uuid4(), name="rep-1", title="Code Audit #1",
    criteria=[criterion], evidence=[evidence], findings=[finding],
    status=AuditStatus.FAILED,
    created_at=now, updated_at=now,
)

print(report.is_clean)       # False
print(report.exit_code)      # 1
print(report.total_findings) # 1
```

## 数据模型

| 模型 | 字段 | 标准字段类型 |
|------|------|-------------|
| `AuditCriteria` | id, name, title, description, severity, category | IdField, NameField, TitleField, DescriptionField |
| `AuditEvidence` | id, name, location, detail, created_at | IdField, NameField, CreatedAtField |
| `AuditFinding` | id, name, criterion_name, evidence_names[], message, severity, suggestion, created_at | IdField, NameField, CreatedAtField |
| `AuditReport` | id, name, title, description, criteria[], evidence[], findings[], metadata, status, created_at, updated_at | IdField, NameField, TitleField, DescriptionField, CreatedAtField, UpdatedAtField |

## 开发

```bash
uv sync --dev
uv run pytest --cov=src/
uv run ruff check src/ tests/
```
