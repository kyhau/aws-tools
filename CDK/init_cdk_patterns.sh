#!/bin/bash
# https://github.com/cdk-patterns/serverless
set -e

# Browse the "Grouped Alphabetically" patterns list below or run
# npx cdkp list

PATTERN_NAME="TODO"

npx cdkp init ${PATTERN_NAME} --lang=python
cd ${PATTERN_NAME}

# create a virtual env and install your dependencies
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt

# test everything is working by outputting the cloudformation
npx cdk synth
# requires you to be using cloud9 or have ran aws configure to setup your local credentials
npx cdk deploy

