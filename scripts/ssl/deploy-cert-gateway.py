#!/usr/bin/env python3
"""将 acme.sh 签发的泛域名证书绑定到系统级 API 网关（api.quanttide.com）。

用法:
    python3 deploy-cert-gateway.py --cert-dir <acme_cert_dir> --group-id <group_id> --domain api.quanttide.com

凭证:
    环境变量 ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET（CI 注入）
"""

import argparse
import json
import os

from aliyunsdkcore.client import AcsClient
from aliyunsdkcloudapi.request.v20160714.SetDomainCertificateRequest import (
    SetDomainCertificateRequest,
)


def read_cert(cert_dir: str):
    cert_path = os.path.join(cert_dir, "fullchain.cer")
    key_path = os.path.join(cert_dir, "quanttide.com.key")
    with open(cert_path, "r") as f:
        cert = f.read()
    with open(key_path, "r") as f:
        key = f.read()
    return cert, key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cert-dir", required=True)
    ap.add_argument("--group-id", required=True, help="API 网关分组 ID（qtcloud）")
    ap.add_argument("--domain", default="api.quanttide.com")
    ap.add_argument("--cert-name", default="quanttide-wildcard")
    args = ap.parse_args()

    ak = os.environ["ALIYUN_ACCESS_KEY_ID"]
    sk = os.environ["ALIYUN_ACCESS_KEY_SECRET"]
    client = AcsClient(ak, sk, "cn-hangzhou")

    cert, key = read_cert(args.cert_dir)

    req = SetDomainCertificateRequest()
    req.set_GroupId(args.group_id)
    req.set_DomainName(args.domain)
    req.set_CertificateName(args.cert_name)
    req.set_CertificateBody(cert)
    req.set_CertificatePrivateKey(key)
    client.do_action_with_exception(req)
    print(f"cert bound to gateway: {args.domain} ({args.cert_name})")


if __name__ == "__main__":
    main()
