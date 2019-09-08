#!/bin/bash
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

DEFAULT_LOCAL_DDB_ROOT="$HOME/dynamodblocal"

if [ ! -d "${DEFAULT_LOCAL_DDB_ROOT}" ]; then
  echo "Downloading dynamodb_local_latest.tar.gz..."
  mkdir -p "${DEFAULT_LOCAL_DDB_ROOT}"
  pushd "${DEFAULT_LOCAL_DDB_ROOT}"
  wget https://s3-ap-southeast-1.amazonaws.com/dynamodb-local-singapore/dynamodb_local_latest.tar.gz
  tar xfz dynamodb_local_latest.tar.gz
  rm dynamodb_local_latest.tar.gz
  popd
fi

if [ -d "${DEFAULT_LOCAL_DDB_ROOT}" ]; then
  pushd "${DEFAULT_LOCAL_DDB_ROOT}"
  nohup sudo java -Djava.library.path=./DynamoDBLocal_lib/ -jar DynamoDBLocal.jar -sharedDb -port 4569 &
  popd
else
  echo "Unable to start DynamoDBLocal.jar" && exit 1
fi

aws dynamodb list-tables --endpoint-url http://localhost:4569
