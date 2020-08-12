#!/bin/bash
set -eo pipefail

function test_topic {

echo "################################################################################"
echo "Testing $1"

cat > event.json << EOF
{"body": {"topic": "$1"}}
EOF

aws lambda invoke --function-name SmileFunction \
  --cli-binary-format raw-in-base64-out \
  --payload file://event.json response.json

cat response.json
sleep 2

}

test_topic "devopsreaction"
test_topic "dilbert"
test_topic "fortunecow"
test_topic "xkcd"

rm event.json
rm response.json