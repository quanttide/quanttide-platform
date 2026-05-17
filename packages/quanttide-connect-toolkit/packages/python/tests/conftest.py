"""
测试用内存仓储：实现 Repository Protocol，不持久化。
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from quanttide_connect.models import Consensus, ConsensusStatus, Message, Relation, Role
from quanttide_connect.repository import Repository


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class FakeRepository:
    """内存仓储，实现 Repository Protocol。"""

    def __init__(self) -> None:
        self._messages: dict[str, dict[str, Any]] = {}
        self._consensuses: dict[str, dict[str, Any]] = {}
        self._relations: dict[str, dict[str, Any]] = {}

    def add_message(self, msg: Message) -> Message:
        self._messages[msg.id] = msg.model_dump(mode="json")
        return msg

    def get_message(self, message_id: str) -> Message | None:
        d = self._messages.get(message_id)
        return Message(**d) if d else None

    def list_messages(self) -> list[Message]:
        return [Message(**d) for d in self._messages.values()]

    def update_message(self, message_id: str, new_content: str) -> Message | None:
        d = self._messages.get(message_id)
        if not d:
            return None
        d["content"] = new_content
        d["updated_at"] = _utcnow()
        return Message(**d)

    def add_consensus(self, c: Consensus) -> Consensus:
        self._consensuses[c.id] = c.model_dump(mode="json")
        return c

    def get_consensus(self, consensus_id: str) -> Consensus | None:
        d = self._consensuses.get(consensus_id)
        return Consensus(**d) if d else None

    def list_consensuses(
        self, status: ConsensusStatus | None = None
    ) -> list[Consensus]:
        result = [Consensus(**d) for d in self._consensuses.values()]
        if status:
            result = [c for c in result if c.status == status]
        return result

    def update_consensus_status(
        self, consensus_id: str, status: ConsensusStatus
    ) -> Consensus | None:
        d = self._consensuses.get(consensus_id)
        if not d:
            return None
        d["status"] = status.value
        d["updated_at"] = _utcnow()
        return Consensus(**d)

    def add_relation(self, r: Relation) -> Relation:
        self._relations[r.id] = r.model_dump(mode="json")
        return r

    def remove_relation(self, relation_id: str) -> bool:
        return self._relations.pop(relation_id, None) is not None

    def get_relations_for_consensus(self, consensus_id: str) -> list[Relation]:
        return [
            Relation(**r)
            for r in self._relations.values()
            if r["consensus_id"] == consensus_id
        ]

    def get_relations_for_message(self, message_id: str) -> list[Relation]:
        return [
            Relation(**r)
            for r in self._relations.values()
            if r["message_id"] == message_id
        ]
