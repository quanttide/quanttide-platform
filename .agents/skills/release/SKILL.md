# 版本发布技能

## 用途
自动化发布流程：检查状态 → 更新 Changelog → 打标签 → 推送 → 创建 GitHub Release。

## 触发
用户说"发布"、"打版本"、"release"时自动激活。

## 发布前检查

1. 检查未发布内容:
   ```bash
   git log --oneline -n 10
   git status
   git diff HEAD
   ```

2. 确认发布就绪:
   - [ ] 所有测试通过
   - [ ] 文档已更新
   - [ ] 无未提交的变更
   - [ ] CHANGELOG已更新
   - [ ] 版本号符合语义化版本规范

## 确定版本号

根据 AGENTS.md 约定：
- **SemVer**: `v{major}.{minor}.{patch}`
- **阶段约定**:
  - Exploration（探索期）→ `0.0.x`
  - Validation（验证期）→ `0.x.y`
  - Release（正式版）→ `x.y.z`

如果用户未指定版本号，根据提交内容建议：
- 新增功能 → minor +1
- 仅修复 → patch +1
- 破坏性变更 → major +1

预发布版本格式：
- Alpha：`v0.0.1-alpha.1`
- Beta：`v0.0.1-beta.1`
- RC：`v0.0.1-rc.1`
- Release：`v0.0.1`

## 更新 CHANGELOG

1. 编辑 `CHANGELOG.md`:
   ```markdown
   ## [0.2.0] - YYYY-MM-DD

   ### Features
   - 新增 XXX

   ### Fixes
   - 修复 ZZZ
   ```

2. 内容要求:
   - 简洁明了，避免冗余描述
   - 使用动词开头：「新增」「修改」「修复」「移除」
   - 每条记录一行，不超过50字
   - 按重要性排序

3. 提交:
   ```bash
   git add CHANGELOG.md
   git commit -m "chore: release v{version}"
   ```

## 创建 Git 标签

```bash
git tag -a "v{version}" -m "Release v{version}"
git push origin main --tags
```

## 创建 GitHub Release

```bash
# 提取 CHANGELOG 中该版本的变更内容
CHANGELOG=$(sed -n "/## \[{version}\]/,/## \[/p" CHANGELOG.md | tail -n +2 | head -n -1)

gh release create "v{version}" \
  --title "Release v{version}" \
  --notes "$CHANGELOG" \
  --target main
```

## 子模块发布

子模块在自己的仓库独立发布，不需要在主仓库打版本。

```bash
# 在子模块中
cd apps/{module}
git status && git log -n 5 --oneline
git add .
git commit -m "chore: release v{version}"
git tag -a "v{version}" -m "Release v{version}"
git push origin main --tags

# 创建子模块 GitHub Release
CHANGELOG=$(cat CHANGELOG.md | sed -n "/## \[{version}\]/,/## \[/p" | tail -n +2 | head -n -1)
gh release create "v{version}" \
  --title "Release v{version}" \
  --notes "$CHANGELOG" \
  --target main
```

## 发布后确认

- [ ] Git标签已创建并推送
- [ ] GitHub Release已创建
- [ ] Release notes内容准确
- [ ] 版本号符合语义化版本规范

验收方式：
```bash
# 检查标签是否存在
git tag -l "v[0-9]*.[0-9]*.[0-9]*"

# 检查 CHANGELOG 对应版本是否存在
grep "## \[" CHANGELOG.md
```

## 注意事项
- 发布前确认测试通过、lint 无错误
- 标签推送到远程前需用户确认
- 如果发布失败：
  ```bash
  git tag -d "v{version}"
  git push --delete origin "v{version}"
  git revert HEAD
  ```

## 规范来源

遵循 [量潮科技版本发布标准](https://github.com/quanttide/quanttide-specification-of-business-entity/blob/v0.1.1/devops/release.md)
