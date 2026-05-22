from enum import Enum


class AuditSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    SUGGESTION = "suggestion"


class AuditStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"
