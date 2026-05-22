from pydantic import BaseModel
from quanttide import CreatedAtField, IdField, NameField


class AuditEvidence(BaseModel):
    """审计证据：原始数据。

    独立收集，不引用标准或发现，作为素材等待被标准检验。
    """

    id: IdField
    name: NameField
    location: str
    detail: str
    created_at: CreatedAtField
