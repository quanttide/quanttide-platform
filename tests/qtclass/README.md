# qtclass 端到端系统测试

验证 qtcloud-auth → qtcloud-course → qtcloud-pay 跨服务链路，模拟 qtclass 学员报名、
课程创建、支付完整流程。

## 前置条件

- Go 1.22+
- Python 3.12+ (pytest)

## 运行

```bash
# 从仓库根目录执行
pytest tests/qtclass/ -v

# 只运行快速测试（不启动服务，仅契约验证）
pytest tests/qtclass/ -v -m "not service"

# 显示详细日志
pytest tests/qtclass/ -v --log-cli-level=INFO
```

## 测试场景

| 测试 | 覆盖服务 | 描述 |
|------|---------|------|
| `test_auth_flow` | qtcloud-auth | 管理员密码登录、获取 JWT、查询用户信息 |
| `test_course_crud` | qtcloud-course | Program → Course → Lesson 三级 CRUD |
| `test_class_lifecycle` | qtcloud-course | 班级创建、状态流转 |
| `test_pay_flow` | qtcloud-pay | 支付发起、订单查询、退款 |
| `test_enrollment_e2e` | 全链路 | 学员认证 → 选课 → 支付 → 班级加入完整流程 |
