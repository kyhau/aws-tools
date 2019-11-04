# Serverless Application Model (SAM)
- [awslabs/aws-sam-cli](https://github.com/awslabs/aws-sam-cli), formerly known as SAM Local.
- [awslabs/serverless-application-model](https://github.com/awslabs/serverless-application-model) (SAM)
- https://aws.amazon.com/serverless/serverlessrepo/resources/
- [Examples](https://github.com/awslabs/serverless-application-model/tree/master/examples/2016-10-31)

1. Install Docker
2. Install Python 3.7


```
pip install aws-sam-cli

sam init --runtime python3.7 --dependency-manager pip --name sam-app --output-dir . --app-template hello-world

cd sam-app/

mkdir build
pip install -r hello_world/requirements.txt -t build/
cp hello_world/*.py build/

sam local start-api

sam local start-lambda

```
