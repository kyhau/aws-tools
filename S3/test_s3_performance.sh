#!/bin/bash

# A simple script for comparing some S3 command's on object with/without encryption enabled.

TEST_BUCKET=filestore-dev            # A bucket that has no default bucket encryption setting
UPLOAD_FILE=sse_test1/input.zip      # An input.zip from nbngreenfield
DOWNLOAD_FILE=sse_test1/input2.zip


run_s3_test() {
  local option=${1}

  ts=$(date +%s%N)  # nanoseconds

  for i in {1..20}
  do
    # Upload
    aws s3 cp ${UPLOAD_FILE}  s3://${TEST_BUCKET}/${UPLOAD_FILE} --quiet  ${option}

    # Download
    aws s3 cp s3://${TEST_BUCKET}/${UPLOAD_FILE} ${DOWNLOAD_FILE} --quiet

    # Delete
    aws s3 rm s3://${TEST_BUCKET}/${UPLOAD_FILE} --quiet
  done

  tt=$((($(date +%s%N) - $ts)/20/1000000))
  echo "Average time taken: $tt milliseconds"
}

echo "Test S3 commands without encryption"
run_s3_test

echo "Test S3 commands with default encryption"
run_s3_test "--sse AES256"