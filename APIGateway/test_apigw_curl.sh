#!/bin/bash

# https://nelson.cloud/invoking-amazon-api-gateway-with-an-api-key/

curl -X POST https://fake.execute-api.ap-southeast-2.amazonaws.com/prod/create

curl -X POST \
  https://fake.execute-api.ap-southeast-2.amazonaws.com/dev/jobs \
  -H 'Accept: application/json' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'authorizationToken: TODO' \
  -d '{
	"tool_name": "my-tool",
	"tool_version": "latest"
}'


# GET request
curl --header "x-api-key: abc123" https://fake.execute-api.ap-southeast-2.amazonaws.com/.amazonaws.com/prod/create

# POST request with data
curl -d "key1=value1&key2=value2" --header "x-api-key: abc123" -X POST https://fake.execute-api.ap-southeast-2.amazonaws.com/prod/create
