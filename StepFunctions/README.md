# Step Functions

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Bucket size and Refill Rate per Second In Step Functions](#bucket-size-and-refill-rate-per-second-in-step-functions)
- [API Gateway Integration](#api-gateway-integration)


---
## Useful Libs and Tools

- [aws/aws-step-functions-data-science-sdk-python](https://github.com/aws/aws-step-functions-data-science-sdk-python) - AWS Step Functions Data Science SDK (Python)
- CDK resources
    - https://github.com/cdk-patterns/serverless/tree/master/the-state-machine
    - https://github.com/cdk-patterns/serverless/tree/master/the-saga-stepfunction
    - https://github.com/awslabs/aws-solutions-constructs/tree/master/source/patterns/%40aws-solutions-constructs/aws-lambda-step-function
- Triggering a State Machine from SQS using EventBridge Pipes - [example](https://github.com/aws-samples/aws-stepfunctions-examples/blob/main/sam/demo-trigger-stepfunctions-from-sqs/template.yaml)


---
## Useful Articles and Blogs

- [Using JSONPath effectively in AWS Step Functions](https://aws.amazon.com/blogs/compute/using-jsonpath-effectively-in-aws-step-functions/), AWS, 2021-10-14
- [Latest Step Functions Overview](https://docs.aws.amazon.com/step-functions/latest/dg/how-step-functions-works.html)
- [Sample projects for Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/create-sample-projects.html), AWS
- Use Cases
    - [Implementing patterns that exit early out of a parallel state in AWS Step Functions](https://aws.amazon.com/blogs/compute/implementing-patterns-that-exit-early-out-of-a-parallel-state-in-aws-step-functions/), AWS, 2023-07-20
    - [How to trigger a Lambda function at specific time with Step Function](https://stackoverflow.com/questions/48538170/how-to-trigger-a-lambda-function-at-specific-time-in-aws)
    - [SQS triggering Step Functions using EventBridge Pipes](https://stackoverflow.com/questions/53422296/aws-sqs-trigger-step-functions)
    - [Implementing Serverless Manual Approval Steps in AWS Step Functions and Amazon API Gateway](https://aws.amazon.com/blogs/compute/implementing-serverless-manual-approval-steps-in-aws-step-functions-and-amazon-api-gateway/), AWS, 2017-02-15


---
## Bucket size and Refill Rate per Second In Step Functions

> Some Step Functions API actions are throttled using a token bucket scheme to maintain service bandwidth.

> The bucket size and refill rate refer to the behavior of an algorithm that is conceptually represented by a bucket of tokens. Each time the action occurs, a token must be removed from the bucket, otherwise the action is throttled if no token is available in the bucket.
> The refill rate establishes the sustained rate at which the action is potentially allowed to occur.

> The bucket size is the maximum burst capacity you can "store" to handle surges of activity.

> Buckets are constantly filling at the refill rate. If the event rate is less than the refill rate, they reach their size limit, and the extra (imaginary) tokens fall off the (imaginary) edge of the (imaginary) bucket and disappear, leaving you with a full bucket to provide for smooth bursting as long as you don't exceed the bucket capacity and run out of tokens.

Ref: https://stackoverflow.com/questions/57959933/what-does-refill-rate-mean-for-aws-step-functions


> State Transitioning Limit is related to what you are trying to do. Each Lambda execution counts as at least one StateTransition. It depends on your state machine.
<br>
For example if you have a wait state after Task State (Lambda) then you have two StateTransitions for each lambda call.

> If you are executing 1 Lambda per state machine, then you should consider StartExecution limits too:

Ref: https://stackoverflow.com/questions/66178900/can-step-function-handle-500-execution-per-second


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
