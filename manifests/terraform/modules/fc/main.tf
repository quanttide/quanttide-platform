# =============================================================================
# fc — 后端服务（provider / API）部署到 Aliyun Function Compute 3.0
#
# 收敛自各仓库重复的 `fc.tf`（如 qtcloud-auth）。provider 为 Go HTTP 服务，
# 以 custom-container 容器镜像运行，VPC 内网访问 RDS。账号级 VPC / 安全组 /
# RDS 由 quanttide-platform 根 IaC 管理，本模块通过变量引用其输出。
# =============================================================================

# FC 默认角色：允许 FC 服务挂载弹性网卡访问 VPC（应用级）
resource "alicloud_ram_role" "fc" {
  role_name                   = "${var.name}-fc"
  assume_role_policy_document = <<EOF
{
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": ["fc.aliyuncs.com"]
      }
    }
  ],
  "Version": "1"
}
EOF
  description                 = "Function Compute 默认角色（${var.name}）"
}

resource "alicloud_ram_role_policy_attachment" "fc_vpc" {
  policy_name = "AliyunECSNetworkInterfaceManagementAccess"
  policy_type = "System"
  role_name   = alicloud_ram_role.fc.role_name
}

# 函数计算（FC 3.0）：custom-container 容器镜像，VPC 内网访问 RDS（应用级）
resource "alicloud_fcv3_function" "this" {
  function_name     = var.name
  description       = var.description
  runtime           = "custom-container"
  handler           = "index.handler" # custom-container 必填占位，实际由容器监听端口决定
  cpu               = var.cpu
  memory_size       = var.memory_size
  disk_size         = 512 # FC 3.0 必填（MB）
  timeout           = var.timeout
  internet_access   = true
  role              = alicloud_ram_role.fc.arn
  resource_group_id = var.resource_group_id

  dynamic "vpc_config" {
    for_each = length(var.vswitch_ids) > 0 ? [1] : []
    content {
      vpc_id            = var.vpc_id
      vswitch_ids       = var.vswitch_ids
      security_group_id = var.security_group_id
    }
  }

  custom_container_config {
    image = var.image
    port  = var.port
  }

  environment_variables = var.environment_variables

  tags = {
    project     = var.project
    environment = var.environment
  }
}

# HTTP 触发器：使服务可直接访问（后续由系统级 API 网关统一接入，保留为直连通道）
resource "alicloud_fcv3_trigger" "http" {
  function_name = alicloud_fcv3_function.this.function_name
  trigger_name  = "http"
  trigger_type  = "http"
  qualifier     = "LATEST"
  trigger_config = jsonencode({
    authType = "anonymous"
    methods  = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
  })
}
