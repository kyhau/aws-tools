# AWS CLI Tips and Tricks

- Standard Input/Output Redirection with "-"
    - By using the `-` character which represents standard input/output (STDIN/STDOUT), you can read or write file content directly from or to S3 without creating local copies.
    - E.g. `aws s3 cp s3://bucket-name/object-key -`
    - [Source](https://hackingthe.cloud/aws/general-knowledge/aws_cli_tips_and_tricks/)

- Modifying the CloudTrail Log User-Agent with `AWS_EXECUTION_ENV`
    - When making API calls to AWS, a User-Agent header is included in each request, containing details about the client making the request. Although it’s not possible to fully customize this header, you can append information to it, which can be useful for tracking API calls in CloudTrail logs.
    - One way to modify the User-Agent is by setting the `AWS_EXECUTION_ENV` environment variable, used by AWS SDKs to identify the execution environment. You can leverage this variable to append custom information to the User-Agent header, making API tracking more informative.
    - [Source](https://hackingthe.cloud/aws/general-knowledge/aws_cli_tips_and_tricks/)

- Model
    - You can add additional "model" to aws cli with https://docs.aws.amazon.com/cli/latest/reference/configure/add-model.html.
    - The model will be added to `~/.aws/model/`.
    - If you need to use the same model with boto3, you will need to have the model available in `botocore/data/`.
    - See also
        - https://github.com/aws/aws-cli/issues/2790
        - https://github.com/boto/botocore/blob/cac78632cabddbc7b64f63d99d419fe16917e09b/botocore/loaders.py#L33
        - https://stackoverflow.com/questions/63512015/boto3-load-custom-models
    - E.g. https://boto3.amazonaws.com/v1/documentation/api/1.9.56/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_provisioned_capacity
