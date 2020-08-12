# About Lambda

## Lambda Tricks

- [Hit the 6MB Lambda payload limit? Here’s what you can do](
  https://theburningmonk.com/2020/04/hit-the-6mb-lambda-payload-limit-heres-what-you-can-do/)
  by Yan Cui on 2020-04-09

- [Shave 99.93% off your Lambda bill with this one weird trick](
  https://medium.com/@hichaelmart/shave-99-93-off-your-lambda-bill-with-this-one-weird-trick-33c0acebb2ea)
  by Michael Hart on 2019-12-10
  - The init stage has the same performance as a 1792 MB Lambda, even if we’re only running a 128 MB one.
  - Technically you can do up to 10 seconds of work before it starts getting included in the billed duration.
  - Also, you'll always have to pay something for the handler execution - the minimum billed execution time is 100ms.

## aws-lambda-powertools

- https://awslabs.github.io/aws-lambda-powertools-python/core/logger/
- https://awslabs.github.io/aws-lambda-powertools-python/core/metrics/
- https://awslabs.github.io/aws-lambda-powertools-python/core/tracer/
- https://awslabs.github.io/aws-lambda-powertools-python/utilities/middleware_factory/
- https://aws.amazon.com/blogs/compute/building-well-architected-serverless-applications-understanding-application-health-part-2/

## Lambda Layers

- https://github.com/kyhau/cdk-lambda-layer-datetimenow
- https://github.com/awsdocs/aws-lambda-developer-guide/tree/master/sample-apps/blank-python
- https://stackoverflow.com/questions/59716366/how-to-deploy-and-attach-a-layer-to-aws-lambda-function-using-aws-cdk-and-python
- https://stackoverflow.com/questions/55695187/import-libraries-in-lambda-layers
    > According to the video they should go in either /opt/python or /opt/python/lib/python3.6/site-packages. The video also gives the indication that if you're using 3.7 or above you have to use the second one but I tried it in just /opt/python with 3.8 and it seemed to work. I feel like for simplicity it would be easier to just put in /opt/python but if you're making a layer for multiple versions then maybe you would want to do the second.

## Custom Lambda Runtime

- https://github.com/kyhau/have-a-smile

## Lambda destination

## Auto Scaling Lambda Provisioned Concurrency

## Invoke lambda with awscli

- https://stackoverflow.com/questions/60310607/amazon-aws-cli-not-allowing-valid-json-in-payload-parameter