# ROADMAP

## 基础设施方向 — 计算以 FaaS 为主

计算原则从 k8s 为主调整为 FaaS（函数计算）为主：大型系统以 FaaS 为主，k8s 与服务器为辅，服务器仅承载 FaaS 无法承载的有状态/常驻组件（如 Vault 密钥服务）。

## qtcloud-knowl-cli v0.2 — 重新设计 domain

当前 extract 按文件生成 domain，但知识库应按故事/作品系列组织。
v0.2 解决 domain 合并与 world 分类问题。

详情见 `apps/qtcloud-knowl/src/cli/ROADMAP.md`。

## qtcloud-devops-cli v0.2 — 增加 audit

当前 `qtcloud-devops release` 只负责发布流程。v0.2 增加审计能力。

盲区见 `apps/qtcloud-devops/src/cli/STATUS.md`。
