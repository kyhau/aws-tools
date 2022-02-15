# Resources for building serverless applications and pipelines


- My example with sam-beta-cdk: https://github.com/kyhau/slack-command-app-cdk



| Description | Repo/Link |
| :--- | :--- |
| AWS Serverless Application Model (SAM) | [awslabs/serverless-application-model](https://github.com/awslabs/serverless-application-model) |
| AWS Serverless Application Model (SAM) CLI | [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli)
| AWS Serverless Application Model (SAM) Examples | [awslabs/serverless-application-model/examples/](https://github.com/awslabs/serverless-application-model/tree/master/examples/2016-10-31) |
| AWS Serverless Application Repository | [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/) |
| Cookiecutter SAM for Python Lambda functions | [aws-samples/cookiecutter-aws-sam-python](https://github.com/aws-samples/cookiecutter-aws-sam-python) |



- https://aws.amazon.com/serverless/serverlessrepo/resources/

-  **Pipeline**
   - [awslabs/aws-sam-codepipeline-cd](https://github.com/awslabs/aws-sam-codepipeline-cd)
   - https://aws.amazon.com/blogs/compute/improving-the-getting-started-experience-with-aws-lambda/

- AWS Serverless Application Repository (SAR)
   - [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/)
   - [DEVELOPER GUIDE: AWS Serverless Application Repository](
        https://docs.aws.amazon.com/serverlessrepo/latest/devguide/what-is-serverlessrepo.html)

---

## Notes on known sam-beta-cdk issues

1. KeyError when running sam-beta-cdk ...
   ```
   KeyError: '/home/.../lambda'
   Failed to execute script __main__
   ```
   - Known bug: https://github.com/aws/aws-sam-cli/issues/2849
   - Workaround:
      - Add `"@aws-cdk/core:newStyleStackSynthesis": false` into cdk.json
      - Add an empty requirements.txt to lambda/ (folder containing the Lambda functions).

---

## SAM

- [awslabs/serverless-application-model](https://github.com/awslabs/serverless-application-model) (SAM)
- [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli) (SAM CLI, formerly known as SAM Local)
- [Examples](https://github.com/awslabs/serverless-application-model/tree/master/examples/2016-10-31)
- [Cookiecutter SAM for Python Lambda functions](https://github.com/aws-samples/cookiecutter-aws-sam-python) |


**Note:**
If docker volume mounting is required, need to use Windows cmd instead of WSL,
otherwise the mounting will not work probably (without error).

Setup
```
# 1. Install Docker
# 2. Install Python 3.8
# 3. Install aws-sam-cli

pip install aws-sam-cli

sam init --runtime python3.8 --dependency-manager pip --name sam-app --output-dir . --app-template hello-world

cd sam-app/
```

Build and test locally
```
# To build on your workstation, run this command in folder containing
# SAM template. Built artifacts will be written to .aws-sam/build folder
sam build

sam local invoke --event events\event.json

sam local start-api
curl http://localhost:3000/

sam local start-lambda

# Run unit tests
pip install pytest pytest-mock --user
python -m pytest tests/ -v
```

Deploy
```
aws s3 mb s3://BUCKET_NAME

sam package --output-template-file packaged.yaml --s3-bucket BUCKET_NAME

sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-app \
    --capabilities CAPABILITY_IAM

sam-app$ aws cloudformation describe-stacks \
    --stack-name sam-app \
    --query 'Stacks[].Outputs[?OutputKey==`HelloWorldApi`]' \
    --output table

sam logs -n HelloWorldFunction --stack-name sam-app --tail
```

Fetch, tail, and filter Lambda function logs
```
sam logs -n HelloWorldFunction --stack-name sam-app --tail
```

Cleanup
```
aws cloudformation delete-stack --stack-name sam-app
aws s3 rb s3://BUCKET_NAME
```
