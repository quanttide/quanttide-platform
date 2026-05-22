from __future__ import annotations

from pydantic import BaseModel, Field
from quanttide import (
    CreatedAtField,
    DescriptionField,
    IdField,
    NameField,
    TitleField,
    UpdatedAtField,
)

from quanttide_audit.models.criteria import AuditCriteria
from quanttide_audit.models.enums import AuditSeverity, AuditStatus  # noqa: F401
from quanttide_audit.models.evidence import AuditEvidence
from quanttide_audit.models.finding import AuditFinding


class AuditReport(BaseModel):
    """审计报告：聚合一次审计的完整上下文与结论。

    标识:
        id: 全局唯一标识（UUID）
        name: 报告唯一名称，slug 风格
        title: 报告可读标题
    说明:
        description: 报告补充说明，如审计范围、运行环境
    审计数据:
        criteria: 本次审计使用的所有标准，报告自包含
        evidence: 本次审计收集的所有原始证据，独立存在
        findings: 证据匹配标准后产生的所有发现
    结论:
        status: PASSED=通过, FAILED=未通过, NEEDS_REVIEW=需人工复核
    时间追踪:
        created_at: 报告创建时间
        updated_at: 报告最后更新时间

    Usage:
        >>> from uuid import uuid4
        >>> now = "2026-01-01T00:00:00"
        >>> f = AuditFinding(
        ...     id=uuid4(), name="f-1", criterion_name="line-length",
        ...     message="Line too long", severity=AuditSeverity.ERROR,
        ...     created_at=now,
        ... )
        >>> r = AuditReport(
        ...     id=uuid4(), name="rep-1", title="Audit #1",
        ...     findings=[f], created_at=now, updated_at=now,
        ... )
        >>> r.is_clean
        True
    """

    # 标识
    id: IdField
    name: NameField
    title: TitleField

    # 说明
    description: DescriptionField | None = None

    # 审计数据
    criteria: list[AuditCriteria] = Field(default_factory=list)
    evidence: list[AuditEvidence] = Field(default_factory=list)
    findings: list[AuditFinding] = Field(default_factory=list)

    # 结论
    status: AuditStatus = AuditStatus.PASSED

    # 时间追踪
    created_at: CreatedAtField
    updated_at: UpdatedAtField

    @property
    def is_clean(self) -> bool:
        return self.status == AuditStatus.PASSED

    @property
    def exit_code(self) -> int:
        return 0 if self.is_clean else 1

    @property
    def total_findings(self) -> int:
        return len(self.findings)
