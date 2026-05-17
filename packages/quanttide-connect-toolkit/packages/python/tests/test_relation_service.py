"""测试关联服务。"""

from quanttide_connect.models import Consensus, Message, Role
from quanttide_connect.services.relation import RelationService
from tests.conftest import FakeRepository


class TestRelationService:
    def setup_method(self) -> None:
        self.repo = FakeRepository()
        self.svc = RelationService(self.repo)
        self.msg = self.repo.add_message(Message(content="test", role=Role.user))
        self.con = self.repo.add_consensus(Consensus(content="共识"))

    def test_link(self) -> None:
        r = self.svc.link(self.msg.id, self.con.id)
        assert r is not None
        assert r.message_id == self.msg.id
        assert r.consensus_id == self.con.id

    def test_link_invalid_message(self) -> None:
        assert self.svc.link("bad", self.con.id) is None

    def test_link_invalid_consensus(self) -> None:
        assert self.svc.link(self.msg.id, "bad") is None

    def test_unlink(self) -> None:
        r = self.svc.link(self.msg.id, self.con.id)
        assert self.svc.unlink(r.id) is True
        assert len(self.repo.get_relations_for_consensus(self.con.id)) == 0

    def test_unlink_not_found(self) -> None:
        assert self.svc.unlink("nonexistent") is False

    def test_get_relations_for_consensus(self) -> None:
        self.svc.link(self.msg.id, self.con.id)
        rels = self.repo.get_relations_for_consensus(self.con.id)
        assert len(rels) == 1
