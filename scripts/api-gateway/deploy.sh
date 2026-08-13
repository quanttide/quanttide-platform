#!/bin/bash
# 系统级 API 网关部署脚本（幂等）——传统版 Serverless，统一入口 api.quanttide.com
#
# 用法：ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET（或本地 aliyun 配置）
#   bash scripts/api-gateway/deploy.sh
#
# 职责：
#   1. 分组 qtcloud（已存在则跳过）
#   2. API 定义（按名称幂等创建 + 发布）：/qtcloud-auth/*、/qtcloud-pay/* 各端点（含 Authorization 头透传）
#   3. 域名绑定 api.quanttide.com（需 DNS CNAME 先生效）
#   4. DNS 记录 api.quanttide.com CNAME（幂等）
#
# 证书：*.quanttide.com 由 acme.sh 签发，CI ssl-cert.yml 负责绑定到网关（SetDomainCertificate）。
# 后续可迁移至 Terraform（manifests/terraform/api-gateway.tf 为迁移目标）。
set -euo pipefail

GROUP_NAME=qtcloud
DOMAIN=api.quanttide.com
REGION=cn-hangzhou

# 后端 FC 地址（公网 HTTP 触发器）
AUTH_FC="http://qtclouduth-prod-gnuguyxinh.cn-hangzhou.fcapp.run"
PAY_FC="http://qtcloudpay-prod-bgqlorwtph.cn-hangzhou.fcapp.run"
DELIB_FC="http://qtcloudlib-prod-eqppqgaboh.cn-hangzhou.fcapp.run"
COURSE_FC="http://qtcloudrse-prod-lsqdodhmqh.cn-hangzhou.fcapp.run"
FINANCE_FC="http://qtcloudnce-prod-bobbsmtsfr.cn-hangzhou.fcapp.run"
HUMAN_FC="http://qtcloudman-prod-eqpdghspoh.cn-hangzhou.fcapp.run"

# retry：aliyun CLI 偶发 DNS 超时（本地网络），重试 8 次
aliyun_retry() {
  local out
  for i in $(seq 1 8); do
    out=$("$@" 2>&1) && ! echo "$out" | grep -q "i/o timeout\|lookup" && { echo "$out"; return 0; }
    sleep 2
  done
  echo "FAILED: $*" >&2
  return 1
}

