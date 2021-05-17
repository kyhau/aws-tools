# Step Functions

## Canary Deployment

- [AWS Lambda Canary Deployments with API Gateway](https://blog.thundra.io/aws-lambda-canary-deployments-with-api-gateway)

## Bucket size and Refill Rate per Second In Step Functions

> Some Step Functions API actions are throttled using a token bucket scheme to maintain service bandwidth.

> The bucket size and refill rate refer to the behavior of an algorithm that is conceptually represented by a bucket of tokens. Each time the action occurs, a token must be removed from the bucket, otherwise the action is throttled if no token is available in the bucket.
> The refill rate establishes the sustained rate at which the action is potentially allowed to occur.

> The bucket size is the maximum burst capacity you can "store" to handle surges of activity.

> Buckets are constantly filling at the refill rate. If the event rate is less than the refill rate, they reach their size limit, and the extra (imaginary) tokens fall off the (imaginary) edge of the (imaginary) bucket and disappear, leaving you with a full bucket to provide for smooth bursting as long as you don't exceed the bucket capacity and run out of tokens.

Ref: https://stackoverflow.com/questions/57959933/what-does-refill-rate-mean-for-aws-step-functions

## API Gateway Integration

Notes
- All Step Functions API actions use the HTTP `POST` method. ([Ref](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-api-gateway.html))
- [Using AWS API Gateway and Step Functions without Exposing Your ARN](https://medium.com/@cody_green/using-aws-api-gateway-and-step-functions-without-exposing-your-arn-ce94a88fa594), 2017-10-07
    - By default, ARNs will be exposed in both requests and responses when using Step Functions with API Gateway integration.
    - Solution 1: Add a Lambda between API Gateway and Step Functions.
    - Solution 2: Use body-mapping templates to map SFN ARN in reguests and hide SFN ARNs in responses.

        Request Integration
        ```
        {
            "input": "$util.escapeJavaScript($input.json('$'))",
            "stateMachineArn": ${stageVariables.sfnArn}
        }
        ```

        Responsee Integration
        ```
        {
          "token": "$input.json('$.executionArn').split(':')[7].replace('"', "")"
        }
        ```

## CDK resources
- https://github.com/cdk-patterns/serverless/tree/master/the-state-machine
- https://github.com/cdk-patterns/serverless/tree/master/the-saga-stepfunction
- https://github.com/awslabs/aws-solutions-constructs/tree/master/source/patterns/%40aws-solutions-constructs/aws-lambda-step-function

## Useful links
- [Latest SFN Overview](https://docs.aws.amazon.com/step-functions/latest/dg/how-step-functions-works.html)
- Use Cases
    - https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html
    - https://aws.amazon.com/blogs/compute/implementing-serverless-manual-approval-steps-in-aws-step-functions-and-amazon-api-gateway/
