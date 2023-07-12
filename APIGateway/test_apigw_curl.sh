#!/bin/bash

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

curl -X POST https://fake.execute-api.ap-southeast-2.amazonaws.com/prod/execution
