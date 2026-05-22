import uuid

import pytest
from pydantic import ValidationError

from quanttide_audit import (
    AuditCriteria,
    AuditEvidence,
    AuditFinding,
    AuditReport,
    AuditSeverity,
    AuditStatus,
)

TS = "2026-01-01T00:00:00"


def criteria(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="line-length",
        title="Line length check",
        description="Lines should not exceed 88 characters",
        severity=AuditSeverity.ERROR,
        category="style",
    )
    data.update(kw)
    return AuditCriteria(**data)


def evidence(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="ev-1",
        location="src/main.py:42",
        detail="Line has 92 chars, max is 88",
        created_at=TS,
    )
    data.update(kw)
    return AuditEvidence(**data)


def finding(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="f-1",
        criterion_name="line-length",
        evidence_names=["ev-1"],
        message="Line too long",
        severity=AuditSeverity.ERROR,
        created_at=TS,
    )
    data.update(kw)
    return AuditFinding(**data)


def report(**kw):
    data = dict(
        id=uuid.uuid4(),
        name="rep-1",
        title="Audit #1",
        criteria=[criteria()],
        evidence=[evidence()],
        findings=[finding()],
        created_at=TS,
        updated_at=TS,
    )
    data.update(kw)
    return AuditReport(**data)


class TestAuditCriteria:
    def test_valid(self):
        c = criteria()
        assert c.name == "line-length"
        assert c.severity == AuditSeverity.ERROR
        assert c.category == "style"

    def test_id_as_uuid(self):
        val = uuid.uuid4()
        c = criteria(id=val)
        assert c.id == val

    def test_id_from_str(self):
        val = "00000000-0000-0000-0000-000000000001"
        c = criteria(id=val)
        assert c.id == uuid.UUID(val)

    def test_rejects_long_name(self):
        with pytest.raises(ValidationError):
            criteria(name="a" * 101)


class TestAuditEvidence:
    def test_valid(self):
        e = evidence()
        assert e.name == "ev-1"
        assert e.location == "src/main.py:42"
        assert e.detail == "Line has 92 chars, max is 88"

    def test_created_at_set(self):
        e = evidence()
        assert e.created_at is not None


class TestAuditFinding:
    def test_valid(self):
        f = finding()
        assert f.name == "f-1"
        assert f.criterion_name == "line-length"
        assert f.message == "Line too long"
        assert f.severity == AuditSeverity.ERROR

    def test_evidence_names(self):
        f = finding(evidence_names=["ev-1", "ev-2"])
        assert f.evidence_names == ["ev-1", "ev-2"]

    def test_evidence_names_empty_default(self):
        f = finding(evidence_names=[])
        assert f.evidence_names == []

    def test_suggestion_optional(self):
        f = finding()
        assert f.suggestion is None

    def test_with_suggestion(self):
        f = finding(suggestion="Break into multiple lines")
        assert f.suggestion == "Break into multiple lines"


class TestAuditReport:
    def test_valid(self):
        r = report()
        assert r.name == "rep-1"
        assert len(r.criteria) == 1
        assert len(r.evidence) == 1
        assert len(r.findings) == 1

    def test_independent_lists(self):
        r = report(
            criteria=[criteria(name="c1"), criteria(name="c2")],
            evidence=[evidence(name="e1"), evidence(name="e2"), evidence(name="e3")],
            findings=[finding(name="f1")],
        )
        assert len(r.criteria) == 2
        assert len(r.evidence) == 3
        assert len(r.findings) == 1

    def test_is_clean_default(self):
        r = report()
        assert r.is_clean
        assert r.exit_code == 0

    def test_failed(self):
        r = report(status=AuditStatus.FAILED)
        assert not r.is_clean
        assert r.exit_code == 1

    def test_total_findings(self):
        r = report(findings=[finding(name="f1"), finding(name="f2")])
        assert r.total_findings == 2

    def test_description_optional(self):
        r = report()
        assert r.description is None

    def test_with_description(self):
        r = report(description="Full audit report")
        assert r.description == "Full audit report"


