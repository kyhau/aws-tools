#!/bin/bash
# https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-jar.html

DEFAULT_LOCAL_PKG_ROOT="$HOME/.local/stepfunctionslocal"

DOWNLOAD_FILE="StepFunctionsLocal.tar.gz"
DOWNLOAD_URL="https://s3.amazonaws.com/stepfunctionslocal/StepFunctionsLocal.tar.gz"

if [ ! -d "${DEFAULT_LOCAL_PKG_ROOT}" ]; then
  echo "INFO: Downloading ${DOWNLOAD_FILE}"
  mkdir -p "${DEFAULT_LOCAL_PKG_ROOT}"

  cd ${DEFAULT_LOCAL_PKG_ROOT}
  wget ${DOWNLOAD_URL}
  tar xfz ${DOWNLOAD_FILE}
  rm ${DOWNLOAD_FILE}
  cd -
fi

echo "INFO: Checking version"
cd ${DEFAULT_LOCAL_PKG_ROOT}
echo "StepFunctionsLocal.jar version: $(java -jar StepFunctionsLocal.jar -v)"
nohup java -jar StepFunctionsLocal.jar &
cd -

echo "TODO: RUN: aws stepfunctions --endpoint-url http://localhost:8083 command"
