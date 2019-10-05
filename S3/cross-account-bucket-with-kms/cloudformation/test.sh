#!/bin/bash
# Set to fail script if any command fails.
set -e

function finish {
  # Cleanup at the end
  [[ -f sample.json ]] && rm sample.json
  [[ -f test111.tgz ]] && rm test111.tgz
  [[ -f test_download.tgz ]] && rm test_download.tgz
}
trap finish EXIT

# TODO Change these
AWS_PROFILE_UPLOAD="account-b"
AWS_PROFILE_DOWNLOAD="account-c"
BUCKET_NAME="k-shared-cross-account-bucket"
IAM_ASSUME_ROLE="arn:aws:iam::111111111111:role/k-shared-cross-account-bucket-readonly-role"
KMS_ALIAS_ARN="arn:aws:kms:ap-southeast-2:111111111111:alias/${BUCKET_NAME}-kms"
SAMPLE_DATA="{\"hello\":\"world\"}"

test_upload() {
  echo "Checking kms describe-key"
  aws kms describe-key --key-id=${KMS_ALIAS_ARN} --profile ${AWS_PROFILE_UPLOAD} | jq -r '.KeyMetadata.Arn'

  echo "Uploading file to another account"
  echo "Command: aws s3 cp test111.tgz s3://${BUCKET_NAME}/test/test-${AWS_PROFILE_UPLOAD}.tgz --acl bucket-owner-full-control --sse aws:kms --sse-kms-key-id ${KMS_ALIAS_ARN} --profile ${AWS_PROFILE_UPLOAD}"
  aws s3 cp test111.tgz s3://${BUCKET_NAME}/test/test-${AWS_PROFILE_UPLOAD}.tgz --acl bucket-owner-full-control --sse aws:kms --sse-kms-key-id ${KMS_ALIAS_ARN} --profile ${AWS_PROFILE_UPLOAD}

  echo "Checking aws s3 ls"
  aws s3 ls s3://${BUCKET_NAME}/test/ --profile ${AWS_PROFILE_UPLOAD}
}

test_download_succeeded() {
  resp=$(aws sts assume-role --role-arn ${IAM_ASSUME_ROLE} --profile ${AWS_PROFILE_DOWNLOAD} --role-session-name test-s3)
  export AWS_ACCESS_KEY_ID=$(echo "$resp" | jq -r '.Credentials.AccessKeyId')
  export AWS_SECRET_ACCESS_KEY=$(echo "$resp" | jq -r '.Credentials.SecretAccessKey')
  export AWS_SESSION_TOKEN=$(echo "$resp" | jq -r '.Credentials.SessionToken')

  echo "Checking kms describe-key"
  aws kms describe-key --key-id=${KMS_ALIAS_ARN} | jq -r '.KeyMetadata.Arn'

  echo "Checking aws s3 ls"
  aws s3 ls s3://${BUCKET_NAME}/
  aws s3 ls s3://${BUCKET_NAME}/test/

  echo "Downloading a file uploaded by other account"
  aws s3 cp s3://${BUCKET_NAME}/test/test-${AWS_PROFILE_UPLOAD}.tgz test_download.tgz

  echo "Checking the downloaded file"
  tar xvzf test_download.tgz
  [[ "$SAMPLE_DATA" = $(cat sample.json) ]] || (echo "Error: File content not the same." && exit 1)
}

prepare_file() {
  echo "$SAMPLE_DATA" > sample.json
  tar czvf test111.tgz sample.json
  rm sample.json
}

prepare_file
test_upload
test_download_succeeded
