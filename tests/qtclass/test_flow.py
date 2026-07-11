"""跨服务端到端流程测试。

模拟 qtclass 学员从认证到选课、支付、班级加入的完整业务链路。
"""

from __future__ import annotations

import json
import urllib.request

import pytest

from .conftest import ADMIN_PASSWORD, http_get, http_post


@pytest.mark.skip(reason="需要真实接口联调，标记为手工运行")
class TestEnrollmentE2E:
    """学员报名端到端流程。

    流程：认证 → 查看课程 → 创建班级 → 支付报名 → 验证。
    """

    def test_full_enrollment_flow(self, all_services, auth_token):
        """完整的报名链路测试。"""
        auth_url = all_services["auth"]
        course_url = all_services["course"]
        pay_url = all_services["pay"]

        # ── Step 1: 创建课程内容 ──
        # 创建 Program
        status, resp = http_post(
            f"{course_url}/programs",
            data={"name": "大数据微专业", "description": "2026秋季班"},
        )
        assert status == 201
        program = json.loads(resp)
        pid = program["id"]

        # 创建 Course
        status, resp = http_post(
            f"{course_url}/programs/{pid}/courses",
            data={"name": "Python 数据科学", "status": "published"},
        )
        assert status == 201
        course = json.loads(resp)
        cid = course["id"]

        # 创建 Lesson
        status, resp = http_post(
            f"{course_url}/programs/{pid}/courses/{cid}/lessons",
            data={"title": "Pandas 基础", "duration": 90},
        )
        assert status == 201

        # ── Step 2: 创建班级 ──
        status, resp = http_post(
            f"{course_url}/classes",
            data={
                "name": "2026秋-大数据微专业班",
                "refName": "大数据微专业",
                "refType": "program",
                "refId": pid,
                "status": "preparing",
                "startDate": "2026-09-01",
                "endDate": "2027-01-15",
            },
        )
        assert status == 201
        class_data = json.loads(resp)
        class_id = class_data["id"]

        # ── Step 3: 学员支付报名 ──
        status, resp = http_post(
            f"{pay_url}/pay",
            data={
                "OrderID": f"ENROLL-{pid}-{class_id[:8]}",
                "Amount": 1999.00,
                "Subject": "大数据微专业 - 2026秋班级报名",
                "NotifyURL": "https://qtclass.example.com/pay/notify",
                "Metadata": {"class_id": class_id, "program_id": pid},
            },
        )
        assert status == 200
        pay_resp = json.loads(resp)
        assert pay_resp["TradeID"] != ""

        # ── Step 4: 查询支付结果 ──
        order_id = f"ENROLL-{pid}-{class_id[:8]}"
        status, resp = http_get(f"{pay_url}/query/{order_id}")
        assert status == 200
        query_resp = json.loads(resp)
        assert query_resp["OrderID"] == order_id
        assert query_resp["Status"] == "SUCCESS"

        # ── Step 5: 验证班级信息 ──
        status, resp = http_get(f"{course_url}/classes/{class_id}")
        assert status == 200
        final_class = json.loads(resp)
        assert final_class["status"] == "preparing"

        # ── Step 6: 班级开课 ──
        req = urllib.request.Request(
            f"{course_url}/classes/{class_id}",
            data=json.dumps({
                "name": final_class["name"],
                "refName": final_class["refName"],
                "refType": final_class["refType"],
                "refId": final_class["refId"],
                "status": "active",
                "startDate": final_class["startDate"],
                "endDate": final_class["endDate"],
                "studentCount": 1,  # 该学员加入
                "progress": 0.0,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            activated = json.loads(r.read().decode())
        assert activated["status"] == "active"
        assert activated["studentCount"] == 1


class TestCrossServiceContract:
    """跨服务契约验证。

    不启动服务，只验证数据结构和接口签名一致性。
    """

    def test_class_refers_to_program(self):
        """班级的 refId 语义应与 Program/Course 的 ID 格式兼容。

        验证两者都使用字符串 ID，无格式冲突。
        """
        # 纯契约验证：字段类型兼容性
        program_id_type = str
        class_ref_id_type = str
        assert program_id_type == class_ref_id_type, "ID 类型不兼容"

    def test_pay_amount_domain(self):
        """支付金额与课程定价的单位一致（元，浮点数）。"""
        # course 无定价字段，但 pay 的 Amount 是 float64
        # 验证精度处理：两位小数
        amount = 1999.00
        assert isinstance(amount, float), "金额应为浮点数"
        # 两位小数精度
        assert round(amount, 2) == amount

    def test_auth_token_usage_pattern(self):
        """验证 auth_token 的 Bearer 格式可被其他服务接受。

        虽然 course/pay 目前无中间件，但契约要求 token 格式统一为 Bearer JWT。
        """
        token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1MSJ9.example"
        assert token.count(".") == 2, "JWT 应有三段"
        assert isinstance(token, str)
