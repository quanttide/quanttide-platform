"""qtclass 端到端测试 — fixtures."""

from __future__ import annotations

import json
import logging
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

# ── 路径常量 ──
REPO_ROOT = Path(__file__).resolve().parents[2]
AUTH_DIR = REPO_ROOT / "apps" / "qtcloud-auth" / "src" / "provider"
COURSE_DIR = REPO_ROOT / "apps" / "qtcloud-course" / "src" / "provider"
PAY_DIR = REPO_ROOT / "apps" / "qtcloud-pay" / "src" / "provider"

# ── 端口配置 ──
AUTH_PORT = 9180
COURSE_PORT = 9181
PAY_PORT = 9182

AUTH_URL = f"http://127.0.0.1:{AUTH_PORT}"
COURSE_URL = f"http://127.0.0.1:{COURSE_PORT}"
PAY_URL = f"http://127.0.0.1:{PAY_PORT}"

ADMIN_PASSWORD = "e2e-test-2026"
E2E_TOKEN = ""

SERVICE_START_TIMEOUT = 15  # 秒


# ── HTTP 请求辅助 ──


def http_get(url: str, token: str | None = None, expect: int = 200) -> tuple[int, str]:
    """GET 请求并返回 (status, body)。"""
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        logger.debug("GET %s -> %d: %s", url, e.code, body)
        return e.code, body


def http_post(
    url: str,
    data: dict | None = None,
    form: dict | None = None,
    token: str | None = None,
    expect: int = 200,
) -> tuple[int, str]:
    """POST 请求并返回 (status, body)。"""
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
    else:
        body = json.dumps(data or {}).encode()
        headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        logger.debug("POST %s -> %d: %s", url, e.code, body)
        return e.code, body


# ── 服务生命周期 ──


def _start_service(label: str, workdir: Path, env: dict | None = None) -> subprocess.Popen:
    """启动 Go 服务并返回进程对象。"""
    merged_env = os.environ.copy()
    merged_env.pop("JWT_SECRET", None)  # 用默认值
    merged_env.pop("ADMIN_PASSWORD", None)
    if env:
        merged_env.update(env)
    logger.info("Starting %s service in %s ...", label, workdir)
    proc = subprocess.Popen(
        ["go", "run", "."],
        cwd=workdir,
        env=merged_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc


def _wait_for_health(url: str, label: str, timeout: int = SERVICE_START_TIMEOUT) -> None:
    """轮询 /healthz 直到服务可用。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            status, body = http_get(f"{url}/healthz")
            if status == 200:
                logger.info("  %s ready at %s", label, url)
                return
        except Exception:
            pass
        time.sleep(0.3)
    pytest.fail(f"{label} did not start within {timeout}s")


def _stop_service(proc: subprocess.Popen, label: str) -> None:
    """停止服务进程。"""
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    logger.info("  %s stopped (exit=%s)", label, proc.returncode)


# ── pytest hooks ──


@pytest.fixture(scope="session")
def auth_service():
    """启动 qtcloud-auth 服务（session 级）。"""
    env = {
        "LISTEN_ADDR": f":{AUTH_PORT}",
        "ADMIN_PASSWORD": ADMIN_PASSWORD,
        "JWT_SECRET": "e2e-test-secret",
    }
    proc = _start_service("auth", AUTH_DIR, env)
    _wait_for_health(f"http://127.0.0.1:{AUTH_PORT}", "auth")
    yield AUTH_URL
    _stop_service(proc, "auth")


@pytest.fixture(scope="session")
def course_service():
    """启动 qtcloud-course 服务（session 级）。"""
    env = {"LISTEN_ADDR": f":{COURSE_PORT}"}
    proc = _start_service("course", COURSE_DIR, env)
    _wait_for_health(COURSE_URL, "course")
    yield COURSE_URL
    _stop_service(proc, "course")


@pytest.fixture(scope="session")
def pay_service():
    """启动 qtcloud-pay 服务（session 级）。"""
    env = {"LISTEN_ADDR": f":{PAY_PORT}"}
    proc = _start_service("pay", PAY_DIR, env)
    time.sleep(1)  # pay 无 healthz, 等启动
    yield PAY_URL
    _stop_service(proc, "pay")


# ── 测试客户端 fixture ──


@pytest.fixture(scope="session")
def auth_token(auth_service):
    """通过密码授权获取 admin 的 access_token。"""
    status, body = http_post(
        f"{auth_service}/oauth/token",
        form={"grant_type": "password", "username": "admin", "password": ADMIN_PASSWORD},
    )
    assert status == 200, f"auth failed: {body}"
    data = json.loads(body)
    token = data.get("access_token")
    assert token, f"no access_token in response: {data}"
    return token


@pytest.fixture(scope="session")
def all_services(auth_service, course_service, pay_service):
    """聚合所有服务 URL。"""
    return {"auth": auth_service, "course": course_service, "pay": pay_service}
