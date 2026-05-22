from pydantic import BaseModel, Field
from quanttide import CreatedAtField, IdField, NameField

from quanttide_audit.models.enums import AuditSeverity


class AuditFinding(BaseModel):
    """审计发现：由"证据匹配标准"产生。"""

    id: IdField
    name: NameField
    criterion_name: NameField
    evidence_names: list[NameField] = Field(default_factory=list)
    message: str
    severity: AuditSeverity
    suggestion: str | None = None
    created_at: CreatedAtField
