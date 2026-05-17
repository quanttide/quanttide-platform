"""测试共识服务。"""

from quanttide_connect.models import ConsensusStatus
from quanttide_connect.services.consensus import ConsensusService
from tests.conftest import FakeRepository


class TestConsensusService:
    def setup_method(self) -> None:
        self.repo = FakeRepository()
        self.svc = ConsensusService(self.repo)

    def test_propose(self) -> None:
        c = self.svc.propose("使用 PostgreSQL")
        assert c.content == "使用 PostgreSQL"
        assert c.status == ConsensusStatus.proposed
        assert self.repo.get_consensus(c.id) is not None

    def test_propose_with_related_messages(self) -> None:
        from quanttide_connect.models import Message, Role

        msg = self.repo.add_message(Message(content="test", role=Role.user))
        c = self.svc.propose("共识", [msg.id])
        rels = self.repo.get_relations_for_consensus(c.id)
        assert len(rels) == 1
        assert rels[0].message_id == msg.id

    def test_confirm(self) -> None:
        c = self.svc.propose("共识")
        confirmed = self.svc.confirm(c.id)
        assert confirmed is not None
        assert confirmed.status == ConsensusStatus.confirmed

    def test_confirm_not_found(self) -> None:
        assert self.svc.confirm("nonexistent") is None

    def test_deprecate(self) -> None:
        c = self.svc.propose("共识")
        self.svc.confirm(c.id)
        deprecated = self.svc.deprecate(c.id)
        assert deprecated is not None
        assert deprecated.status == ConsensusStatus.deprecated

    def test_deprecate_not_found(self) -> None:
        assert self.svc.deprecate("nonexistent") is None

    def test_full_lifecycle(self) -> None:
        c = self.svc.propose("PostgreSQL")
        assert c.status == ConsensusStatus.proposed
        self.svc.confirm(c.id)
        assert self.repo.get_consensus(c.id).status == ConsensusStatus.confirmed
        self.svc.deprecate(c.id)
        assert self.repo.get_consensus(c.id).status == ConsensusStatus.deprecated
