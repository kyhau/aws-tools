
API_NAME=K-Mock-Status-API

API_URL=$(aws cloudformation describe-stacks --stack-name ${API_NAME} --query "Stacks[0].Outputs[0].OutputValue" --output text)
echo "API URL: ${API_URL}"

date
echo "Response:"
curl -X POST ${API_URL} -H "Content-Type: application/json" --data '{"statusCode": 200}'
echo

date
echo "Response:"
curl -X POST ${API_URL} -H "Content-Type: application/json" --data '{"statusCode": 500}'
echo

# https://${API_ID}.execute-api.ap-southeast-2.amazonaws.com/v0/mock
