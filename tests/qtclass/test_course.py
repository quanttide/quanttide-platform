"""qtcloud-course 课程与课时端到端测试。"""

from __future__ import annotations

import json
import urllib.request

import pytest

from .conftest import http_get, http_post


class TestProgramCurd:
    """Program/Course/Lesson 独立 CRUD（扁平资源，通过 ID 列表关联）。"""

    def test_create_program(self, course_service):
        """创建专业 (Program)。"""
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "e2e-测试专业", "description": "测试"},
        )
        assert status == 201
        data = json.loads(resp)
        assert data["name"] == "e2e-测试专业"
        assert "id" in data

    def test_program_crud_flow(self, course_service):
        """完整的 Program → Course → Lesson 三级创建与关联。"""
        # 1. 创建 Program
        status, resp = http_post(
            f"{course_service}/programs",
            data={"name": "大数据微专业", "status": "published"},
        )
        assert status == 201
        pid = json.loads(resp)["id"]

        # 2. 创建 Course（扁平资源）
        status, resp = http_post(
            f"{course_service}/courses",
            data={"name": "Python 基础", "status": "draft"},
        )
        assert status == 201
        cid = json.loads(resp)["id"]

        # 3. 创建 Lesson（扁平资源）
        status, resp = http_post(
            f"{course_service}/lessons",
            data={"title": "变量与类型", "duration": 45},
        )
        assert status == 201
        lid = json.loads(resp)["id"]

        # 4. 建立关联：Program.courseIds = [cid], Course.lessonIds = [lid]
        req = urllib.request.Request(
            f"{course_service}/programs/{pid}",
            data=json.dumps({
                "id": pid,
                "name": "大数据微专业",
                "status": "published",
                "courseIds": [cid],
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            updated_program = json.loads(r.read().decode())
        assert cid in updated_program["courseIds"]

        req = urllib.request.Request(
            f"{course_service}/courses/{cid}",
            data=json.dumps({
                "id": cid,
                "name": "Python 基础",
                "status": "published",
                "lessonIds": [lid],
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req) as r:
            updated_course = json.loads(r.read().decode())
        assert lid in updated_course["lessonIds"]

        # 5. 列表查询
        status, resp = http_get(f"{course_service}/programs")
        assert status == 200
        programs = json.loads(resp)
        assert any(p["id"] == pid for p in programs)

        status, resp = http_get(f"{course_service}/courses")
        assert status == 200
        courses = json.loads(resp)
        assert any(c["id"] == cid for c in courses)

        status, resp = http_get(f"{course_service}/lessons")
        assert status == 200
        lessons = json.loads(resp)
        assert any(l["id"] == lid for l in lessons)

        # 6. 获取单个
        status, resp = http_get(f"{course_service}/programs/{pid}")
        assert status == 200
        status, resp = http_get(f"{course_service}/courses/{cid}")
        assert status == 200
        status, resp = http_get(f"{course_service}/lessons/{lid}")
        assert status == 200

    def test_get_nonexistent_program(self, course_service):
        """查询不存在的 Program 应返回 404。"""
        status, body = http_get(f"{course_service}/programs/nonexistent")
        assert status == 404

    def test_create_program_missing_name(self, course_service):
        """创建 Program 缺少 name 应返回 400。"""
        status, resp = http_post(
            f"{course_service}/programs", data={"description": "no name"}
        )
        assert status == 400

    def test_create_course_missing_name(self, course_service):
        """创建 Course 缺少 name 应返回 400。"""
        status, resp = http_post(
            f"{course_service}/courses", data={"status": "draft"}
        )
        assert status == 400

    def test_create_lesson_missing_title(self, course_service):
        """创建 Lesson 缺少 title 应返回 400。"""
        status, resp = http_post(
            f"{course_service}/lessons", data={"duration": 45}
        )
        assert status == 400
