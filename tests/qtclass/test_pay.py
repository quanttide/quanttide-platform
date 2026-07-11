"""qtcloud-course Class（班级）与 qtcloud-pay（支付）端到端测试。"""

from __future__ import annotations

import json
import urllib.request

import pytest

from .conftest import http_get, http_post


class TestClassLifecycle:
    """教学班级 (Class) 生命周期系统测试。"""

    def _create_class(self, url: str, name: str, ref_id: str) -> dict:
        status, resp = http_post(
            f"{url}/classes",
            data={
                "name": name,
                "refName": "参考专业",
                "refType": "program",
                "refId": ref_id,
                "status": "preparing",
                "startDate": "2026-09-01",
                "endDate": "2027-01-15",
            },
        )
        assert status == 201
        return json.loads(resp)

    def test_create_class(self, course_service):
        """创建教学班级。"""
        # 先创建 Program 作为引用
        status, resp = http_post(
            f"{course_service}/programs", data={"name": "e2e-班级测试专业"}
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        cls = self._create_class(course_service, "2026秋-大数据班", pid)
        assert cls["name"] == "2026秋-大数据班"
        assert cls["refType"] == "program"
        assert cls["refId"] == pid
        assert cls["status"] == "preparing"

    def test_class_status_transition(self, course_service):
        """班级状态流转：preparing → active → ended。"""
        status, resp = http_post(
            f"{course_service}/programs", data={"name": "状态流转测试专业"}
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        cls = self._create_class(course_service, "状态流转测试班", pid)
        cid = cls["id"]

        # preparing → active
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
                "studentCount": 20,
                "progress": 0.0,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            updated = json.loads(r.read().decode())
        assert updated["status"] == "active"

        # active → ended
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
                "studentCount": 20,
                "progress": 1.0,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            ended = json.loads(r.read().decode())
        assert ended["status"] == "ended"
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

    def test_delete_class(self, course_service):
        """删除班级。"""
        status, resp = http_post(
            f"{course_service}/programs", data={"name": "delete-class-test"}
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        cls = self._create_class(course_service, "待删除班级", pid)
        cid = cls["id"]

        req = urllib.request.Request(
            f"{course_service}/classes/{cid}", method="DELETE",
        )
        with urllib.request.urlopen(req) as r:
            assert r.status == 204


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
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": "E2E-ORD-QUERY-001", "Amount": 99.00, "Subject": "测试查询"},
        )
        status, resp = http_get(f"{pay_service}/query/E2E-ORD-QUERY-001")
        assert status == 200, f"query failed: {resp}"
        data = json.loads(resp)
        assert data["OrderID"] == "E2E-ORD-QUERY-001"
        assert data["Status"] == "SUCCESS"

    def test_refund(self, pay_service):
        """发起退款。"""
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": "E2E-ORD-REF-001", "Amount": 299.00, "Subject": "退款测试"},
        )
        status, resp = http_post(
            f"{pay_service}/refund",
            data={"OrderID": "E2E-ORD-REF-001", "RefundAmount": 299.00, "Reason": "学员退课"},
        )
        assert status == 200, f"refund failed: {resp}"
        data = json.loads(resp)
        assert "RefundID" in data
        assert data["Status"] == "SUCCESS"

    def test_refund_invalid_body(self, pay_service):
        """退款请求体缺失应返回 400。"""
        req = urllib.request.Request(
            f"{pay_service}/refund",
            data=b"",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            assert e.code == 400
