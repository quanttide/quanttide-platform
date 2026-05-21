---
name: devops-release
description: 发布 Git 仓库 Release。使用 qtcloud-devops CLI，必须先写 CHANGELOG 再发布，禁止跳步。支持子模块和主仓库两种流程。
---

# devops-release

> **⚠ 硬约束：不执行预检查 → 禁止发布**
> 加载此 Skill 后，必须按下方工作流从头到尾逐行执行命令。
> 标有"必须执行，不可跳过"的步骤是强制性的，AI 不得合并、跳过或提前执行后续步骤。

## CLI 使用

```bash
qtcloud-devops release --version v0.1.0                 # 标签 + GitHub Release（默认）
qtcloud-devops release --version v0.1.0 --tag-only       # 仅标签
qtcloud-devops release --version v0.1.0 --release-only   # 仅 GitHub Release（tag 须已存在）
qtcloud-devops release --version v0.1.0 --dry-run        # 仅检查
qtcloud-devops release --version v0.1.0 -y               # 跳过确认
```

- 仓库从 `git remote get-url origin` 自动检测，**不需要** `--repo` 参数
- Tag 已存在时默认模式跳过 tag 创建，继续发 release
- `--tag-only` 和 `--release-only` 互斥

## 规则

- 版本号遵循 semver（MAJOR.MINOR.PATCH）
- **必须先更新 CHANGELOG.md，提交推送，再执行发布**
- 发布前确认工作区干净
- Release notes 只包含对应版本内容
- 发布主仓库前确认所有子模块引用是最新的

## 工作流

### 0. 先决条件

确保 `qtcloud-devops` 命令可用：

```bash
which qtcloud-devops
```

如未安装：

```bash
pip install qtcloud-devops-cli
```

### 1. 预检查

**必须执行，不可跳过**

```bash
VERSION="v0.4.0"
qtcloud-devops release --version "$VERSION" --dry-run
```

若预检查失败，根据提示修复后重新执行。

### 2. 发布前确认

CLI 会在执行前展示发布摘要并等待 `y/N` 确认。使用 `-y` 跳过。

### 3. 子模块发布 Release

子模块使用 scoped tag（如 `cli/v0.1.0`、`python/v0.1.0`），在子模块目录内执行：

```bash
# 1. 进入子模块目录
cd <子模块路径>

# 2. 预检查
qtcloud-devops release --version "scope/vX.Y.Z" --dry-run

# 3. 发布（自动使用子模块的 remote）
VERSION="scope/vX.Y.Z"
qtcloud-devops release --version "$VERSION" -y

# 4. 返回主仓库，更新子模块引用
cd <主仓库根目录>
git add <子模块路径>
git commit -m "chore: update <子模块路径> submodule — $VERSION"
git push
```

### 4. 主仓库发布 Release

```bash
VERSION="vX.Y.Z"

# 1. 创建预发布版本（可选）
gh release create "${VERSION}-rc.1" --prerelease \
  --title "vX.Y.Z RC" \
  --notes "$(sed -n "/^## \[X.Y.Z\]/,/^## \[/p" CHANGELOG.md | sed '1d;$d')"

# 2. 确认所有子模块已更新
git submodule update --remote
git status

# 3. 更新 CHANGELOG.md

# 4. 提交 CHANGELOG.md
git add CHANGELOG.md && git commit -m "chore: prepare CHANGELOG for $VERSION"
git push

# 5. 预检查
qtcloud-devops release --version "$VERSION" --dry-run

# 6. 发布
qtcloud-devops release --version "$VERSION" -y
```

### 5. 错误处理和回滚

qtcloud-devops CLI 自动处理回滚（推送失败、Release 创建失败时）。手动回滚：

```bash
git tag -d vX.Y.Z
git push origin --delete vX.Y.Z 2>/dev/null || true
git reset --hard HEAD~1
gh release delete vX.Y.Z-rc.1 --repo $(gh repo view --json nameWithOwner -q .nameWithOwner) --yes
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| CHANGELOG 缺少版本 | 忘记更新 CHANGELOG.md | 添加版本记录后再发布 |
| 标签已存在（--release-only） | 标签不存在 | 先创建标签 |
| 工作区脏 | 有未提交变更 | 提交或暂存变更后再发布 |
| Release Notes 为空 | 版本格式不匹配 | 检查 CHANGELOG 版本标题格式 |
| 无法解析仓库 | git remote 不可用 | 检查是否在 git 仓库内 |

## 预发布检查清单

- [ ] 所有子模块版本已锁定
- [ ] 通过 CI 测试
- [ ] CHANGELOG.md 版本段已验证
- [ ] 版本号格式正确
- [ ] Release Notes 提取成功
- [ ] 工作区干净