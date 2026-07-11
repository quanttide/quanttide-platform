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
| `TestAuthFlow` | qtcloud-auth | 管理员密码登录、获取 JWT、查询用户信息 |
| `TestProgramCurd` | qtcloud-course | Program/Course/Lesson 扁平 CRUD 与关联 |
| `TestClassLifecycle` | qtcloud-course | 班级创建、状态流转 (preparing→active→ended) |
| `TestPayFlow` | qtcloud-pay | 支付发起、订单查询、退款 |
| `TestTeacherPreparesClass` | qtcloud-course | 教师开课备课：课程体系 + 班级创建 |
| `TestStudentEnrollsAndAttends` | qtcloud-course + qtcloud-pay | 学员报名支付 + 上课结课 |
| `TestAuthGate` | qtcloud-auth | 身份校验、未授权拦截 |
| `TestSceneTeaching` | qtcloud-course | 互动课时创建（视频片段 + 分支选项） |
