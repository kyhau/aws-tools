# API Gateway

1. Creating a private API in Amazon API Gateway ([AWS doc](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html))
1. Be careful with AWS Private API Gateway Endpoints ([Ref](https://st-g.de/2019/07/be-careful-with-aws-private-api-gateway-endpoints))
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
