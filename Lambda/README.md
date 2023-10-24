# Lambda notes

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Synchronous Invokes, Asynchronous Invokes, Poll-Based Invokes](#synchronous-invokes-asynchronous-invokes-poll-based-invokes)
- [MLTA, Debugging, Error Handling](#mlta-debugging-error-handling)
    - [Useful blog posts](#useful-blog-posts)
    - [How errors should be handled for Asynchronous Invocations](#how-error-should-be-handled-for-asynchronous-invocations)
- [Code storage for uploaded Lambda functions (`CodeStorageExceededException`)](#code-storage-for-uploaded-lambda-functions-codestorageexceededexception)
- [Lambda Scaling and Throughput](#lambda-scaling-and-throughput)
    - [Scaling Quotas](#scaling-quotas)
    - [Provisioned Concurrency](#provisioned-concurrency)
    - [Estimate concurrent requests](#estimate-concurrent-requests)
    - [Throttling error and asynchronous/synchronous invocations](#throttling-error-and-asynchronoussynchronous-invocations)
    - [Operational metrics](#operational-metrics)
- [Lambda Performance Optimisation](#lambda-performance-optimisation)
- [Lambda Cost Optimisaton](#lambda-cost-optimisation)
- [Lambda Function URLs](#lambda-function-urls)
- [Lambda Response Streaming](#lambda-response-streaming)
- [Lambda Container Images](#lambda-container-images)
- [Lambda Layers](#lambda-layers)
- [Lambda Extensions](#lambda-extensions)
- [Gotchas](#gotchas)
    - [Lambda Python Runtimes - Python 3.6/3.7 are Amazon Linux 1 and Python 3.8/3.9 are Amazon Linux 2](#lambda-python-runtimes---python-3637-are-amazon-linux-1-and-python-3839-are-amazon-linux-2)
    - [AWS CLI not allowing valid JSON in payload parameter with lambda invoke](#aws-cli-not-allowing-valid-json-in-payload-parameter-with-lambda-invoke)
    - [Cannot do `ping` from Lambda Function](#cannot-do-ping-from-lambda-function)
    - [Non-async handlers and `context.callbackWaitsForEmptyEventLoop = false`](#non-async-handlers-and-contextcallbackwaitsforemptyeventloop--false)


---
## Useful Libs and Tools

- Lambda base container images
    - [aws-lambda-base-images](https://github.com/aws/aws-lambda-base-images)
- Lambda execution environment
    - [AWS Lambda Extensions API specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html)
    - [AWS Lambda Logs API specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-logs-api.html)
    - [AWS Lambda Runtime API specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html)
    - [aws-lambda-extensions](https://github.com/aws-samples/aws-lambda-extensions/) - AWS Lambda Extensions sample projects
- Lambda Container Images
    - [gallery.ecr.aws/lambda](https://gallery.ecr.aws/lambda?page=1) - AWS Lambda base images
    - [awslambdaric](https://github.com/aws/aws-lambda-python-runtime-interface-client) - AWS Lambda Python Runtime Interface Client (RIC)
    - [aws-lambda-runtime-interface-emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator/)  -  AWS Lambda Runtime Interface Emulator (RIE)
    - Example: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
- Lambda Powertools
    - [cdk-aws-lambda-powertools-layer](https://github.com/awslabs/cdk-aws-lambda-powertools-layer) - AWS Lambda powertools layer
    - [aws-lambda-powertools-dotnet](https://github.com/awslabs/aws-lambda-powertools-dotnet/) - AWS Lambda Powertools for .NET
    - [aws-lambda-powertools-java](https://github.com/awslabs/aws-lambda-powertools-java) - AWS Lambda Powertools for Java
    - [aws-lambda-powertools-python](https://github.com/awslabs/aws-lambda-powertools-python) - AWS Lambda Powertools for Python
        - https://awslabs.github.io/aws-lambda-powertools-python/core/logger/
        - https://awslabs.github.io/aws-lambda-powertools-python/core/metrics/
        - https://awslabs.github.io/aws-lambda-powertools-python/core/tracer/
        - https://awslabs.github.io/aws-lambda-powertools-python/utilities/middleware_factory/
        - https://aws.amazon.com/blogs/compute/building-well-architected-serverless-applications-understanding-application-health-part-2/
    - [aws-lambda-powertools-typescript](https://github.com/awslabs/aws-lambda-powertools-typescript) - AWS Lambda Powertools for TypeScript
- Tuning
    - [alexcasalboni/aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) - AWS Lambda Power Tuning is a state machine powered by AWS Step Functions that helps you optimize your Lambda functions for cost and/or performance in a data-driven way.
- [aws-lambda-builders](https://github.com/aws/aws-lambda-builders) - Lambda Builders is a Python library to compile, build and package AWS Lambda functions for several runtimes & frameworks. Lambda Builders is the brains behind the `sam build`.
- [aws-lambda-dotnet](https://github.com/aws/aws-lambda-dotnet) - Lambda Annotations Framework for .NET
- [aws-lambda-developer-guide](https://github.com/awsdocs/aws-lambda-developer-guide) - AWS Lambda Developer Guide with examples
- [authorization-lambda-at-edge](https://github.com/aws-samples/authorization-lambda-at-edge) - Authorization Lambda@Edge (Node.js)
- [cargo-lambda](https://github.com/cargo-lambda/cargo-lambda) - Cargo Lambda provides tools and workflows to help you get started building Rust functions for AWS Lambda from scratch.
- [lambci/docker-lambda](https://github.com/lambci/docker-lambda) - A sandboxed local environment that replicates the live AWS Lambda environment
- Using SAM CLI with the CDK to test a Lambda function locally
    - https://docs.aws.amazon.com/cdk/latest/guide/sam.html
    - Example: https://github.com/kyhau/slack-command-app-cdk

---

## Synchronous Invokes, Asynchronous Invokes, Poll-Based Invokes

- [Understanding the Different Ways to Invoke Lambda Functions](https://aws.amazon.com/blogs/architecture/understanding-the-different-ways-to-invoke-lambda-functions/), AWS, 2019-07-02
- [How to trigger a Lambda function at specific time in AWS](https://stackoverflow.com/questions/48538170/how-to-trigger-a-lambda-function-at-specific-time-in-aws)
    - E.g. SQS (message with a `due-date`) -> EventBridge Pipes -> Step Function (WaitTillScheduled `due-date`) -> Lambda


---

## MLTA, Debugging, Error Handling

- Lambda Performance Insights
- Lambda Powertools (Python, Java, TypeScript, .NET) - used as lib or as a layer
    - Distributed tracing
    - Structured logging
    - Async metrics
    - Event routing (Python only)
    - Streaming (Python only)
- Lambda Telemetry API (Lambda Extensions, New Relic, Sumo Logic) - deployed as layers
    - https://aws.amazon.com/blogs/compute/introducing-the-aws-lambda-telemetry-api/
- CloudWatch
    - [How to get notified on specific Lambda function error patterns using CloudWatch](https://aws.amazon.com/blogs/mt/get-notified-specific-lambda-function-error-patterns-using-cloudwatch/), AWS, 2020-08-24

### Useful blog posts

- [Implementing AWS Lambda error handling patterns](https://aws.amazon.com/blogs/compute/implementing-aws-lambda-error-handling-patterns/), AWS, 2023-07-06
- [Implementing error handling for AWS Lambda asynchronous invocations](https://aws.amazon.com/blogs/compute/implementing-error-handling-for-aws-lambda-asynchronous-invocations/), AWS, 2023-04-25

### How error should be handled for Asynchronous Invocations

1. Lambda Destinations + X-Ray traces
    - With Destinations, you will be able to send asynchronous function execution results to a destination resource without writing code.
        For each execution status (i.e. Success and Failure), you can choose one destination from four options:
        - another Lambda function,
        - an SNS topic,
        - an SQS standard queue, or
        - EventBridge.
2. [Dead-letter queues](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-dlq)


---

## Code storage for uploaded Lambda functions (`CodeStorageExceededException`)

The Lambda service stores your function code in an internal **S3 bucket** that's private to your account. Each AWS account is allocated **75 GB of storage in each Region** (and can be increased up to Terabytes). Code storage includes the total storage used by both **Lambda functions and layers**. If you reach the quota, you receive a **`CodeStorageExceededException`** when you attempt to deploy new functions.

See [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html).

### To see the storage used

1. From AWS Lambda console > Dashboard
2. From AWS CLI:
    ```
    aws lambda list-versions-by-function --function-name myTestFunction
    aws lambda get-layer-version --layer-version --layer-name TestLayer --version-number 2
    ```
    This returns each published version of the function/layer together with the $LATEST version. The CodeSize attribute shows the total number of bytes used by code storage of this function/layer.

See [Monitoring Lambda code storage](https://docs.aws.amazon.com/lambda/latest/operatorguide/code-storage.html).

### To manage the storage used

It's best practice to manage the storage space available and clean up old versions of functions and remove unused code.
- For Serverless, you may use the Serverless plugin [serverless-prune-plugin](https://www.serverless.com/plugins/serverless-prune-plugin).

See [Best practices for managing code storage](https://docs.aws.amazon.com/lambda/latest/operatorguide/code-storage-best-practice.html).


---

## Lambda Scaling and Throughput

### Scaling quotas

There are two scaling quotas to consider with **concurrency: account concurrency quota** and **burst concurrency quota**.

- The **account concurrency** is the maximum concurrency in a particular Region. This is shared across all functions in an account. The default Regional concurrency quota starts at 1,000, which you can increase with a service ticket.

- The **burst concurrency quota** provides an initial burst of traffic for each function, between 500 and 3000 per minute, depending on the [Region](https://docs.aws.amazon.com/lambda/latest/dg/invocation-scaling.html). After this initial burst, functions can scale by another 500 concurrent invocations per minute for all Regions. If you reach the maximum number of concurrent requests, further requests are **throttled**.

### Provisioned Concurrency

The function initialization process can introduce latency for your applications. You can **reduce this latency** by configuring **Provisioned Concurrency** for **a function version or alias**. This prepares runtime environments in advance, running the function initialization process, so the function is ready to invoke when needed.

This is primarily useful for **synchronous requests** to ensure you have enough concurrency before an expected traffic spike. You can still burst above this using **standard concurrency**.

You can use [Application Auto Scaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html) to adjust Provisioned Concurrency automatically based on Lambda's utilization metric.

### Estimate concurrent requests

- Each **runtime environment** processes **a single request at a time**. While a single runtime environment is processing a request, it cannot process other requests.
- The **number of runtime environments** determines the **concurrency**. This is the sum of all **concurrent requests** for currently running functions at a particular point in time.
- The **number of transactions** Lambda can process per second is the sum of **all invokes** for that period.
- Reducing a function's **invocation duration** can increase the **transactions per second** that a function can process.

To estimate **concurrent requests** from the number of requests per unit of time (e.g. seconds) and their average duration, using the formula:

**_RequestsPerSecond x AvgDurationInSeconds = concurrent requests_**

For example, if a Lambda function takes an average 500 ms to run, at 100 requests per second, the number of concurrent requests is 50:

_100 requests/second x 0.5 sec = 50 concurrent requests_

See this [blog post](https://aws.amazon.com/blogs/compute/understanding-aws-lambda-scaling-and-throughput/) for more examples.

### Throttling error and asynchronous/synchronous invocations

- For **synchronous invocations**, Lambda returns a throttling error (`429`) to the caller, which must retry the request.
- With **asynchronous** and **event source mapping** invokes, Lambda automatically retries the requests.

See also
- [Understanding AWS Lambda’s invoke throttling limits](https://aws.amazon.com/blogs/compute/understanding-aws-lambdas-invoke-throttle-limits/), AWS, 2023-07-07


### Operational metrics

There are CloudWatch metrics available to monitor your account and function concurrency to ensure that your applications can scale as expected. Monitor function Invocations and Duration to understand throughput. Throttles show throttled invocations.

- **ConcurrentExecutions** tracks the total number of runtime environments that are processing events. Ensure this doesn't reach your account concurrency to avoid account throttling. Use the metric for individual functions to see which are using account concurrency, and also ensure reserved concurrency is not too high. For example, a function may have a reserved concurrency of 2000, but is only using 10.
- **UnreservedConcurrentExecutions** show the number of function invocations without reserved concurrency. This is your available account concurrency buffer.
- Use **ProvisionedConcurrencyUtilization** to ensure you are not paying for Provisioned Concurrency that you are not using. The metric shows the percentage of allocated Provisioned Concurrency in use.
- **ProvisionedConcurrencySpilloverInvocations** show function invocations using standard concurrency, above the configured Provisioned Concurrency value. This may show that you need to increase Provisioned Concurrency.

See [Understanding AWS Lambda scaling and throughput](https://aws.amazon.com/blogs/compute/understanding-aws-lambda-scaling-and-throughput/).


---

## Lambda Performance Optimisation

Some good reads:
- [Optimizing AWS Lambda extensions in C# and Rust](https://aws.amazon.com/blogs/compute/optimizing-aws-lambda-extensions-in-c-and-rust/), AWS, 13 Apr 2023
- [Understanding AWS Lambda scaling and throughput](https://aws.amazon.com/blogs/compute/understanding-aws-lambda-scaling-and-throughput/), AWS, 18 Jul 2022
- [Optimizing Node.js dependencies in AWS Lambda](https://aws.amazon.com/blogs/compute/optimizing-node-js-dependencies-in-aws-lambda/), AWS, 13 JUL 2022
- [Optimizing AWS Lambda function performance for Java](https://aws.amazon.com/blogs/compute/optimizing-aws-lambda-function-performance-for-java/), AWS, 31 MAR 2022
- [How to Make Your Lambda Functions Run Faster (and Cheaper)](https://hackernoon.com/how-to-make-your-lambda-functions-run-faster-and-cheaper-gp2034jl) by webiny on 2020-11-25
- [Shave 99.93% off your Lambda bill with this one weird trick](
  https://medium.com/@hichaelmart/shave-99-93-off-your-lambda-bill-with-this-one-weird-trick-33c0acebb2ea)
  by Michael Hart on 2019-12-10
  - The init stage has the same performance as a 1792 MB Lambda, even if we're only running a 128 MB one.
  - Technically you can do up to 10 seconds of work before it starts getting included in the billed duration.
  - Also, you'll always have to pay something for the handler execution - the minimum billed execution time is 100ms.
  - [Using AWS Lambda with AWS X-Ray](https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html) - AWS X-Ray can provide sampling of cross-component breakdown of where initialisation, execution and integration time is being spent.

See also [Lambda - Performance optimization](https://docs.aws.amazon.com/lambda/latest/operatorguide/perf-optimize.html).


---

## Lambda Cost Optimisation

- Right-sizing memory allocation
    - Tools
        1. [AWS Lambda Power Tuning](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning)
        2. [AWS Compute Optimizer](https://aws.amazon.com/compute-optimizer/)
- Setting a realistic function timeout
- Using Graviton
- [Filtering event sources for AWS Lambda functions](https://aws.amazon.com/blogs/compute/filtering-event-sources-for-aws-lambda-functions/)
- [Avoiding recursive invocation with Amazon S3 and AWS Lambda](https://aws.amazon.com/blogs/compute/avoiding-recursive-invocation-with-amazon-s3-and-aws-lambda/)

Useful blog posts
- [Understanding techniques to reduce AWS Lambda costs in serverless applications](https://aws.amazon.com/blogs/compute/understanding-techniques-to-reduce-aws-lambda-costs-in-serverless-applications/), AWS, 20 Apr 2023


---

## Lambda Function URLs

The Lambda Function URLs feature was introduced in April 2022. A function URL is a dedicated HTTP(S) endpoint for the Lambda function (`https://<url-id>.lambda-url.<region>.on.aws`)

Lambda function URLs use resource-based policies for security and access control. **When [AuthType = None](https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html), resource-based policy that grants public access, any unauthenticated user with your function URL can invoke your function)**.

Recommendation:
- Use SCP to deny following actions:
    - `lambda:CreateFunctionUrlConfig`
    - `lambda:UpdateFunctionUrlConfig`

Useful blog posts
- [Protecting an AWS Lambda function URL with Amazon CloudFront and Lambda@Edge](https://aws.amazon.com/blogs/compute/protecting-an-aws-lambda-function-url-with-amazon-cloudfront-and-lambdaedge/), AWS, 2023-08-23
- [Building a Serverless ASP.NET Core Web API with AWS Lambda using Function URLs](https://coderjony.com/blogs/building-a-serverless-aspnet-core-web-api-with-aws-lambda-using-function-urls), 2022-10-02
    - To make the API available on a public HTTP(S) endpoint, generally 2 approaches
        1. along with Amazon API Gateway
        2. use Lambda function URLs


---

## Lambda Response Streaming

- [Using response streaming with AWS Lambda Web Adapter to optimize performance](https://aws.amazon.com/blogs/compute/using-response-streaming-with-aws-lambda-web-adapter-to-optimize-performance/), AWS, 2023-08-07
- [Introducing AWS Lambda response streaming](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-response-streaming/), AWS, 2023-04-07


---
## Lambda Container Images

- [Previewing environments using containerized AWS Lambda functions](https://aws.amazon.com/blogs/compute/previewing-environments-using-containerized-aws-lambda-functions/) (using Lamda URL, Lambda extension), AWS, 2023-02-06
- Optimizing Lambda functions packaged as container images ([blog post](https://aws.amazon.com/blogs/compute/optimizing-lambda-functions-packaged-as-container-images/))
- Working with Lambda layers and extensions in container images ([blog post](https://aws.amazon.com/blogs/compute/working-with-lambda-layers-and-extensions-in-container-images/))


---

## Lambda Layers

- [Centralizing management of AWS Lambda layers across multiple AWS Accounts](https://aws.amazon.com/blogs/compute/centralizing-management-of-aws-lambda-layers-across-multiple-aws-accounts/)
, AWS, 2023-09-19
    - [aws-samples/lambda-layer-management](https://github.com/aws-samples/lambda-layer-management)
    - With AWS Config, EventBridge Scheduler, SSM Automation, StackSets.
    - On demand query example:
    ```
    aws configservice select-aggregate-resource-config \
        --expression "SELECT accountId, awsRegion, configuration.functionName, configuration.version WHERE resourceType = 'AWS::Lambda::Function' AND configuration.layers.arn = 'YOUR_LAYER_ARN'" \
        --configuration-aggregator-name 'YOUR_AGGREGATOR_NAME' \
        --query "Results" \
        --output json | \
        jq -r '.[] | fromjson | [.accountId, .awsRegion, .configuration.functionName, .configuration.version] | @csv' > output.csv
    ```


---

## Lambda Extensions

- Running a web server in Lambda with Lambda extension - [Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter) - [blog post](https://aws.amazon.com/blogs/compute/previewing-environments-using-containerized-aws-lambda-functions/).


---
## Gotchas

### Lambda Python Runtimes - Python 3.6/3.7 are Amazon Linux 1 and Python 3.8/3.9 are Amazon Linux 2

Python 3.6/3.7 are Amazon Linux 1 and Python 3.8/3.9 are Amazon Linux 2.

In general it should be fine to upgrade from Python 3.6 to 3.9. But there are cases you'll need to make some changes. For example: If you have code utilizing some sys call, e.g. `curl` - `curl` is not installed in Amazon Linux 2 by default.


### AWS CLI not allowing valid JSON in payload parameter with lambda invoke

If you see error like `Invalid base64:`, it could be because since awscli 2, payloads need to be base64 encoded when invoking a Lambda function.

> By default, the AWS CLI version 2 now passes all binary input and binary output parameters as base64-encoded strings. A parameter that requires binary input has its type specified as blob (binary large object) in the documentation.

You will need to pass in also `--cli-binary-format raw-in-base64-out`. For example:
```
aws lambda invoke --function-name testsms \
    --invocation-type Event \
    --cli-binary-format raw-in-base64-out \
    --payload '{"key": "test"}' response.json
```
See also
- https://github.com/aws/aws-cli/issues/4968
- https://stackoverflow.com/questions/60310607/amazon-aws-cli-not-allowing-valid-json-in-payload-parameter


### Cannot do `ping` from Lambda Function

See [AWS Lambda FAQs](https://aws.amazon.com/lambda/faqs/)
> Lambda attempts to impose as few restrictions as possible on normal language and operating system activities, but there are a few activities that are disabled: Inbound network connections are blocked by AWS Lambda, and for outbound connections, only TCP/IP and UDP/IP sockets are supported, and ptrace (debugging) system calls are blocked. TCP port 25 traffic is also blocked as an anti-spam measure.


### Non-async handlers and `context.callbackWaitsForEmptyEventLoop = false`

- By default calling the callback() function in a NodeJS Lambda function does not end the function execution. It will continue running until the event loop is empty. A common issue with NodeJS Lambda functions continuing to run after callback is called occurs when you are holding on to open database connections.

I solved my problems with set to callbackWaitsForEmptyEventLoop = false.
  - https://stackoverflow.com/questions/53296201/request-time-out-from-aws-lambda/53312129
  - https://stackoverflow.com/questions/37791258/lambda-timing-out-after-calling-callback
  - https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html (edited)
     - > For non-async handlers, function execution continues until the event loop is empty or the function times out. The response isn't sent to the invoker until all event loop tasks are finished. If the function times out, an error is returned instead. You can configure the runtime to send the response immediately by setting context.callbackWaitsForEmptyEventLoop to false.
