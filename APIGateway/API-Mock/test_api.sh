
API_ID=TODO

date

curl -X POST https://${API_ID}.execute-api.ap-southeast-2.amazonaws.com/v0/mock \
  -H "Content-Type: application/json" --data '{"statusCode": 200}'

curl -X POST https://${API_ID}.execute-api.ap-southeast-2.amazonaws.com/v0/mock \
  -H "Content-Type: application/json" --data '{"statusCode": 500}'
