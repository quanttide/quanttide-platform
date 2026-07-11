"""qtcloud-course 端到端测试。"""

from __future__ import annotations

import json

import pytest

from .conftest import http_get, http_post


class TestProgramCurd:
    """Program → Course → Lesson 三级 CRUD 系统测试。"""

    def _create_program(self, url: str, name: str) -> tuple[str, dict]:
        body = json.dumps({"name": name, "description": f"{name} description"})
        status, resp = http_post(f"{url}/programs", data=json.loads(body))
        assert status == 201, f"create program failed: {resp}"
        data = json.loads(resp)
        return data["id"], data

    def _create_course(self, url: str, program_id: str, name: str) -> tuple[str, dict]:
        body = json.dumps({"name": name, "status": "draft"})
        status, resp = http_post(
            f"{url}/programs/{program_id}/courses", data=json.loads(body)
        )
        assert status == 201, f"create course failed: {resp}"
        data = json.loads(resp)
        return data["id"], data

    def _create_lesson(self, url: str, program_id: str, course_id: str, title: str) -> tuple[str, dict]:
        body = json.dumps({"title": title, "duration": 45})
        status, resp = http_post(
            f"{url}/programs/{program_id}/courses/{course_id}/lessons",
            data=json.loads(body),
        )
        assert status == 201, f"create lesson failed: {resp}"
        data = json.loads(resp)
        return data["id"], data

    def test_create_program(self, course_service):
        """创建专业 (Program)。"""
        pid, data = self._create_program(course_service, "e2e-测试专业")
        assert data["name"] == "e2e-测试专业"
        assert "id" in data

    def test_program_crud_flow(self, course_service):
        """完整的 Program → Course → Lesson 三级 CRUD 流程。"""
        url = course_service

        # 1. 创建 Program
        pid, program = self._create_program(url, "大数据微专业")
        assert program["name"] == "大数据微专业"
        assert program["status"] == "" or program["status"] is None

        # 2. 创建 Course
        cid, course = self._create_course(url, pid, "Python 基础")
        assert course["name"] == "Python 基础"
        assert course["status"] == "draft"

        # 3. 创建 Lesson
        lid, lesson = self._create_lesson(url, pid, cid, "变量与类型")
        assert lesson["title"] == "变量与类型"
        assert lesson["duration"] == 45

        # 4. 列表查询
        status, resp = http_get(f"{url}/programs")
        assert status == 200
        programs = json.loads(resp)
        assert any(p["id"] == pid for p in programs)

        status, resp = http_get(f"{url}/programs/{pid}/courses")
        assert status == 200
        courses = json.loads(resp)
        assert any(c["id"] == cid for c in courses)

        status, resp = http_get(f"{url}/programs/{pid}/courses/{cid}/lessons")
        assert status == 200
        lessons = json.loads(resp)
        assert any(l["id"] == lid for l in lessons)

        # 5. 获取单个
        status, resp = http_get(f"{url}/programs/{pid}")
        assert status == 200

        status, resp = http_get(f"{url}/programs/{pid}/courses/{cid}")
        assert status == 200

        status, resp = http_get(f"{url}/programs/{pid}/courses/{cid}/lessons/{lid}")
        assert status == 200

    def test_get_nonexistent_program(self, course_service):
        """查询不存在的 Program 应返回 404。"""
        status, body = http_get(f"{course_service}/programs/nonexistent")
        assert status == 404, f"expected 404, got {status}: {body}"

    def test_create_program_missing_name(self, course_service):
        """创建 Program 缺少 name 应返回 400。"""
        body = json.dumps({"description": "no name"})
        status, resp = http_post(
            f"{course_service}/programs", data=json.loads(body)
        )
        assert status == 400, f"expected 400, got {status}: {resp}"
