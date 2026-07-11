"""后台管理端到端测试。

运营管理员对课程体系、班级、用户、支付的运维操作。
"""

from __future__ import annotations

import json
import urllib.request

import pytest

from .conftest import ADMIN_PASSWORD, http_get, http_post


class TestAdminAuth:
    """后台用户与认证管理。"""

    def test_admin_login_password_grant(self, auth_service):
        """管理员使用密码授权登录，获取 access_token。"""
        status, body = http_post(
            f"{auth_service}/oauth/token",
            form={
                "grant_type": "password",
                "username": "admin",
                "password": ADMIN_PASSWORD,
            },
        )
        assert status == 200, f"status={status} body={body}"
        data = json.loads(body)
        assert "access_token" in data
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        assert token.count(".") == 3, "not a valid JWT"

    def test_admin_login_wrong_password(self, auth_service):
        """错误密码应返回 401。"""
        status, body = http_post(
            f"{auth_service}/oauth/token",
            form={
                "grant_type": "password",
                "username": "admin",
                "password": "wrong-password",
            },
        )
        assert status == 401

    def test_userinfo(self, auth_service, auth_token):
        """用 access_token 获取用户信息。"""
        status, body = http_get(f"{auth_service}/userinfo", token=auth_token)
        assert status == 200
        data = json.loads(body)
        assert data["sub"]

    def test_userinfo_no_token(self, auth_service):
        """无 token 访问 userinfo 应返回 401。"""
        status, body = http_get(f"{auth_service}/userinfo")
        assert status == 401

    def test_unsupported_grant_type(self, auth_service):
        """不支持的 grant_type 应返回 400。"""
        status, body = http_post(
            f"{auth_service}/oauth/token",
            form={"grant_type": "client_credentials"},
        )
        assert status == 400


class TestAdminCourseContent:
    """后台课程内容管理。

    管理员对 Program → Course → Lesson → Scene 进行 CRUD 和关联配置。
    """

    def test_create_program(self, course_service):
        """创建专业 (Program)。"""
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "后台-测试专业", "description": "管理员创建"},
        )
        assert status == 201
        data = json.loads(resp)
        assert data["name"] == "后台-测试专业"

    def test_program_crud_flow(self, course_service):
        """完整的 Program → Course → Lesson 三级创建与关联。"""
        # 创建 Program
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "大数据微专业", "status": "published"},
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        # 创建 Course（扁平资源）
        status, resp = http_post(
            f"{course_service}/courses",
            data={"name": "Python 基础", "status": "draft"},
        )
        assert status == 201
        cid = json.loads(resp)["id"]

        # 创建 Lesson（扁平资源）
        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "变量与类型", "duration": 45},
        )
        assert status == 201
        lid = json.loads(resp)["id"]

        # 建立关联：Program.courseIds = [cid], Course.lessonIds = [lid]
        req = urllib.request.Request(
            f"{course_service}/programs/{pid}",
            data=json.dumps({
                "id": pid, "name": "大数据微专业", "status": "published",
                "courseIds": [cid],
            }).encode(),
            headers={"Content-Type": "application/json"}, method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            assert cid in json.loads(r.read().decode())["courseIds"]

        req = urllib.request.Request(
            f"{course_service}/courses/{cid}",
            data=json.dumps({
                "id": cid, "name": "Python 基础", "status": "published",
                "lessonIds": [lid],
            }).encode(),
            headers={"Content-Type": "application/json"}, method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            assert lid in json.loads(r.read().decode())["lessonIds"]

        # 列表查询
        for path in ("/programs", "/courses", "/lessons"):
            status, resp = http_get(f"{course_service}{path}")
            assert status == 200

        # 获取单个
        for path in (f"/programs/{pid}", f"/courses/{cid}", f"/lessons/{lid}"):
            status, resp = http_get(f"{course_service}{path}")
            assert status == 200

    def test_create_scene(self, course_service):
        """管理员创建互动场景。"""
        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "场景测试课时", "duration": 45},
        )
        assert status == 201
        lid = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/scenes",
            data={
                "lessonId": lid,
                "videoUrl": "https://media.example.com/test.mp4",
                "choices": [{"label": "继续", "targetSceneId": ""}],
            },
        )
        assert status == 201
        assert json.loads(resp)["id"] != ""

    def test_get_nonexistent_returns_404(self, course_service):
        """查询不存在的资源应返回 404。"""
        for path in ("/programs/nonexistent", "/courses/nonexistent",
                     "/lessons/nonexistent", "/classes/nonexistent"):
            status, body = http_get(f"{course_service}{path}")
            assert status == 404, f"{path}: expected 404, got {status}"

    def test_create_missing_required_field(self, course_service):
        """创建资源缺少必填字段应返回 400。"""
        cases = [
            ("/programs", {"description": "no name"}),
            ("/courses", {"status": "draft"}),
            ("/lessons", {"duration": 45}),
        ]
        for path, data in cases:
            status, resp = http_post(f"{course_service}{path}", data=data)
            assert status == 400, f"{path}: expected 400, got {status}"


