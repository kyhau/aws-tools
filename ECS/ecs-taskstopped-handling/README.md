# ECS Task Stopped Handler #

The Task Stopped Handler is deployed as a AWS Lambda function for handling ECS Task Stopped events.

## Templates

1. [LambdaInit-ForTaskStoppedHandling.yaml](LambdaInit-ForTaskStoppedHandling.yaml)
    - Create a Lambda function with dummy content for TaskStoppedHandler.

2. [CloudWatchEventRule-ForTaskStoppedHandling.yaml](CloudWatchEventRule-ForTaskStoppedHandling.yaml)
    - Create CloudWatch Event Rule for triggering Lambda function on ECS Task Stopped event.
