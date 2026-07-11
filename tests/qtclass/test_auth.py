"""qtcloud-auth 端到端测试。"""

from __future__ import annotations

import json

import pytest

from .conftest import ADMIN_PASSWORD, http_get, http_post


class TestAuthFlow:
    """身份认证服务系统测试。"""

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
        assert "access_token" in data, f"no access_token: {data}"
        assert data["token_type"] == "Bearer"
        assert "expires_in" in data
        # JWT 格式校验
        token = data["access_token"]
        parts = token.split(".")
        assert len(parts) == 3, "not a valid JWT (expected 3 parts)"

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
        assert status == 401, f"expected 401, got {status}: {body}"

    def test_userinfo(self, auth_service, auth_token):
        """用 access_token 获取用户信息。"""
        status, body = http_get(f"{auth_service}/userinfo", token=auth_token)
        assert status == 200, f"status={status} body={body}"
        data = json.loads(body)
        assert data["sub"], f"no sub in userinfo: {data}"
        assert "phone" in data
        assert "nickname" in data

    def test_userinfo_no_token(self, auth_service):
        """无 token 访问 userinfo 应返回 401。"""
        status, body = http_get(f"{auth_service}/userinfo")
        assert status == 401, f"expected 401, got {status}: {body}"

    def test_unsupported_grant_type(self, auth_service):
        """不支持的 grant_type 应返回 400。"""
        status, body = http_post(
            f"{auth_service}/oauth/token",
            form={"grant_type": "client_credentials"},
        )
        assert status == 400, f"expected 400, got {status}: {body}"
