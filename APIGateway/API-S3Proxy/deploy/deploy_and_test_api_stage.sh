#!/bin/bash
# Set to fail script if any command fails.
set -e

echo "################################################################################"

if [ $# -ne 1 ]; then
  echo "Usage: $0 [stage-name]"
  exit 1
fi
STAGE_NAME=$1

echo "TEST_STEP: Create virtual env"
virtualenv -p python3 env
. env/bin/activate

echo "TEST_STEP: Install dependencies"
python -m pip install -r requirements.txt --upgrade

echo "TEST_STEP: Create or update a deployment stage"
python deployment_helper.py --deploy ${STAGE_NAME}

echo "TEST_STEP: Run tests on the deployed stage"
python -m pytest -s tests/test_api.py --junit-xml junit-api.xml

# Leave virtual environment
deactivate
