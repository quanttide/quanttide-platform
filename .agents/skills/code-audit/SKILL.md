---
name: code-audit
description: 代码质量审计，使用 lizard/ruff 对 Python 项目进行复杂度分析、代码规范检查和重构建议。
---

# code-audit

> **⚠ 硬约束：先审计 → 再修复 → 最后提交**
> 加载此 Skill 后，必须按下方工作流从头到尾逐行执行命令。
> 标有"必须执行，不可跳过"的步骤是强制性的，AI 不得合并、跳过或提前执行后续步骤。

## CLI 工具

```bash
# 圈复杂度分析
lizard --languages python <source_dir>                            # 默认阈值：CCN > 15 警告
lizard --languages python --CCN 10 <source_dir>                   # 自定义阈值（严格模式）
lizard --languages python --l 100 <source_dir>                    # 同时检查函数长度超过 100 行
lizard --languages python --csv <source_dir>                      # CSV 格式输出（用于报告）

# 代码规范检查
ruff check <source_dir>                                           # 运行所有规则
ruff check --select ALL <source_dir>                              # 启用所有规则
ruff check --statistics <source_dir>                              # 按规则统计错误数
ruff check --fix <source_dir>                                     # 自动修复
ruff format --check <source_dir>                                  # 检查格式
ruff format <source_dir>                                          # 自动格式化

# 死代码检测
vulture <source_dir>                                              # 未使用的函数/变量/导入/类
vulture <source_dir> --min-confidence 100                          # 只报告确定无用的代码

# 依赖检测
deptry <source_dir>                                               # pyproject.toml 中未使用的依赖
```

## 规则

- **建议先 ruff 再 lizard**：ruff 能快速暴露语法错误和格式问题，避免在无效代码上做复杂度分析
- CCN > 15 的函数需要重构说明
- ruff 错误必须逐条审查，不能批量忽略
- 审计报告必须包含：CCN 分布、Top-N 高风险函数、ruff 错误分类统计
- 确认修复方案后再提交，禁止先提交再审计

## 审计指标

| 指标 | 健康区间 | 警告区间 | 危险区间 |
|------|----------|----------|----------|
| 平均 CCN | 1-5 | 6-10 | >10 |
| 单函数 CCN | 1-10 | 11-15 | >15 |
| 函数长度 | 1-30 行 | 31-60 行 | >60 行 |
| 参数数量 | 1-3 | 4-5 | >5 |
| ruff 错误数 | 0 | 1-10 | >10 |

**综合判定**：只要任一指标进入危险区间（如单函数 CCN > 15 或 ruff 错误 > 10），
总体评估即判为需改进。

## 工作流

### 0. 先决条件

确保工具可用：

```bash
which lizard && lizard --version
which ruff && ruff --version
which vulture && vulture --version
which deptry && deptry --version
```

### 1. 代码规范检查

**必须执行，不可跳过**

```bash
ruff check --statistics <source_dir>
ruff check <source_dir>
```

区分：
- **错误 (E/F)**：必须修复
- **警告 (W)**：建议修复
- **约定 (C)**：可选择修复

### 2. 圈复杂度分析

**必须执行，不可跳过**

```bash
lizard --languages python <source_dir>
```

记录输出中的：
- 总函数数、总 NLOC、平均 CCN
- 所有 CCN > 15 警告的函数及其位置
- 高 CCN 函数的文件名/行号/函数名

### 2.5 死代码检测

**必须执行，不可跳过**

```bash
vulture <source_dir>
```

记录所有未使用的函数、变量、导入和类，标注置信度。

### 2.6 依赖检测

**必须执行，不可跳过**

```bash
deptry <source_dir>
```

记录 `pyproject.toml` 中声明了但代码中没有使用的依赖。

### 3. 格式检查

```bash
ruff format --check <source_dir>
```

若有格式问题，记录差异点。

### 4. 问题分级与报告

按以下模板输出审计报告：

```
## 审计报告：<项目名>

### 1. 代码规范
- ruff 总错误数: N
- 错误分类: E/F/W/C 分布
- 关键问题: ...

### 2. 圈复杂度
- 总函数数: N
- 平均 CCN: X.X（健康/警告/危险）
- 最高 CCN 函数: <函数名> (CCN: X) @ <文件:行号>

### 3. 高风险函数

| 函数 | CCN | 行数 | 位置 | 建议 |
|------|-----|------|------|------|
| ... | ... | ... | ... | ... |

### 4. 总体评估
- 代码质量: 良好/一般/需改进
- 优先处理: <前 3 项建议>
```

### 5. 修复

> **在开始修复之前，先向用户展示第 4 步的审计报告，并逐项确认哪些问题需要修。** 有些高 CCN 函数可能是业务逻辑复杂但合理，不需要强制重构。用户确认后按优先级执行：

1. **CCN > 15** 的函数 —— 提取子函数、简化条件逻辑、引入守卫子句
2. **ruff 错误 (E/F)** —— 按 lint 提示修正
3. **ruff 警告 (W)** —— 逐条评估并修复
4. **格式问题** —— `ruff format <source_dir>` 自动修正

每修复一个函数后重新运行 `lizard` 确认 CCN 下降。**终止条件：全部函数的 CCN ≤ 15 即停止修复循环**，不需要强求降到健康区间。

### 6. 验证

修复完成后重新执行完整审计确认无退化：

```bash
lizard --languages python <source_dir>
ruff check <source_dir>
ruff format --check <source_dir>
vulture <source_dir>
deptry <source_dir>
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| CCN 偏高 | 函数内条件分支过多 | 提取子函数、用字典映射替代 if-else 链、策略模式 |
| 函数过长 | 单函数承担过多职责 | 按单一职责拆分为多个小函数 |
| 参数过多 | 函数依赖过多外部数据 | 封装为数据类或配置对象 |
| ruff E 类错误 | 语法或逻辑隐患 | 按 lint 提示逐条修复 |
| 代码重复 | 缺少抽象提取 | 提取公共函数或基类 |
