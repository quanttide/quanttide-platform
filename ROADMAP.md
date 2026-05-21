# ROADMAP

## qtcloud-knowl-cli v0.2 — 重新设计 domain

当前 extract 按文件生成 domain，但知识库应按故事/作品系列组织。
v0.2 解决 domain 合并问题，让多文件能够合并到同一个 domain 下。

**层级扩展**：domain 上级增加 world（世界观），用于区分现实与虚构世界：

方向见 `apps/qtcloud-knowl/src/cli/ROADMAP.md`。

## qtcloud-devops v0.2 — 增加 audit

当前 `qtcloud-devops release` 只负责发布流程。v0.2 增加审计能力，
让工具能检测发布过程中的常见问题（如 CHANGELOG 未写、版本未升等）。

盲区见 `apps/qtcloud-devops/src/cli/STATUS.md`。