class TestAdminClassManagement:
    """后台班级管理。

    管理员对教学班级的创建、状态变更、删除等运维操作。
    """

    def _create_program(self, url: str) -> str:
        status, resp = http_post(url, data={"name": "班级管理测试专业"})
        assert status == 201
        return json.loads(resp)["id"]

    def _create_class(self, url: str, name: str, ref_id: str) -> dict:
        status, resp = http_post(
            f"{url}/classes",
            data={
                "name": name, "refName": "班级管理测试专业",
                "refType": "program", "refId": ref_id,
                "status": "preparing",
                "startDate": "2026-09-01", "endDate": "2027-01-15",
            },
        )
        assert status == 201
        return json.loads(resp)

    def test_create_class(self, course_service):
        """管理员创建教学班级。"""
        pid = self._create_program(course_service)
        cls = self._create_class(course_service, "2026秋-大数据班", pid)
        assert cls["name"] == "2026秋-大数据班"
        assert cls["refType"] == "program"
        assert cls["refId"] == pid
        assert cls["status"] == "preparing"

    def test_class_status_transition(self, course_service):
        """班级状态流转：preparing → active → ended。"""
        pid = self._create_program(course_service)
        cls = self._create_class(course_service, "状态流转测试班", pid)
        cid = cls["id"]

        for status, progress, students in [
            ("active", 0.0, 0),
            ("active", 0.6, 15),
            ("ended", 1.0, 15),
        ]:
            req = urllib.request.Request(
                f"{course_service}/classes/{cid}",
                data=json.dumps({
                    "name": cls["name"], "refName": cls["refName"],
                    "refType": cls["refType"], "refId": cls["refId"],
                    "status": status, "startDate": cls["startDate"],
                    "endDate": cls["endDate"],
                    "studentCount": students, "progress": progress,
                }).encode(),
                headers={"Content-Type": "application/json"}, method="PUT",
            )
            with urllib.request.urlopen(req) as r:
                updated = json.loads(r.read().decode())
            assert updated["status"] == status

    def test_list_classes(self, course_service):
        """列出所有班级。"""
        status, resp = http_get(f"{course_service}/classes")
        assert status == 200
        assert isinstance(json.loads(resp), list)

    def test_delete_class(self, course_service):
        """删除班级。"""
        pid = self._create_program(course_service)
        cls = self._create_class(course_service, "待删除班级", pid)
        cid = cls["id"]
        req = urllib.request.Request(f"{course_service}/classes/{cid}", method="DELETE")
        with urllib.request.urlopen(req) as r:
            assert r.status == 204


class TestAdminPayManagement:
    """后台支付管理。

    管理员对订单的查询、退款操作。
    """

    def test_pay_create(self, pay_service):
        """发起支付订单。"""
        status, resp = http_post(
            f"{pay_service}/pay",
            data={
                "OrderID": "ADMIN-ORD-001", "Amount": 199.99,
                "Subject": "大数据微专业 - 报名费",
            },
        )
        assert status == 200
        data = json.loads(resp)
        assert data["TradeID"] != ""

    def test_query_order(self, pay_service):
        """查询支付订单。"""
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": "ADMIN-ORD-002", "Amount": 99.00, "Subject": "测试查询"},
        )
        status, resp = http_get(f"{pay_service}/query/ADMIN-ORD-002")
        assert status == 200
        data = json.loads(resp)
        assert data["Status"] == "SUCCESS"

    def test_refund(self, pay_service):
        """发起退款。"""
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": "ADMIN-ORD-003", "Amount": 299.00, "Subject": "退款测试"},
        )
        status, resp = http_post(
            f"{pay_service}/refund",
            data={"OrderID": "ADMIN-ORD-003", "RefundAmount": 299.00, "Reason": "学员退课"},
        )
        assert status == 200
        data = json.loads(resp)
        assert data["Status"] == "SUCCESS"

    def test_pay_invalid_body(self, pay_service):
        """无效请求体应返回 400。"""
        req = urllib.request.Request(
            f"{pay_service}/pay", data=b"not-json",
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(req)
        assert e.value.code == 400

    def test_refund_invalid_body(self, pay_service):
        """退款请求体缺失应返回 400。"""
        req = urllib.request.Request(
            f"{pay_service}/refund", data=b"",
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(req)
        assert e.value.code == 400
