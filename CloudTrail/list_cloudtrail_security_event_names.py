COMMON_SECURITY_EVENTS = [
    "AuthorizeSecurityGroupEgress",
    "AuthorizeSecurityGroupIngress",
    "RevokeSecurityGroupEgress",
    "RevokeSecurityGroupIngress",
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
