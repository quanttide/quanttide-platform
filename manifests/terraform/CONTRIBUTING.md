# CONTRIBUTING

## 文件组织

按资源域组织 `.tf` 文件：

| 文件 | 内容 |
|------|------|
| `providers.tf` / `versions.tf` | provider 与远程状态 |
| `network.tf` | VPC / 交换机 / 安全组 |
| `rds.tf` | 共享 RDS 实例 |
| `resource-group.tf` | quanttide 资源组 |
| `outputs.tf` | 供应用仓库引用的输出 |

## 规则

- 命名遵循 quanttide 命名规则：系统级 `quanttide-<env>` 前缀
- 本仓库只管理系统级共享资源；应用级资源交给应用仓库
- 关键资源（VPC/RDS）保持 `prevent_destroy` + 删除保护
- 新增踩坑记录写入 README「踩坑记录」
