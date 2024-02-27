# STS

Jump to:
- [Regional AWS STS endpoints and global (legacy) AWS STS endpoint](#regional-aws-sts-endpoints-and-global-legacy-aws-sts-endpoint)
- [Decoding an encoded authorization failure message](#decoding-an-encoded-authorization-failure-message)

---
### Regional AWS STS endpoints and global (legacy) AWS STS endpoint

- [How to use Regional AWS STS endpoints](https://aws.amazon.com/blogs/security/how-to-use-regional-aws-sts-endpoints/), AWS,2024-02-26
- How to configure Regional AWS STS endpoints for your tools and SDKs
    - AWS CLI
        - By default, the AWS CLI version 2 sends AWS STS API requests to the Regional AWS STS endpoint
        - By default, the AWS CLI v1 sends AWS STS requests to the global (legacy) AWS STS endpoint.
        - Add `sts_regional_endpoints = regional  # or legacy` to ~/.aws/config


---
### Decoding an encoded authorization failure message

When you see an encoded authorization failure message like the one below:
[[Ref](https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html)]

```
A client error (UnauthorizedOperation) occurred when calling the RunInstances operation:
You are not authorized to perform this operation. Encoded authorization failure message:
FR4gBD7Ph0...
```

You can run the command below to decode the encoded authorization message.
You will need to have access to `sts:DecodeAuthorizationMessage`.

```
$ aws sts decode-authorization-message --encoded-message FR4gBD7Ph0...
```
