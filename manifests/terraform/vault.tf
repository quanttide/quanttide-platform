terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.0"
    }
  }
}

provider "vault" {
  # 使用 VAULT_ADDR 和 VAULT_TOKEN 环境变量
}

locals {
  vault_basedir = var.home
  data_dir      = var.data_dir != null ? var.data_dir : "${local.vault_basedir}/.vault-data/data"
  logs_dir      = var.logs_dir != null ? var.logs_dir : "${local.vault_basedir}/.vault-data/logs"
  config_dir    = "${local.vault_basedir}/.vault-data/config"
}

resource "vault_mount" "kv_secret" {
  path        = var.stack_vault_mount != null ? var.stack_vault_mount : "secret"
  type        = "kv-v2"
  description = "KV v2 secrets engine managed by terraform"
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
