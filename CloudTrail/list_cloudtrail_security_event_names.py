COMMON_SECURITY_EVENTS = [
    "AuthorizeSecurityGroupEgress",
    "AuthorizeSecurityGroupIngress",
    "RevokeSecurityGroupEgress",
    "RevokeSecurityGroupIngress",
    "CreateSecurityGroup",
    "DeleteSecurityGroup",
    "AuthorizeDBSecurityGroupIngress",
    "RevokeDBSecurityGroupIngress",
    "CreateDBSecurityGroup",
    "DeleteDBSecurityGroup",
    "ConsoleLogin",
    "StopLogging",
    "CreateNetworkAclEntry",
    "CreateRoute",
]

for e in COMMON_SECURITY_EVENTS:
    print(e)
