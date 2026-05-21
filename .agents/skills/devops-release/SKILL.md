---
name: devops-release
description: 发布 Git 仓库 Release。必须先写 CHANGELOG 再打 tag，禁止跳步。支持子模块和主仓库两种流程。
---

# devops-release

> **⚠ 硬约束：不执行预检查 → 禁止发布**
> 加载此 Skill 后，必须按下方工作流从头到尾逐行执行命令。
> 标有"必须执行，不可跳过"的步骤是强制性的，AI 不得合并、跳过或提前执行后续步骤。

发布 Git 仓库 Release。

## 规则

- 版本号遵循 semver（MAJOR.MINOR.PATCH）
- **必须先更新 CHANGELOG.md，提交推送，再执行发布**
- 发布前确认工作区干净
- Release notes 只包含对应版本内容
- 发布主仓库前确认所有子模块引用是最新的

## 依赖

- devops-commit: 检查工作区状态
- devops-submodule: 检查子模块状态

## 工作流

### 0. 先决条件

确保 `qtcloud-devops` 命令可用：

```bash
which qtcloud-devops
```

如未安装，在 `apps/qtcloud-devops` 目录下执行：

```bash
cd apps/qtcloud-devops && pip install -e src/cli
```

### 1. 预检查

**必须执行，不可跳过**

```bash
# 设置版本号（替换为实际值）
VERSION="v0.4.0"

# 执行预检查（dry-run 模式）
qtcloud-devops release --version "$VERSION" --dry-run
```

若预检查失败，根据提示修复后重新执行。

### 2. 发布前确认

**向用户展示以下信息并请求确认**

```
发布版本: vX.Y.Z

检查结果:
✓ 版本号格式正确
✓ CHANGELOG.md 包含目标版本
✓ Release Notes 提取成功
✓ 标签不存在
✓ 工作区干净

确认发布? (y/n)
```

使用 `-y` 跳过确认直接发布，或不加 `-y` 让 CLI 交互式确认。

### 3. 子模块发布 Release

子模块使用 scoped tag（如 `cli/v0.1.0`、`python/v0.1.0`），需在子模块目录内执行：

```bash
# 1. 进入子模块目录
cd <子模块路径>

# 2. 执行预检查（使用 scoped 版本号）
qtcloud-devops release --version "scope/vX.Y.Z" --dry-run

# 3. 发布
VERSION="scope/vX.Y.Z"
REPO="quanttide/<仓库名>"

# 创建并推送标签 + GitHub Release
qtcloud-devops release --version "$VERSION" --repo "$REPO" -y

# 4. 返回主仓库，更新子模块引用
cd <主仓库根目录>
git add <子模块路径>
git commit -m "chore: update <子模块路径> submodule — $VERSION"
git push
```

### 4. 主仓库发布 Release

```bash
VERSION="vX.Y.Z"
REPO="quanttide/quanttide-platform"

# 1. 创建预发布版本（可选）
gh release create "${VERSION}-rc.1" \
  --prerelease \
  --title "vX.Y.Z RC" \
  --notes "$(sed -n "/^## \[X.Y.Z\]/,/^## \[/p" CHANGELOG.md | sed '1d;$d')"

# 2. 确认所有子模块已更新
git submodule update --remote
git status

# 3. 更新 CHANGELOG.md

# 4. 提交 CHANGELOG.md
git add CHANGELOG.md && git commit -m "chore: prepare CHANGELOG for $VERSION"
git push

# 5. 预检查 + 发布前确认
qtcloud-devops release --version "$VERSION" --dry-run

# 6. 发布（创建标签 + 推送 + GitHub Release）
qtcloud-devops release --version "$VERSION" --repo "$REPO" -y
```

### 5. 错误处理和回滚

```bash
# 标签已创建但 GitHub Release 失败（qtcloud-devops 自动回滚标签）
# 手动回滚：

# 删除本地标签
git tag -d vX.Y.Z

# 删除远程标签
git push origin --delete vX.Y.Z 2>/dev/null || true

# 恢复到发布前状态（如果有提交）
git reset --hard HEAD~1

# 清理预发布版本
gh release delete vX.Y.Z-rc.1 --repo quanttide/quanttide-platform --yes
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| CHANGELOG 缺少版本 | 忘记更新 CHANGELOG.md | 添加版本记录后再发布 |
| 标签已存在 | 重复发布 | 删除旧标签或使用新版本号 |
| 工作区脏 | 有未提交变更 | 提交或暂存变更后再发布 |
| Release Notes 为空 | 版本格式不匹配 | 检查 CHANGELOG 版本标题格式 |
| 子模块未更新 | 子模块有新提交 | 执行 `git submodule update --remote` |

## 预发布检查清单

- [ ] 所有子模块版本已锁定
- [ ] 通过 CI 测试
- [ ] CHANGELOG.md 版本段已验证
- [ ] 执行过 `npm run build` (如适用)
- [ ] 版本号格式正确
- [ ] Release Notes 提取成功
- [ ] 工作区干净

## 输出

### 成功时返回

```
✓ Release vX.Y.Z 创建成功
  标签: vX.Y.Z
  URL: https://github.com/quanttide/quanttide-founder/releases/tag/vX.Y.Z
  提交: <SHA>
```

### 失败时返回

```
✗ Release vX.Y.Z 创建失败
  错误码: <ERROR_CODE>
  原因: <错误描述>
  建议: <解决方案>
```