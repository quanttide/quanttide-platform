from pydantic import BaseModel, Field
from quanttide import DescriptionField, IdField, NameField, TitleField

from quanttide_audit.models.enums import AuditSeverity


class AuditCriteria(BaseModel):
    """审计标准：定义检查规则。

    作为"标尺"独立存在，不引用证据或发现。
    """

    id: IdField
    name: NameField
    title: TitleField
    description: DescriptionField
    severity: AuditSeverity
    category: str = Field(default="", max_length=50)
