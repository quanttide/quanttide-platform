"""
共识服务：共识的提议、确认、废弃。
"""

from __future__ import annotations

from datetime import datetime, timezone

from quanttide_connect.events import (
    ConsensusConfirmed,
    ConsensusDeprecated,
    ConsensusProposed,
    EventBus,
)
from quanttide_connect.models import Consensus, ConsensusStatus, Relation
from quanttide_connect.repository import Repository


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ConsensusService:
    def __init__(
        self, repository: Repository, event_bus: EventBus | None = None
    ) -> None:
        self.repository = repository
        self.event_bus = event_bus or EventBus()

    def propose(
        self, content: str, related_message_ids: list[str] | None = None
    ) -> Consensus:
        c = Consensus(content=content, status=ConsensusStatus.proposed)
        self.repository.add_consensus(c)
        related_message_ids = related_message_ids or []
        for mid in related_message_ids:
            if self.repository.get_message(mid):
                self.repository.add_relation(
                    Relation(message_id=mid, consensus_id=c.id)
                )
        self.event_bus.publish(
            ConsensusProposed(
                consensus_id=c.id,
                content=c.content,
                proposed_at=c.created_at,
                related_message_ids=related_message_ids,
            )
        )
        return c

    def confirm(self, consensus_id: str) -> Consensus | None:
        c = self.repository.update_consensus_status(
            consensus_id, ConsensusStatus.confirmed
        )
        if c:
            self.event_bus.publish(
                ConsensusConfirmed(consensus_id=c.id, confirmed_at=_utcnow())
            )
        return c

    def deprecate(self, consensus_id: str) -> Consensus | None:
        c = self.repository.update_consensus_status(
            consensus_id, ConsensusStatus.deprecated
        )
        if c:
            self.event_bus.publish(
                ConsensusDeprecated(consensus_id=c.id, deprecated_at=_utcnow())
            )
        return c
