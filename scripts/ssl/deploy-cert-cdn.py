#!/usr/bin/env python3
"""将 acme.sh 签发的证书批量绑定到 CDN 域名。

用法:
    python3 deploy-cert-cdn.py --cert-dir <acme_cert_dir> [--domains d1,d2,...]

凭证:
    环境变量 ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET（CI 注入）
"""

import argparse
import json
import os
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510.SetCdnDomainSSLCertificateRequest import (
    SetCdnDomainSSLCertificateRequest,
)

CDN_DOMAINS = [
    "quanttide.com",
    "founder.quanttide.com",
    "data.quanttide.com",
    "data.cloud.quanttide.com",
    "studio.execute.cloud.quanttide.com",
]


def read_cert(cert_dir: str):
    cert_path = os.path.join(cert_dir, "fullchain.cer")
    key_path = os.path.join(cert_dir, "quanttide.com.key")
    with open(cert_path, "r") as f:
        cert = f.read()
    with open(key_path, "r") as f:
        key = f.read()
    return cert, key


def bind_cert(client, domain: str, cert: str, key: str):
    req = SetCdnDomainSSLCertificateRequest()
    req.set_DomainName(domain)
    req.set_SSLPub(cert)
    req.set_SSLPri(key)
    req.set_SSLProtocol("on")
    req.set_CertType("upload")
    client.do_action_with_exception(req)
    print(f"[OK] bound cert to {domain}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cert-dir", required=True, help="acme.sh cert dir")
    parser.add_argument("--domains", default=",".join(CDN_DOMAINS), help="CDN domains")
    args = parser.parse_args()

    ak = os.environ.get("ALIYUN_ACCESS_KEY_ID")
    sk = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
    if not ak or not sk:
        print("ERROR: ALIYUN_ACCESS_KEY_ID/SECRET not set", file=sys.stderr)
        sys.exit(1)

    cert, key = read_cert(args.cert_dir)
    client = AcsClient(ak, sk, "cn-hangzhou")

    domains = [d for d in args.domains.split(",") if d]
    for domain in domains:
        bind_cert(client, domain, cert, key)


if __name__ == "__main__":
    main()