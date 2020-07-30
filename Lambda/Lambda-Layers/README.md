# Deploy Lambda Layer from SAR (Serverless Application Repository)

Limits
- A function can use up to 5 layers at a time. 
- The total unzipped size of the function and all layers cannot exceed the unzipped deployment package size limit of
  250 MB.
- Layers support resource-based policies for granting layer usage permissions to specific AWS accounts, AWS
  Organizations, or all accounts.
- Layers are extracted to the `/opt` directory in the function execution environment. Each runtime looks for libraries
  in a different location under `/opt`, depending on the language.
- [Environment Variables Available to Lambda Functions](
  https://docs.aws.amazon.com/lambda/latest/dg/lambda-environment-variables.html)

```
aws lambda update-function-configuration --function-name my-function --layers []

aws lambda publish-layer-version \
  --layer-name my-layer \
  --description "My layer" \
  --license-info "MIT" \
  --content S3Bucket=lambda-layers-us-east-2-123456789012,S3Key=layer.zip \
  --compatible-runtimes python3.6 python3.7

aws lambda list-layers --compatible-runtime python3.7

aws lambda get-layer-version --layer-name my-layer --version-number 2

aws lambda delete-layer-version --layer-name my-layer --version-number 1

aws lambda add-layer-version-permission \
  --layer-name xray-sdk-nodejs \
  --statement-id xaccount \
  --action lambda:GetLayerVersion \
  --principal 210987654321 \
  --version-number 1 --output text
```

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