# Deploy Lambda Layer from SAR (Serverless Application Repository)

1. Deploy with CDK from SAR 
2. Deploy with CLI from SAR
3. Deploy with console from SAR
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