# Example

See also https://aws.amazon.com/blogs/aws/aws-serverless-application-model-sam-command-line-interface-build-test-and-debug-serverless-apps-locally/

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


