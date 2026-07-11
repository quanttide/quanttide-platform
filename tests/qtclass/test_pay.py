"""qtcloud-course Class 和 qtcloud-pay 端到端测试。"""

from __future__ import annotations

import json

import pytest

from .conftest import http_get, http_post


class TestClassLifecycle:
    """教学班级 (Class) 生命周期系统测试。"""

    def _create_program(self, url: str) -> str:
        status, resp = http_post(url, data={"name": "e2e-班级测试专业"})
        assert status == 201
        return json.loads(resp)["id"]

    def _create_class(self, url: str, name: str, ref_id: str, ref_type: str = "program") -> dict:
        body = {
            "name": name,
            "refName": "e2e-班级测试专业",
            "refType": ref_type,
            "refId": ref_id,
            "status": "preparing",
            "startDate": "2026-09-01",
            "endDate": "2027-01-15",
        }
        status, resp = http_post(f"{url}/classes", data=body)
        assert status == 201, f"create class failed: {resp}"
        return json.loads(resp)

    def test_create_class(self, course_service):
        """创建教学班级。"""
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

        # active
        status, resp = http_post(
            f"{course_service}/classes",
            data={
                "name": cls["name"],
                "refName": cls["refName"],
                "refType": cls["refType"],
                "refId": cls["refId"],
                "status": "active",
                "startDate": cls["startDate"],
                "endDate": cls["endDate"],
            },
        )
        # PUT 更新
        import urllib.request

        req = urllib.request.Request(
            f"{course_service}/classes/{cid}",
            data=json.dumps({
                "name": cls["name"],
                "refName": cls["refName"],
                "refType": cls["refType"],
                "refId": cls["refId"],
                "status": "active",
                "startDate": cls["startDate"],
                "endDate": cls["endDate"],
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            updated = json.loads(r.read().decode())
        assert updated["status"] == "active"

        # ended
        req = urllib.request.Request(
            f"{course_service}/classes/{cid}",
            data=json.dumps({
                "name": cls["name"],
                "refName": cls["refName"],
                "refType": cls["refType"],
                "refId": cls["refId"],
                "status": "ended",
                "startDate": cls["startDate"],
                "endDate": cls["endDate"],
                "studentCount": 30,
                "progress": 1.0,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            ended = json.loads(r.read().decode())
        assert ended["status"] == "ended"
        assert ended["studentCount"] == 30
        assert ended["progress"] == 1.0

    def test_list_classes(self, course_service):
        """列出所有班级。"""
        status, resp = http_get(f"{course_service}/classes")
        assert status == 200
        classes = json.loads(resp)
        assert isinstance(classes, list)

    def test_get_nonexistent_class(self, course_service):
        """查询不存在的 Class 应返回 404。"""
        status, body = http_get(f"{course_service}/classes/nonexistent")
        assert status == 404


class TestPayFlow:
    """支付服务系统测试。"""

    def test_pay_create(self, pay_service):
        """发起支付订单。"""
        body = {
            "OrderID": "E2E-ORD-001",
            "Amount": 199.99,
            "Subject": "大数据微专业 - 报名费",
            "NotifyURL": "https://qtclass.example.com/pay/notify",
        }
        status, resp = http_post(f"{pay_service}/pay", data=body)
        assert status == 200, f"pay failed: {resp}"
        data = json.loads(resp)
        assert "TradeID" in data
        assert data["TradeID"] != ""

    def test_pay_invalid_body(self, pay_service):
        """无效请求体应返回 400。"""
        import urllib.request

        req = urllib.request.Request(
            f"{pay_service}/pay",
            data=b"not-json",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            assert e.code == 400

    def test_query_order(self, pay_service):
        """查询支付订单。"""
        # 先创建订单
        body = {
            "OrderID": "E2E-ORD-QUERY-001",
            "Amount": 99.00,
            "Subject": "测试查询",
        }
        http_post(f"{pay_service}/pay", data=body)

        # 查询
        status, resp = http_get(f"{pay_service}/query/E2E-ORD-QUERY-001")
        assert status == 200, f"query failed: {resp}"
        data = json.loads(resp)
        assert data["OrderID"] == "E2E-ORD-QUERY-001"
        assert data["Status"] == "SUCCESS"

    def test_refund(self, pay_service):
        """发起退款。"""
        # 先创建订单
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": "E2E-ORD-REF-001", "Amount": 299.00, "Subject": "退款测试"},
        )
        # 退款
        status, resp = http_post(
            f"{pay_service}/refund",
            data={"OrderID": "E2E-ORD-REF-001", "RefundAmount": 299.00, "Reason": "学员退课"},
        )
        assert status == 200, f"refund failed: {resp}"
        data = json.loads(resp)
        assert "RefundID" in data
        assert data["Status"] == "SUCCESS"
