# Lambda notes

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [CDK, CLI, SAM](#cdk-cli-sam)
- [Container Images, Lambda Layers, Lambda Extensions](#container-images-lambda-layers-lambda-extensions)
- [Performance Optimisation](#performance-optimisation)
- [Useful Articles and Blogs](#useful-articles-and-blogs)


---
## Useful Libs and Tools

- [AWS Lambda Extensions API specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html)
- [AWS Lambda Logs API specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-logs-api.html)
- [AWS Lambda Runtime API specification](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-api.html)
- AWS Lambda Powertools
    - https://awslabs.github.io/aws-lambda-powertools-python/core/logger/
    - https://awslabs.github.io/aws-lambda-powertools-python/core/metrics/
    - https://awslabs.github.io/aws-lambda-powertools-python/core/tracer/
    - https://awslabs.github.io/aws-lambda-powertools-python/utilities/middleware_factory/
    - https://aws.amazon.com/blogs/compute/building-well-architected-serverless-applications-understanding-application-health-part-2/
- [aws-lambda-builders](https://github.com/aws/aws-lambda-builders) - Lambda Builders is a Python library to compile, build and package AWS Lambda functions for several runtimes & frameworks. Lambda Builders is the brains behind the `sam build`.
- [aws-lambda-developer-guide](https://github.com/awsdocs/aws-lambda-developer-guide) - AWS Lambda Developer Guide with examples
- [aws-lambda-extensions](https://github.com/aws-samples/aws-lambda-extensions/) - AWS Lambda Extensions sample projects
- [aws-lambda-python-runtime-interface-client](https://github.com/aws/aws-lambda-python-runtime-interface-client) - AWS Lambda Python Runtime Interface Client
- [aws-lambda-runtime-interface-emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator/)  -  AWS Lambda Runtime Interface Emulator
- [authorization-lambda-at-edge](https://github.com/aws-samples/authorization-lambda-at-edge) - Authorization Lambda@Edge (Node.js)
- [alexcasalboni/aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning) - AWS Lambda Power Tuning is a state machine powered by AWS Step Functions that helps you optimize your Lambda functions for cost and/or performance in a data-driven way.
- [lambci/docker-lambda](https://github.com/lambci/docker-lambda) - A sandboxed local environment that replicates the live AWS Lambda environment


---
## CDK, CLI, SAM

- Using SAM CLI with the CDK to test a Lambda function locally
    - Example: https://github.com/kyhau/slack-command-app-cdk
    - https://docs.aws.amazon.com/cdk/latest/guide/sam.html
- https://stackoverflow.com/questions/60310607/amazon-aws-cli-not-allowing-valid-json-in-payload-parameter


---
## Container Images, Lambda Layers, Lambda Extensions

- Working with Lambda layers and extensions in container images ([blog post](https://aws.amazon.com/blogs/compute/working-with-lambda-layers-and-extensions-in-container-images/))
- Optimizing Lambda functions packaged as container images ([blog post](https://aws.amazon.com/blogs/compute/optimizing-lambda-functions-packaged-as-container-images/))


---
## Performance Optimisation

- [Optimizing AWS Lambda function performance for Java](https://aws.amazon.com/blogs/compute/optimizing-aws-lambda-function-performance-for-java/), AWS, 31 MAR 2022
- [How to Make Your Lambda Functions Run Faster (and Cheaper)](https://hackernoon.com/how-to-make-your-lambda-functions-run-faster-and-cheaper-gp2034jl) by webiny on 2020-11-25
- [Shave 99.93% off your Lambda bill with this one weird trick](
  https://medium.com/@hichaelmart/shave-99-93-off-your-lambda-bill-with-this-one-weird-trick-33c0acebb2ea)
  by Michael Hart on 2019-12-10
  - The init stage has the same performance as a 1792 MB Lambda, even if we’re only running a 128 MB one.
  - Technically you can do up to 10 seconds of work before it starts getting included in the billed duration.
  - Also, you'll always have to pay something for the handler execution - the minimum billed execution time is 100ms.


---
## Useful Articles and Blogs

- [How to get notified on specific Lambda function error patterns using CloudWatch](https://aws.amazon.com/blogs/mt/get-notified-specific-lambda-function-error-patterns-using-cloudwatch/), AWS, 2020-08-24
- Cannot do `ping` from Lambda Function (see [AWS Lambda FAQs](https://aws.amazon.com/lambda/faqs/))
  > Lambda attempts to impose as few restrictions as possible on normal language and operating system activities, but there are a few activities that are disabled: Inbound network connections are blocked by AWS Lambda, and for outbound connections, only TCP/IP and UDP/IP sockets are supported, and ptrace (debugging) system calls are blocked. TCP port 25 traffic is also blocked as an anti-spam measure.
- Non-async handlers and `context.callbackWaitsForEmptyEventLoop = false`
  - By default calling the callback() function in a NodeJS Lambda function does not end the function execution. It will continue running until the event loop is empty. A common issue with NodeJS Lambda functions continuing to run after callback is called occurs when you are holding on to open database connections.
I solved my problems with set to callbackWaitsForEmptyEventLoop = false.
  - https://stackoverflow.com/questions/53296201/request-time-out-from-aws-lambda/53312129
  - https://stackoverflow.com/questions/37791258/lambda-timing-out-after-calling-callback
  - https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html (edited)
     - > For non-async handlers, function execution continues until the event loop is empty or the function times out. The response isn't sent to the invoker until all event loop tasks are finished. If the function times out, an error is returned instead. You can configure the runtime to send the response immediately by setting context.callbackWaitsForEmptyEventLoop to false.
