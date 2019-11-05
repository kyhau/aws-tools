# Serverless Application Model (SAM)
- [awslabs/serverless-application-model](https://github.com/awslabs/serverless-application-model) (SAM)
- [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli) (SAM CLI, formerly known as SAM Local)
- [Examples](https://github.com/awslabs/serverless-application-model/tree/master/examples/2016-10-31)
- Example `sam-app`'s source can be found [here](
  https://aws.amazon.com/blogs/aws/aws-serverless-application-model-sam-command-line-interface-build-test-and-debug-serverless-apps-locally/)

**Note:** 
If docker volume mounting is required, need to use Windows cmd instead of WSL, 
otherwise the mounting will not work probably (without error).

Setup
```
# 1. Install Docker
# 2. Install Python 3.7
# 3. Install aws-sam-cli

pip install aws-sam-cli

sam init --runtime python3.7 --dependency-manager pip --name sam-app --output-dir . --app-template hello-world

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