# ── 1. 分组 ──
GROUP_ID=$(aliyun_retry aliyun cloudapi DescribeApiGroups --PageNumber 1 --PageSize 100 |
  python3 -c "
import json,sys
d=json.load(sys.stdin)
for g in d.get('ApiGroupAttributes',{}).get('ApiGroupAttribute',[]):
    if g['GroupName']=='$GROUP_NAME': print(g['GroupId'])
" || true)
if [ -z "$GROUP_ID" ]; then
  GROUP_ID=$(aliyun_retry aliyun cloudapi CreateApiGroup --GroupName "$GROUP_NAME" --Description "qtcloud" |
    python3 -c "import json,sys; print(json.load(sys.stdin)['GroupId'])")
  echo "created group: $GROUP_ID"
else
  echo "group exists: $GROUP_ID"
fi
SUB_DOMAIN=$(aliyun_retry aliyun cloudapi DescribeApiGroup --GroupId "$GROUP_ID" |
  python3 -c "import json,sys; print(json.load(sys.stdin)['SubDomain'])" || echo "")

# ── 2. API 定义（名称幂等） ──
# 每行：ApiName|方法|请求路径|后端路径|FC 地址
APIS=(
  "qtcloud-auth-token|POST|/qtcloud-auth/oauth/token|/oauth/token|$AUTH_FC"
  "qtcloud-auth-sms|POST|/qtcloud-auth/oauth/sms/send|/oauth/sms/send|$AUTH_FC"
  "qtcloud-auth-register|POST|/qtcloud-auth/oauth/register|/oauth/register|$AUTH_FC"
  "qtcloud-auth-userinfo|GET|/qtcloud-auth/userinfo|/userinfo|$AUTH_FC"
  "qtcloud-pay-accounts|POST|/qtcloud-pay/accounts|/accounts|$PAY_FC"
  "qtcloud-pay-recharges|POST|/qtcloud-pay/accounts/{account_id}/recharges|/accounts/{account_id}/recharges|$PAY_FC"
  "qtcloud-pay-orders|POST|/qtcloud-pay/orders|/orders|$PAY_FC"
  "qtcloud-pay-health|GET|/qtcloud-pay/reconcile/consistency|/reconcile/consistency|$PAY_FC"
  "qtcloud-delib-resolutions|GET|/qtcloud-delib/resolutions|/resolutions|$DELIB_FC"
  "qtcloud-delib-resolutions-post|POST|/qtcloud-delib/resolutions|/resolutions|$DELIB_FC"
  "qtcloud-delib-resolution-delete|DELETE|/qtcloud-delib/resolutions/{name}|/resolutions/{name}|$DELIB_FC"
  "qtcloud-course-player-data|GET|/qtcloud-course/player-data|/player-data|$COURSE_FC"
  "qtcloud-course-programs|GET|/qtcloud-course/programs|/programs|$COURSE_FC"
  "qtcloud-course-courses|GET|/qtcloud-course/courses|/courses|$COURSE_FC"
  "qtcloud-finance-budgets|GET|/qtcloud-finance/budgets|/budgets|$FINANCE_FC"
  "qtcloud-finance-budgets-post|POST|/qtcloud-finance/budgets|/budgets|$FINANCE_FC"
  "qtcloud-finance-budget|GET|/qtcloud-finance/budgets/{id}|/budgets/{id}|$FINANCE_FC"
  "qtcloud-delib-topics|GET|/qtcloud-delib/topics|/topics|$DELIB_FC"
  "qtcloud-delib-topics-post|POST|/qtcloud-delib/topics|/topics|$DELIB_FC"
  "qtcloud-delib-topic|GET|/qtcloud-delib/topics/{id}|/topics/{id}|$DELIB_FC"
  "qtcloud-delib-topic-second|POST|/qtcloud-delib/topics/{id}/second|/topics/{id}/second|$DELIB_FC"
  "qtcloud-delib-topic-debate|POST|/qtcloud-delib/topics/{id}/debate|/topics/{id}/debate|$DELIB_FC"
  "qtcloud-delib-topic-vote|POST|/qtcloud-delib/topics/{id}/vote|/topics/{id}/vote|$DELIB_FC"
  "qtcloud-delib-topic-close|POST|/qtcloud-delib/topics/{id}/close|/topics/{id}/close|$DELIB_FC"
  "qtcloud-human-healthz|GET|/qtcloud-human/healthz|/healthz|$HUMAN_FC"
  "qtcloud-human-timesheets|GET|/qtcloud-human/timesheets|/timesheets|$HUMAN_FC"
  "qtcloud-human-timesheets-post|POST|/qtcloud-human/timesheets|/timesheets|$HUMAN_FC"
)

for entry in "${APIS[@]}"; do
  IFS='|' read -r name method reqpath svcpath fc <<< "$entry"
  API_ID=$(aliyun_retry aliyun cloudapi DescribeApis --GroupId "$GROUP_ID" --ApiName "$name" --PageNumber 1 --PageSize 100 |
    python3 -c "
import json,sys
d=json.load(sys.stdin)
for a in d.get('ApiSummarys',{}).get('ApiSummary',[]):
    if a['ApiName']=='$name': print(a['ApiId'])
" || true)
  if [ -n "$API_ID" ]; then
    echo "api exists: $name ($API_ID)"
  else
    REQ="{\"RequestProtocol\":\"HTTPS\",\"RequestHttpMethod\":\"$method\",\"RequestPath\":\"$reqpath\",\"BodyFormat\":\"STREAM\"}"
    SVC="{\"ServiceProtocol\":\"HTTP\",\"ServiceAddress\":\"$fc\",\"ServicePath\":\"$svcpath\",\"ServiceHttpMethod\":\"$method\",\"Mock\":\"FALSE\",\"ContentTypeCatagory\":\"CLIENT\"}"
    # Authorization 头透传（JWT 鉴权；传统网关默认丢弃未定义 Header）
    P_REQ='[{"ApiParameterName":"Authorization","Location":"HEAD","ParameterType":"String","Required":"OPTIONAL","DefaultValue":"","ApiParameterDesc":"JWT Bearer"}]'
    P_SVC='[{"ServiceParameterName":"Authorization","Location":"HEAD","Type":"String","ParameterCatalog":"REQUEST","ServiceParameterApiName":"Authorization"}]'
    P_MAP='[{"ServiceParameterName":"Authorization","RequestParameterName":"Authorization"}]'
    API_ID=$(aliyun_retry aliyun cloudapi CreateApi \
      --GroupId "$GROUP_ID" --ApiName "$name" --Description "$name" \
      --RequestConfig "$REQ" --ServiceConfig "$SVC" \
      --RequestParameters "$P_REQ" --ServiceParameters "$P_SVC" --ServiceParametersMap "$P_MAP" \
      --Visibility PUBLIC --AuthType ANONYMOUS --ResultType JSON --ResultSample '{}' |
      python3 -c "import json,sys; print(json.load(sys.stdin)['ApiId'])")
    echo "created api: $name ($API_ID)"
  fi
  aliyun_retry aliyun cloudapi DeployApi --GroupId "$GROUP_ID" --ApiId "$API_ID" --StageName RELEASE --Description "deploy.sh" > /dev/null 2>&1 || true
done

# ── 3. DNS 记录（幂等） ──
EXISTING_DNS=$(aliyun_retry aliyun cloudapi DescribeApiGroup --GroupId "$GROUP_ID" >/dev/null 2>&1; echo "")
# DNS 用 alidns SDK 处理（aliyun CLI 无 dns 产品），见 dns.py
${PYTHON:-python3} "$(dirname "$0")/dns.py" --rr api --type CNAME --value "${SUB_DOMAIN}."

# ── 4. 域名绑定（需 DNS 生效；幂等：已绑定则跳过） ──
DOMAIN_STATE=$(aliyun_retry aliyun cloudapi DescribeDomain --GroupId "$GROUP_ID" --DomainName "$DOMAIN" 2>&1 || true)
if echo "$DOMAIN_STATE" | grep -q "DomainName"; then
  echo "domain bound: $DOMAIN"
else
  aliyun_retry aliyun cloudapi SetDomain --GroupId "$GROUP_ID" --DomainName "$DOMAIN" --IsHttpRedirectToHttps true > /dev/null
  echo "domain bound: $DOMAIN（等待证书绑定，见 ssl-cert.yml）"
fi

echo "DONE"
