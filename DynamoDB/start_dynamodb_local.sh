#!/bin/bash
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

DEFAULT_LOCAL_PKG_ROOT="$HOME/.local/dynamodblocal"

DOWNLOAD_FILE="dynamodb_local_latest.tar.gz"
DOWNLOAD_URL="https://s3.ap-southeast-1.amazonaws.com/dynamodb-local-singapore/dynamodb_local_latest.tar.gz"

if [ ! -d "${DEFAULT_LOCAL_PKG_ROOT}" ]; then
  echo "INFO: Downloading ${DOWNLOAD_FILE}"
  mkdir -p ${DEFAULT_LOCAL_PKG_ROOT}

  cd ${DEFAULT_LOCAL_PKG_ROOT}
  wget ${DOWNLOAD_URL}
  tar xfz ${DOWNLOAD_FILE}
  rm ${DOWNLOAD_FILE}
  cd -
fi

cd ${DEFAULT_LOCAL_PKG_ROOT}
nohup sudo java -Djava.library.path=./DynamoDBLocal_lib/ -jar DynamoDBLocal.jar -sharedDb -port 4569 &
cd -

aws dynamodb list-tables --endpoint-url http://localhost:4569
