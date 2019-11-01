# Deploy Lambda Layer from SAR (Serverless Application Repository)

Useful tools
- [aws/aws-cdk](https://github.com/aws/aws-cdk)
- [aws/aws-cli](https://github.com/aws/aws-cli)
- [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli)
- [aws-samples/aws-lambda-layer-awscli](https://github.com/aws-samples/aws-lambda-layer-awscli)

Different approaches
1. Deploy from SAR with CDK 
2. Deploy from SAR with CLI from SAR
3. Deploy from SAR with console
4. Create layer with SAM CLI

Ref: https://github.com/aws-samples/aws-lambda-layer-awscli

Examples: https://github.com/aws-samples/aws-lambda-layer-awscli/tree/master/samples

Permission:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "sar-allow-all",
            "Effect": "Allow",
            "Action": "serverlessrepo:*",
            "Resource": "*"
        }
    ]
}
```