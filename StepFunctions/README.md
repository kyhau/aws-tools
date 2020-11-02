# Step Functions

Notes
- All Step Functions API actions use the HTTP `POST` method. ([Ref](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-api-gateway.html))
- [Using AWS API Gateway and Step Functions without Exposing Your ARN](https://medium.com/@cody_green/using-aws-api-gateway-and-step-functions-without-exposing-your-arn-ce94a88fa594), 2017-10-07
    - By default, ARNs will be exposed in both requests and responses when using Step Functions with API Gateway integration.
    - Solution 1: Add a Lambda between API Gateway and Step Functions.
    - Solution 2: Use body-mapping templates to map SFN ARN in reguests and hide SFN ARNs in responses.

CDK resources
- https://github.com/cdk-patterns/serverless/tree/master/the-state-machine
- https://github.com/cdk-patterns/serverless/tree/master/the-saga-stepfunction
- https://github.com/awslabs/aws-solutions-constructs/tree/master/source/patterns/%40aws-solutions-constructs/aws-lambda-step-function

Useful links
- [Latest SFN Overview](https://docs.aws.amazon.com/step-functions/latest/dg/how-step-functions-works.html)
- Use Cases
    - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html
    - https://aws.amazon.com/blogs/compute/implementing-serverless-manual-approval-steps-in-aws-step-functions-and-amazon-api-gateway/