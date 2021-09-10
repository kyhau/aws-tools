# Some notes about Lambda

- [How to Make Your Lambda Functions Run Faster (and Cheaper)](https://hackernoon.com/how-to-make-your-lambda-functions-run-faster-and-cheaper-gp2034jl) by webiny on 2020-11-25

- Lambda now supports up to 10 GB of memory and 6 vCPU cores
    - Old blog post: [Hit the 6MB Lambda payload limit? Here’s what you can do](
        https://theburningmonk.com/2020/04/hit-the-6mb-lambda-payload-limit-heres-what-you-can-do/)
        by Yan Cui on 2020-04-09

- [Shave 99.93% off your Lambda bill with this one weird trick](
  https://medium.com/@hichaelmart/shave-99-93-off-your-lambda-bill-with-this-one-weird-trick-33c0acebb2ea)
  by Michael Hart on 2019-12-10
  - The init stage has the same performance as a 1792 MB Lambda, even if we’re only running a 128 MB one.
  - Technically you can do up to 10 seconds of work before it starts getting included in the billed duration.
  - Also, you'll always have to pay something for the handler execution - the minimum billed execution time is 100ms.

- Cannot do `ping` from Lambda Function (see [AWS Lambda FAQs](https://aws.amazon.com/lambda/faqs/))
  > Lambda attempts to impose as few restrictions as possible on normal language and operating system activities, but there are a few activities that are disabled: Inbound network connections are blocked by AWS Lambda, and for outbound connections, only TCP/IP and UDP/IP sockets are supported, and ptrace (debugging) system calls are blocked. TCP port 25 traffic is also blocked as an anti-spam measure.

- non-async handlers and `context.callbackWaitsForEmptyEventLoop = false`
  - By default calling the callback() function in a NodeJS Lambda function does not end the function execution. It will continue running until the event loop is empty. A common issue with NodeJS Lambda functions continuing to run after callback is called occurs when you are holding on to open database connections.
I solved my problems with set to callbackWaitsForEmptyEventLoop = false.
  - https://stackoverflow.com/questions/53296201/request-time-out-from-aws-lambda/53312129
  - https://stackoverflow.com/questions/37791258/lambda-timing-out-after-calling-callback
  - https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html (edited)
     - > For non-async handlers, function execution continues until the event loop is empty or the function times out. The response isn't sent to the invoker until all event loop tasks are finished. If the function times out, an error is returned instead. You can configure the runtime to send the response immediately by setting context.callbackWaitsForEmptyEventLoop to false.


## Container Image, Lambda Layers, Lambda Extensions

- Working with Lambda layers and extensions in container images ([blog post](https://aws.amazon.com/blogs/compute/working-with-lambda-layers-and-extensions-in-container-images/))

- Optimizing Lambda functions packaged as container images ([blog post](https://aws.amazon.com/blogs/compute/optimizing-lambda-functions-packaged-as-container-images/))

### Lambda Layers

- Deploy Lambda Layer wwith CDK - example: https://github.com/kyhau/cdk-examples/tree/master/python/cdk-lambda-layer-datetimenow


## APIs
- Lambda Extensions API https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html
- Lambda Logs API https://docs.aws.amazon.com/lambda/latest/dg/runtimes-logs-api.html
- Lambda runtime API https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html


## Using SAM CLI with the CDK to test a Lambda function locally

- Example: https://github.com/kyhau/slack-command-app-cdk
- https://docs.aws.amazon.com/cdk/latest/guide/sam.html


## aws-lambda-powertools

- https://awslabs.github.io/aws-lambda-powertools-python/core/logger/
- https://awslabs.github.io/aws-lambda-powertools-python/core/metrics/
- https://awslabs.github.io/aws-lambda-powertools-python/core/tracer/
- https://awslabs.github.io/aws-lambda-powertools-python/utilities/middleware_factory/
- https://aws.amazon.com/blogs/compute/building-well-architected-serverless-applications-understanding-application-health-part-2/


## Lambda code signing with AWS Signer

## Lambda Error Patterns and Logging

- [How to get notified on specific Lambda function error patterns using CloudWatch](https://aws.amazon.com/blogs/mt/get-notified-specific-lambda-function-error-patterns-using-cloudwatch/) AWS Management & Governance Blog, 2020-08-24

## Custom Lambda Runtime

## Lambda destination

## Auto Scaling Lambda Provisioned Concurrency

## Invoke lambda with awscli

- https://stackoverflow.com/questions/60310607/amazon-aws-cli-not-allowing-valid-json-in-payload-parameter
