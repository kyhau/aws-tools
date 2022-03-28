# API Gateway

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)


---
## Useful Libs and Tools

| Description | Repo/Link |
| :--- | :--- |
| Amazon API Gateway CORS Configurator | [aws-samples/amazon-api-gateway-cors-configurator](https://github.com/aws-samples/amazon-api-gateway-cors-configurator) |
| [Amazon API Gateway Serverless Developer Portal](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-developer-portal.html) | [awslabs/aws-api-gateway-developer-portal](https://github.com/awslabs/aws-api-gateway-developer-portal) |


---
## Useful Articles and Blogs

1. Private API invocation between two separate AWS accounts
    1. [How can I access an API Gateway private REST API in another AWS account using an interface VPC endpoint?](https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-private-cross-account-vpce/), AWS, 2021-10-11
    1. AWS Cross Account Private API demo - [aws-samples/aws-cross-account-private-api-demo](https://github.com/aws-samples/aws-cross-account-private-api-demo)
1. [Architecting multiple microservices behind a single domain with API Gateway](https://aws.amazon.com/blogs/compute/architecting-multiple-microservices-behind-a-single-domain-with-amazon-api-gateway/), AWS, 2020-09-18
1. [API Gateway for multi account architecture](https://www.levvel.io/resource-library/aws-api-gateway-for-multi-account-architecture), levvel.io, 2019-10-02
1. [AWS API Gateway vs. Application Load Balancer (ALB)](https://dashbird.io/blog/aws-api-gateway-vs-application-load-balancer/), dashbird.io, 2020-05-28
1. Public and private API Gateways
    1. https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-vpc-connections/, AWS, 2020-12-16
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
    4. https://aws.amazon.com/blogs/compute/understanding-vpc-links-in-amazon-api-gateway-private-integrations/
1. Connecting API Gateway and private ALB ([stackoverflow](https://stackoverflow.com/questions/50782573/connecting-aws-api-gateway-and-private-alb))
    1. For a REST API, you can create a VPC link to an NLB. The NLB and API must be owned by the same AWS account ([Ref](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-with-private-integration.html)).
        - You can create a VPC link to an NLB, but not an ALB (that's the invalid endpoint address issue you've been seeing)
    1. For a HTTP API, you can create a VPC link to an ALB, NLB, or resources registered with an AWS Cloud Map service. However, all resources must be owned by the same AWS account (including the load balancer or AWS Cloud Map service, VPC link and HTTP API)
    ([Ref](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-private.html)).
        - https://aws.amazon.com/about-aws/whats-new/2020/03/api-gateway-private-integrations-aws-elb-cloudmap-http-apis-release/
        - https://aws.amazon.com/blogs/compute/building-better-apis-http-apis-now-generally-available/
1. [Using static IP addresses for Application Load Balancers (NLB->ALB)](https://aws.amazon.com/blogs/networking-and-content-delivery/using-static-ip-addresses-for-application-load-balancers/), 2018-04-20
