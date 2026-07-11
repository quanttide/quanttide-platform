"""课堂端到端流程测试。

围绕课堂真实调用场景，覆盖教师后台操作到学员上课的完整链路。
"""

from __future__ import annotations

import json
import urllib.request

import pytest

from .conftest import ADMIN_PASSWORD, http_get, http_post


class TestTeacherPreparesClass:
    """教师开课备课流程。

    1. 创建课程体系（Program → Course → Lesson → Scene）
    2. 创建教学班级
    3. 验证备课内容完整可查
    """

    def test_teacher_creates_curriculum(self, auth_service, course_service, auth_token):
        """教师创建完整的课程体系。"""
        # ── 创建 Program ──
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "大数据微专业", "description": "2026秋季班", "status": "draft"},
        )
        assert status == 201
        program = json.loads(resp)
        pid = program["id"]
        assert program["name"] == "大数据微专业"

        # ── 创建两门 Course ──
        status, resp = http_post(
            f"{course_service}/courses",
            data={"name": "Python 数据科学", "status": "draft"},
        )
        assert status == 201
        cid1 = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/courses",
            data={"name": "SQL 数据分析", "status": "draft"},
        )
        assert status == 201
        cid2 = json.loads(resp)["id"]

        # ── Program 关联 Course ──
        req = urllib.request.Request(
            f"{course_service}/programs/{pid}",
            data=json.dumps({
                "id": pid,
                "name": "大数据微专业",
                "description": "2026秋季班",
                "status": "published",
                "courseIds": [cid1, cid2],
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            updated = json.loads(r.read().decode())
        assert cid1 in updated["courseIds"]
        assert cid2 in updated["courseIds"]

        # ── 为第一门 Course 创建 Lesson ──
        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "Pandas 基础", "duration": 90, "status": "published"},
        )
        assert status == 201
        lid = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "数据清洗实战", "duration": 90, "status": "published"},
        )
        assert status == 201
        lid2 = json.loads(resp)["id"]

        # Course 关联 Lesson
        req = urllib.request.Request(
            f"{course_service}/courses/{cid1}",
            data=json.dumps({
                "id": cid1,
                "name": "Python 数据科学",
                "status": "published",
                "lessonIds": [lid, lid2],
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            updated_course = json.loads(r.read().decode())
        assert lid in updated_course["lessonIds"]
        assert lid2 in updated_course["lessonIds"]

        # ── 为 Lesson 创建 Scene（互动视频片段） ──
        status, resp = http_post(
            f"{course_service}/scenes",
            data={
                "lessonId": lid,
                "videoUrl": "https://media.example.com/pandas-intro.mp4",
                "choices": [],
            },
        )
        assert status == 201
        scene1_id = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/scenes",
            data={
                "lessonId": lid,
                "videoUrl": "https://media.example.com/pandas-advanced.mp4",
                "choices": [
                    {"label": "继续学习", "targetSceneId": ""},
                    {"label": "重新观看", "targetSceneId": scene1_id},
                ],
            },
        )
        assert status == 201

        # ── 验证完整链路可查询 ──
        # 查 Program
        status, resp = http_get(f"{course_service}/programs/{pid}")
        assert status == 200
        final_program = json.loads(resp)
        assert len(final_program["courseIds"]) == 2

        # 查 Course
        status, resp = http_get(f"{course_service}/courses/{cid1}")
        assert status == 200
        final_course = json.loads(resp)
        assert len(final_course["lessonIds"]) == 2

        # 按 lessonId 查 Scene
        status, resp = http_get(f"{course_service}/scenes?lessonId={lid}")
        assert status == 200
        scenes = json.loads(resp)
        assert len(scenes) == 2
        assert scenes[0]["videoUrl"] != ""

    def test_teacher_creates_class(self, course_service):
        """教师创建教学班级并开始招生。"""
        # 先创建 Program 供班级引用
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "大数据微专业", "status": "published"},
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        # 创建班级
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
        cls = json.loads(resp)
        cid = cls["id"]
        assert cls["status"] == "preparing"

        # 验证班级出现在列表中
        status, resp = http_get(f"{course_service}/classes")
        assert status == 200
        classes = json.loads(resp)
        assert any(c["id"] == cid for c in classes)


class TestStudentEnrollsAndAttends:
    """学员报名与上课流程。

    1. 学员登录 → 课程展示 → 支付报名
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
        program = json.loads(resp)
        pid = program["id"]

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
        cls = json.loads(resp)
        class_id = cls["id"]

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
        pay_resp = json.loads(resp)
        assert pay_resp["TradeID"] != ""

        # ── 查询支付结果 ──
        status, resp = http_get(f"{pay_service}/query/{order_id}")
        assert status == 200
        query = json.loads(resp)
        assert query["OrderID"] == order_id
        assert query["Status"] == "SUCCESS"

    def test_class_starts_and_ends(self, course_service, pay_service):
        """班级开课 → 上课 → 结课完整流程。"""
        # ── 准备课程和班级 ──
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "数据科学实训营", "status": "published"},
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        status, resp = http_post(
            f"{course_service}/courses",
            data={"name": "机器学习入门", "status": "published"},
        )
        assert status == 201
        cid = json.loads(resp)["id"]

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

        # ── 学员报名 ──
        order_id = f"ENROLL-{pid}-{class_id[:8]}"
        http_post(
            f"{pay_service}/pay",
            data={"OrderID": order_id, "Amount": 2999.00, "Subject": "实训营报名"},
        )

        # ── 开课（班级状态 active） ──
        req = urllib.request.Request(
            f"{course_service}/classes/{class_id}",
            data=json.dumps({
                "name": cls["name"],
                "refName": cls["refName"],
                "refType": cls["refType"],
                "refId": cls["refId"],
                "status": "active",
                "startDate": cls["startDate"],
                "endDate": cls["endDate"],
                "studentCount": 15,
                "progress": 0.0,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            active = json.loads(r.read().decode())
        assert active["status"] == "active"
        assert active["studentCount"] == 15
        assert active["progress"] == 0.0

        # ── 上课一段时间，进度推进 ──
        req = urllib.request.Request(
            f"{course_service}/classes/{class_id}",
            data=json.dumps({
                "name": cls["name"],
                "refName": cls["refName"],
                "refType": cls["refType"],
                "refId": cls["refId"],
                "status": "active",
                "startDate": cls["startDate"],
                "endDate": cls["endDate"],
                "studentCount": 15,
                "progress": 0.6,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            progressing = json.loads(r.read().decode())
        assert progressing["progress"] == 0.6

        # ── 结课 ──
        req = urllib.request.Request(
            f"{course_service}/classes/{class_id}",
            data=json.dumps({
                "name": cls["name"],
                "refName": cls["refName"],
                "refType": cls["refType"],
                "refId": cls["refId"],
                "status": "ended",
                "startDate": cls["startDate"],
                "endDate": cls["endDate"],
                "studentCount": 15,
                "progress": 1.0,
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            ended = json.loads(r.read().decode())
        assert ended["status"] == "ended"
        assert ended["progress"] == 1.0


class TestAuthGate:
    """课堂身份认证场景。

    教师/学员登录、身份校验、非法访问拦截。
    """

    def test_teacher_login_and_query(self, auth_service, auth_token):
        """教师登录后可查询课程内容。"""
        status, resp = http_get(f"{auth_service}/userinfo", token=auth_token)
        assert status == 200
        info = json.loads(resp)
        assert info["sub"] != ""

    def test_unauthenticated_access_blocked(self, auth_service):
        """未登录用户无法访问用户信息。"""
        status, body = http_get(f"{auth_service}/userinfo")
        assert status == 401


class TestSceneTeaching:
    """互动课堂授课场景。

    包含视频场景创建、分支选择、按课时查询等教学操作。
    """

    def test_teacher_creates_interactive_lesson(self, course_service):
        """教师创建互动课时，含视频片段和分支选项。"""
        # ── 创建 Lesson ──
        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "变量与数据类型", "duration": 45, "status": "published"},
        )
        assert status == 201
        lid = json.loads(resp)["id"]

        # ── 创建开场 Scene ──
        status, resp = http_post(
            f"{course_service}/scenes",
            data={
                "lessonId": lid,
                "videoUrl": "https://media.example.com/variables-intro.mp4",
                "choices": [
                    {"label": "继续", "targetSceneId": ""},
                ],
            },
        )
        assert status == 201
        opening_scene = json.loads(resp)
        opening_id = opening_scene["id"]

        # ── 创建第二个带分支的 Scene ──
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
        assert json.loads(resp)["id"] != ""

        # ── 按课时查询所有 Scene ──
        status, resp = http_get(f"{course_service}/scenes?lessonId={lid}")
        assert status == 200
        scenes = json.loads(resp)
        assert len(scenes) == 2

    def test_scene_requires_lesson_id(self, course_service):
        """查询场景时必须提供 lessonId。"""
        status, body = http_get(f"{course_service}/scenes")
        assert status == 400
