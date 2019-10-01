#!/bin/bash
# Set to fail script if any command fails.
set -e

function upload_file {
  aws s3 cp test.json s3://k-shared-cross-account-bucket/account_b.json --acl bucket-owner-full-control --sse aws:kms --profile account-b
}

function download_file {
  # Ref: https://aws.amazon.com/premiumsupport/knowledge-center/decrypt-kms-encrypted-objects-s3/

  ROLE_ARN="arn:aws:iam::111111111111:role/k-shared-cross-account-bucket-readonly-role"

  resp=$(aws sts assume-role --role-arn ${ROLE_ARN} --profile account-c --role-session-name test-s3)
  export AWS_ACCESS_KEY_ID=$(echo "$resp" | jq -r '.Credentials.AccessKeyId')
  export AWS_SECRET_ACCESS_KEY=$(echo "$resp" | jq -r '.Credentials.SecretAccessKey')
  export AWS_SESSION_TOKEN=$(echo "$resp" | jq -r '.Credentials.SessionToken')

  #aws s3 ls s3://k-shared-cross-account-bucket

  #aws kms describe-key --key-id=xxx

  aws s3 cp s3://k-shared-cross-account-bucket/account_b.json test_download.json
  #aws s3api get-object --bucket k-shared-cross-account-bucket --key account_b.json test_download.json
}

#upload_file
download_file