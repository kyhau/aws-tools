# API Gateway

Jump to
- [Examples for demo](#examples-for-demo)
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Authentication and Authorisation](#authentication-and-authorisation)
- [Protect API Gateway with CloudFront / How to limit the access to your REST Regional API Gateway endpoint exclusively to CloudFront](#protect-apigw-with-cloudfront--how-to-limit-the-access-to-your-rest-regional-apigw-endpoint-exclusively-to-cloudfront)
- [Public API Gateway and VPC Private DNS setting](#public-api-gateway-and-vpc-private-dns-setting)
- [Private API Gateways](#private-api-gateways)
- [AWS API Gateway vs. Application Load Balancer (ALB)](#aws-api-gateway-vs-application-load-balancer-alb)
- [From API Gateway to private ALB](#from-api-gateway-to-private-alb)
- [mTLS](#mtls)
- [Managing multi-tenant APIs using Amazon API Gateway](https://aws.amazon.com/blogs/compute/managing-multi-tenant-apis-using-amazon-api-gateway/), AWS, 2022-06-22
- [Architecting multiple microservices behind a single domain with API Gateway](https://aws.amazon.com/blogs/compute/architecting-multiple-microservices-behind-a-single-domain-with-amazon-api-gateway/), AWS, 2020-09-18
- [API Gateway for multi account architecture](https://www.levvel.io/resource-library/aws-api-gateway-for-multi-account-architecture), levvel.io, 2019-10-02
- [Previous Security Issues or Breaking Changes](#previous-security-issues-or-breaking-changes)


---
## Examples for demo
- [access-private-apigw-in-another-account](https://github.com/kyhau/access-private-apigw-in-another-account) - This repo provides a working example for calling a private API Gateway REST API from another AWS account, including CloudFormation templates, API test code and GitHub Actions workflows.


---
## Useful Libs and Tools

- [amazon-api-gateway-cors-configurator](https://github.com/aws-samples/amazon-api-gateway-cors-configurator) - Amazon API Gateway CORS Configurator
- [aws-api-gateway-developer-portal](https://github.com/awslabs/aws-api-gateway-developer-portal) - Amazon API Gateway Serverless Developer Portal, see also [Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-developer-portal.html)


---
## Authentication and Authorisation

- [API Gateway customers can easily secure APIs using Amazon Verified Permissions](https://aws.amazon.com/about-aws/whats-new/2024/06/amazon-api-gateway-apis-amazon-verified-permissions/), AWS, 2024-06
- [Reduce risk by implementing HttpOnly cookie authentication in Amazon API Gateway](https://aws.amazon.com/blogs/security/reduce-risk-by-implementing-httponly-cookie-authentication-in-amazon-api-gateway/), AWS, 2023-01-30
    - store access tokens and authenticate with HttpOnly cookies in your own workloads when using APIGW as the client-facing endpoint.
    - store OAuth2 access tokens in the browser cookie store, and verify user authentication through APIGW
    - use Cognito to issue OAuth2 access tokens (not limited to OAuth2). (can use other kinds of tokens or session IDs)


---
## Protect APIGW with CloudFront / How to limit the access to your REST Regional APIGW endpoint exclusively to CloudFront

See also
- [Securing Amazon API Gateway with secure ciphers using Amazon CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/securing-amazon-api-gateway-with-secure-ciphers-using-amazon-cloudfront/), AWS, 2023-08-14
- [Protect APIs with Amazon API Gateway and perimeter protection services](https://aws.amazon.com/blogs/security/protect-apis-with-amazon-api-gateway-and-perimeter-protection-services/), AWS, 2023-07-19


To take advantage of the perimeter protection layer built with CloudFront, AWS WAF, and Shield, and to help avoid exposing API Gateway endpoints directly, you can use the following approaches to restrict API access through CloudFront only.

1. CloudFront can insert the X-API-Key header before it forwards the request to API Gateway, and API Gateway validates the API key when receiving the requests. For more information, see [Protecting your API using Amazon API Gateway and AWS WAF — Part 2](https://aws.amazon.com/blogs/compute/protecting-your-api-using-amazon-api-gateway-and-aws-waf-part-2/).
    - Support REST API endpoints only
2. CloudFront can insert a custom header (not X-API-Key) with a known secret that is shared with API Gateway. An AWS Lambda custom request authorizer that is configured in API Gateway validates the secret. For more information, see [Restricting access on HTTP API Gateway Endpoint with Lambda Authorizer](https://aws.amazon.com/blogs/networking-and-content-delivery/restricting-access-http-api-gateway-lambda-authorizer/).
    - has an additional cost due to the use of the Lambda authorizer.
3. CloudFront can sign the request with AWS Signature Version 4 by using Lambda@Edge before it sends the request to API Gateway. Configured AWS Identity and Access Management (IAM) authorization in API Gateway validates the signature and verifies the identity of the requester.
    - an additional Lambda@Edge cost in this approach
    - support all REST, HTTP, and WebSocket endpoints


---
## From API Gateway to private ALB

- Connecting API Gateway and private ALB ([stackoverflow](https://stackoverflow.com/questions/50782573/connecting-aws-api-gateway-and-private-alb))
    1. For a REST API, you can create a VPC link to an NLB. The NLB and API must be owned by the same AWS account ([Ref](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-with-private-integration.html)).
        - You can create a VPC link to an NLB, but not an ALB (that's the invalid endpoint address issue you've been seeing)
    1. For a HTTP API, you can create a VPC link to an ALB, NLB, or resources registered with an AWS Cloud Map service. However, all resources must be owned by the same AWS account (including the load balancer or AWS Cloud Map service, VPC link and HTTP API)
    ([Ref](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-private.html)).
        - https://aws.amazon.com/about-aws/whats-new/2020/03/api-gateway-private-integrations-aws-elb-cloudmap-http-apis-release/
        - https://aws.amazon.com/blogs/compute/building-better-apis-http-apis-now-generally-available/


---
## Public API Gateway and VPC Private DNS setting

See https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-vpc-connections/, AWS, 2020-12-16

Connect to public APIs with private DNS enabled
- If private DNS is enabled, use edge-optimized custom domain names or regional custom domain names to connect to your public APIs.

Connect to public APIs with private DNS disabled
- If private DNS is disabled for the interface VPC endpoint, or there is no endpoint in your Amazon VPC, confirm if the following is true:
   - Security groups for your VPC allow outbound traffic to your public API.
   - The resource policy attached to your API doesn't deny access from the VPC.
- When your Amazon VPC has permission to access your public APIs, use public DNS to connect to your public APIs.


---
## Private API Gateways

1. Private API invocation between two separate AWS accounts
    1. [access-private-apigw-in-another-account](https://github.com/kyhau/access-private-apigw-in-another-account) - This repo provides a working example for calling a private API Gateway REST API from another AWS account, including CloudFormation templates, API test code and GitHub Actions workflows.
    2. [How can I access an API Gateway private REST API in another AWS account using an interface VPC endpoint?](https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-private-cross-account-vpce/), AWS, 2021-10-11
    3. AWS Cross Account Private API demo - [aws-samples/aws-cross-account-private-api-demo](https://github.com/aws-samples/aws-cross-account-private-api-demo)
2. [Be careful with AWS Private API Gateway Endpoints](https://st-g.de/2019/07/be-careful-with-aws-private-api-gateway-endpoints), 2019-07-24
    - The setting **Enable Private DNS Name**,  will prevent all access to any regional/public API Gateway in the whole AWS region!
    - Solution 1:
        - Disable the private DNS name, and
        - Set one of following HTTP headers:
            - `Host: <api-id>.execute-api.<region>.amazonaws.com`, or
            - `x-apigw-api-id: <api-id>`
    - Solution 2:
        - Not require to set custom headers with disabled DNS resolution
        - Use a custom domain name configured in the API Gateway and an ALB in front of it.
        - Based on an IP target group, the ALB would forwards the requests to the ENIs of the VPC Endpoint.
3. https://aws.plainenglish.io/custom-dns-for-private-api-gateway-5940cb4889a8
4. https://aws.amazon.com/blogs/compute/understanding-vpc-links-in-amazon-api-gateway-private-integrations/, 10 AUG 2021


---
## mTLS

- [Consuming private Amazon API Gateway APIs using mutual TLS](https://aws.amazon.com/blogs/compute/consuming-private-amazon-api-gateway-apis-using-mutual-tls/), AWS, 2024-01-23
    - Regional API Gateway endpoints have native support for mTLS but private API Gateway endpoints do not support mTLS, so you must terminate mTLS before API Gateway.
    - Private API Gateway mTLS verification using an ALB.
- [Configure mTLS authentication for Amazon API Gateway](https://aws.amazon.com/blogs/compute/introducing-mutual-tls-authentication-for-amazon-api-gateway/), AWS, 2020-09-17


---
## AWS API Gateway vs. Application Load Balancer (ALB)

- [AWS API Gateway vs. Application Load Balancer (ALB)](https://dashbird.io/blog/aws-api-gateway-vs-application-load-balancer/), dashbird.io, 2020-05-28


---
## Previous Security Issues or Breaking Changes

- [Removing header remapping from Amazon API Gateway, and notes about our work with security researchers](https://aws.amazon.com/blogs/security/removing-header-remapping-from-amazon-api-gateway-and-notes-about-our-work-with-security-researchers/)
   > As of June 14, 2023, the header remapping feature is no longer available in API Gateway.

   > Before we removed the feature, we contacted customers who were using the direct HTTP header remapping feature through email and the AWS Health Dashboard. If you haven’t been contacted, no action is required on your part.

   - See also [Writeup: AWS API Gateway header smuggling and cache confusion](https://securityblog.omegapoint.se/en/writeup-apigw/)
