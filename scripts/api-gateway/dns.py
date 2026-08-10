#!/usr/bin/env python3
"""DNS 记录幂等管理（aliyun CLI 无 dns 产品，用 alidns SDK）。

用法：dns.py --rr api --type CNAME --value xxx.alicloudapi.com.
凭据：环境变量 ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET，或 ~/.aliyun/config.json default profile。
"""

import argparse
import json
import os
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest


def load_credentials():
    ak = os.environ.get("ALIYUN_ACCESS_KEY_ID")
    sk = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
    if ak and sk:
        return ak, sk
    # 本地 aliyun CLI 配置兜底
    cfg_path = os.path.expanduser("~/.aliyun/config.json")
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path))
        for p in cfg.get("profiles", []):
            if p.get("name") == cfg.get("current", "default"):
                return p["access_key_id"], p["access_key_secret"]
    raise SystemExit("缺少阿里云凭证（ALIYUN_ACCESS_KEY_ID / SECRET 或 ~/.aliyun/config.json）")


def find_record(client, domain, rr, rtype):
    req = DescribeDomainRecordsRequest()
    req.set_DomainName(domain)
    req.set_RRKeyWord(rr)
    req.set_TypeKeyWord(rtype)
    resp = json.loads(client.do_action_with_exception(req))
    for r in resp.get("DomainRecords", {}).get("Record", []):
        if r["RR"] == rr and r["Type"] == rtype:
            return r
    return None


def add_record(client, domain, rr, rtype, value):
    req = AddDomainRecordRequest()
    req.set_DomainName(domain)
    req.set_RR(rr)
    req.set_Type(rtype)
    req.set_Value(value)
    resp = json.loads(client.do_action_with_exception(req))
    return resp.get("RecordId")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="quanttide.com")
    ap.add_argument("--rr", required=True)
    ap.add_argument("--type", required=True)
    ap.add_argument("--value", required=True)
    args = ap.parse_args()

    ak, sk = load_credentials()
    client = AcsClient(ak, sk, "cn-hangzhou")

    existing = find_record(client, args.domain, args.rr, args.type)
    if existing:
        print(f"dns record exists: {args.rr} {args.type} -> {existing['Value']}")
        return
    rid = add_record(client, args.domain, args.rr, args.type, args.value)
    print(f"dns record added: {args.rr} {args.type} -> {args.value} ({rid})")


if __name__ == "__main__":
    main()
