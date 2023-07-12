
API_NAME=K-Mock-Simple-API

API_URL=$(aws cloudformation describe-stacks --stack-name ${API_NAME} --query "Stacks[0].Outputs[0].OutputValue" --output text)
echo "API URL: ${API_URL}"

date
echo "Response:"
curl -X POST ${API_URL}
echo

# curl -X POST https://${API_ID}.execute-api.ap-southeast-2.amazonaws.com/v0/mock
