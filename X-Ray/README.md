## Some links

- https://aws.amazon.com/blogs/compute/building-well-architected-serverless-applications-understanding-application-health-part-2/

- Dynamically adjusting X-Ray sampling rules
  https://aws.amazon.com/blogs/mt/dynamically-adjusting-x-ray-sampling-rules/

## Some notes

- Though SQS supports X-Ray tracing, it doesn't propagate the trace to a lambda function - Lambda always starts a new trace. There is an issue reported https://github.com/aws/aws-xray-sdk-node/issues/208.
    - Possible workaround: Create a new segment for the lambda to link to the parent (sqs).

- The `in_progress` subsegment is discarded in favor of the completed subsegment.
    - i.e. (in_progress === undefined)
    - Ref: https://docs.aws.amazon.com/xray-sdk-for-nodejs/latest/reference/

- By default, the X-Ray SDK records the first request each second, and five percent of any additional requests.

- Sampling rules
  https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html#xray-console-sampling-options

- Segment doc max 64 kb
  https://docs.aws.amazon.com/xray/latest/devguide/xray-api-segmentdocuments.html
