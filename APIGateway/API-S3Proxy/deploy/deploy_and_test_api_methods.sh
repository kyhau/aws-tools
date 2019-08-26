#!/bin/bash
# Set to fail script if any command fails.
set -e

echo "################################################################################"

echo "TEST_STEP: Create virtual env"
virtualenv -p python3 env
. env/bin/activate

echo "TEST_STEP: Install dependencies"
python -m pip install -r requirements.txt --upgrade

echo "TEST_STEP: Re-import API Swagger file to AWS"
python deployment_helper.py

echo "TEST_STEP: Test API methods"
python -m pytest -s tests/test_invoke_methods.py --junit-xml junit-methods.xml

# TODO Enable the following for regenerating the API.md
#echo "TEST_STEP: Generate API.md documentation"
#swagger2markdown -i ../../api/DataServiceAPI_swagger.json -o ../../API.md

# Leave virtual environment
deactivate
