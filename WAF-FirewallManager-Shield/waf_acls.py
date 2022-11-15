import json

import boto3


def get_web_acls(client, scope="REGIONAL"):  # Scope='CLOUDFRONT'|'REGIONAL',
    web_acls = []
    kwargs = {"Scope": scope}
    while True:
        resp = client.list_web_acls(**kwargs)
        web_acls.extend(resp["WebACLs"])

        next_marker = resp.get("NextMarker")
        if not next_marker:
            break
        kwargs["NextMarker"] = next_marker
    return web_acls


def main():
    client = boto3.client("wafv2")
    web_acls = get_web_acls(client, "REGIONAL")

    for web_acl in web_acls:
        print(json.dumps(web_acl, indent=2, default=str))


if __name__ == "__main__":
     main()
