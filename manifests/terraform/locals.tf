locals {
  # 系统级共享资源命名：quanttide-<env>（与命名规则一致，见 docs/dev-guide/iac.md）
  name_prefix = "quanttide-${var.environment}"
}
