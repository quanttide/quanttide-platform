# qtclass 端到端系统测试

验证 qtcloud-auth → qtcloud-course → qtcloud-pay 跨服务链路，模拟 qtclass 学员报名、
课程创建、支付完整流程。

## 前置条件

- Go 1.22+
- Python 3.12+ (pytest)

## 运行

```bash
# 从仓库根目录执行
uv run pytest tests/qtclass/ -v

# 显示详细日志
uv run pytest tests/qtclass/ -v --log-cli-level=INFO
```

## 测试场景

| 测试类 | 覆盖服务 | 描述 |
|--------|---------|------|
| `test_admin.py` | **后台管理** | |
| `TestAdminAuth` | qtcloud-auth | 管理员登录、身份校验、用户信息 |
| `TestAdminCourseContent` | qtcloud-course | Program/Course/Lesson/Scene CRUD 与关联 |
| `TestAdminClassManagement` | qtcloud-course | 班级创建、状态流转、删除 |
| `TestAdminPayManagement` | qtcloud-pay | 支付发起、订单查询、退款 |
| `test_qtclass.py` | **前台课堂** | |
| `TestStudentEnrollsAndAttends` | qtcloud-course + qtcloud-pay | 学员报名支付 → 开课 → 上课 → 结课 |
| `TestSceneTeaching` | qtcloud-course | 互动课时（视频片段 + 分支选项） |
