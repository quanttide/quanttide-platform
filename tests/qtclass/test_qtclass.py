"""前台课堂端到端流程测试。

覆盖教师上课、学员报名参与、互动授课等课堂真实场景。
后台运维操作（课程配置、班级管理、支付管理）见 test_admin.py。
"""

from __future__ import annotations

import json
import urllib.request

import pytest

from .conftest import http_get, http_post


class TestStudentEnrollsAndAttends:
    """学员报名与上课流程。

    1. 查看课程 → 支付报名
    2. 班级开课 → 开始上课
    3. 完成课时 → 结课
    """

    def test_student_enrolls(self, course_service, pay_service):
        """学员查看课程信息并支付报名。"""
        # ── 准备：教师已创建好课程和班级 ──
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "大数据微专业", "status": "published", "description": "2026秋季班"},
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/classes",
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
        class_id = json.loads(resp)["id"]

        # ── 学员支付报名费 ──
        order_id = f"ENROLL-{pid}-{class_id[:8]}"
        status, resp = http_post(
            f"{pay_service}/pay",
            data={
                "OrderID": order_id,
                "Amount": 1999.00,
                "Subject": "大数据微专业 - 2026秋班级报名",
                "NotifyURL": "https://qtclass.example.com/pay/notify",
            },
        )
        assert status == 200
        assert json.loads(resp)["TradeID"] != ""

        # ── 查询支付结果 ──
        status, resp = http_get(f"{pay_service}/query/{order_id}")
        assert status == 200
        query = json.loads(resp)
        assert query["OrderID"] == order_id
        assert query["Status"] == "SUCCESS"

    def test_class_starts_and_ends(self, course_service, pay_service):
        """班级开课 → 上课推进 → 结课完整流程。"""
        # ── 准备 ──
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "数据科学实训营", "status": "published"},
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/classes",
            data={
                "name": "数据科学实训营-10月班",
                "refName": "数据科学实训营",
                "refType": "program",
                "refId": pid,
                "status": "preparing",
                "startDate": "2026-10-01",
                "endDate": "2026-12-31",
            },
        )
        assert status == 201
        cls = json.loads(resp)
        class_id = cls["id"]

        # 学员报名
        order_id = f"ENROLL-{pid}-{class_id[:8]}"
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": order_id, "Amount": 2999.00, "Subject": "实训营报名"},
        )

        # ── 开课（班级状态 → active） ──
        req = urllib.request.Request(
            f"{course_service}/classes/{class_id}",
            data=json.dumps({
                "name": cls["name"], "refName": cls["refName"],
                "refType": cls["refType"], "refId": cls["refId"],
                "status": "active",
                "startDate": cls["startDate"], "endDate": cls["endDate"],
                "studentCount": 15, "progress": 0.0,
            }).encode(),
            headers={"Content-Type": "application/json"}, method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            active = json.loads(r.read().decode())
        assert active["status"] == "active"
        assert active["studentCount"] == 15

        # ── 上课中，进度推进 ──
        req = urllib.request.Request(
            f"{course_service}/classes/{class_id}",
            data=json.dumps({
                "name": cls["name"], "refName": cls["refName"],
                "refType": cls["refType"], "refId": cls["refId"],
                "status": "active",
                "startDate": cls["startDate"], "endDate": cls["endDate"],
                "studentCount": 15, "progress": 0.6,
            }).encode(),
            headers={"Content-Type": "application/json"}, method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            assert json.loads(r.read().decode())["progress"] == 0.6

        # ── 结课（班级状态 → ended） ──
        req = urllib.request.Request(
            f"{course_service}/classes/{class_id}",
            data=json.dumps({
                "name": cls["name"], "refName": cls["refName"],
                "refType": cls["refType"], "refId": cls["refId"],
                "status": "ended",
                "startDate": cls["startDate"], "endDate": cls["endDate"],
                "studentCount": 15, "progress": 1.0,
            }).encode(),
            headers={"Content-Type": "application/json"}, method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            ended = json.loads(r.read().decode())
        assert ended["status"] == "ended"
        assert ended["progress"] == 1.0


class TestSceneTeaching:
    """互动课堂授课场景。

    教师在上课过程中创建互动视频片段、设置分支选项。
    """

    def test_teacher_creates_interactive_lesson(self, course_service):
        """教师创建互动课时，含视频片段和分支选项。"""
        # 创建 Lesson
        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "变量与数据类型", "duration": 45, "status": "published"},
        )
        assert status == 201
        lid = json.loads(resp)["id"]

        # 创建开场 Scene
        status, resp = http_post(
            f"{course_service}/scenes",
            data={
                "lessonId": lid,
                "videoUrl": "https://media.example.com/variables-intro.mp4",
                "choices": [{"label": "继续", "targetSceneId": ""}],
            },
        )
        assert status == 201
        opening_id = json.loads(resp)["id"]

        # 创建第二个带分支的 Scene
        status, resp = http_post(
            f"{course_service}/scenes",
            data={
                "lessonId": lid,
                "videoUrl": "https://media.example.com/variables-quiz.mp4",
                "choices": [
                    {"label": "回答正确，继续", "targetSceneId": ""},
                    {"label": "再看一遍讲解", "targetSceneId": opening_id},
                ],
            },
        )
        assert status == 201

        # 按课时查询所有 Scene
        status, resp = http_get(f"{course_service}/scenes?lessonId={lid}")
        assert status == 200
        assert len(json.loads(resp)) == 2

    def test_scene_requires_lesson_id(self, course_service):
        """查询场景时必须提供 lessonId。"""
        status, body = http_get(f"{course_service}/scenes")
        assert status == 400
