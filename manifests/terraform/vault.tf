# ================================================================
# 管理层（环境无关）
# 声明 Vault 运行时的 secrets engine、policies 等。
# 本地和云共用，无需修改。
# ================================================================

resource "vault_mount" "kv_secret" {
  path        = var.stack_vault_mount != null ? var.stack_vault_mount : "secret"
  type        = "kv-v2"
  description = "KV v2 secrets engine managed by terraform"
}

# ================================================================
# 部署层（本地环境）
# 生成 Vault 配置文件、seal key 及备份。上云时整块替换。
# ================================================================

locals {
  vault_basedir = var.home
  data_dir      = var.data_dir != null ? var.data_dir : "${local.vault_basedir}/.vault-data/data"
  logs_dir      = var.logs_dir != null ? var.logs_dir : "${local.vault_basedir}/.vault-data/logs"
  config_dir    = "${local.vault_basedir}/.vault-data/config"
}

resource "local_file" "vault_config" {
  filename = "${local.config_dir}/vault.hcl"
  content = templatefile("${path.module}/templates/vault.hcl.tftpl", {
    bind_ip     = var.bind_ip
    bind_port   = var.container_port
    data_dir    = local.data_dir
    logs_dir    = local.logs_dir
    tls_disable = var.tls_disable
  })
}
