# ================================================================
# 系统级共享 RDS PostgreSQL Serverless（quanttide 体系统一管理）
# 实例为共享：各应用在实例上创建自己的数据库/账号（应用侧 IaC 负责）
# ================================================================

# 服务关联角色（账号级一次性前置，已创建；新账号需先执行）：
#   aliyun rds CreateServiceLinkedRole --RegionId cn-hangzhou --ServiceLinkedRole AliyunServiceRoleForRdsPgsqlOnEcs
#   aliyun rds CreateServiceLinkedRole --RegionId cn-hangzhou --ServiceLinkedRole AliyunServiceRoleForRDSProxyOnEcs
# 踩坑：CreateDBInstance 报 ServiceLinkedRole.NotExist 时两个角色都需存在（错误信息未指向第二个）

resource "alicloud_db_instance" "this" {
  engine         = "PostgreSQL"
  engine_version = var.db_engine_version
  category       = var.db_category
  # Serverless 实例计费方式必须为 Serverless（Postpaid 报 InvalidSaleComponentFault）
  instance_charge_type     = "Serverless"
  instance_type            = "pg.n2.serverless.1c"
  instance_storage         = 20
  db_instance_storage_type = "cloud_essd"
  vswitch_id               = alicloud_vswitch.this.id
  port                     = "5432"
  # 白名单：仅允许 VPC 交换机网段内网访问
  security_ips = [var.vswitch_cidr]
  serverless_config {
    min_capacity = var.db_min_capacity
    max_capacity = var.db_max_capacity
    auto_pause   = true
    switch_force = false
  }
  instance_name     = local.name_prefix
  resource_group_id = local.resource_group_id
  # 生产保护：删除保护 + prevent_destroy
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
  tags = {
    project     = "quanttide"
    environment = var.environment
  }
}
