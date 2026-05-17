"""测试消息服务。"""

from quanttide_connect.models import Role
from quanttide_connect.services.message import MessageService
from tests.conftest import FakeRepository


class TestMessageService:
    def setup_method(self) -> None:
        self.repo = FakeRepository()
        self.svc = MessageService(self.repo)

    def test_send(self) -> None:
        msg = self.svc.send("你好", Role.user)
        assert msg.content == "你好"
        assert msg.role == Role.user
        assert self.repo.get_message(msg.id) is not None

    def test_send_and_retrieve(self) -> None:
        self.svc.send("a", Role.user)
        self.svc.send("b", Role.agent)
        assert len(self.repo.list_messages()) == 2

    def test_edit(self) -> None:
        msg = self.svc.send("original", Role.user)
        updated = self.svc.edit(msg.id, "edited")
        assert updated is not None
        assert updated.content == "edited"
        assert updated.updated_at is not None

    def test_edit_not_found(self) -> None:
        assert self.svc.edit("nonexistent", "x") is None
