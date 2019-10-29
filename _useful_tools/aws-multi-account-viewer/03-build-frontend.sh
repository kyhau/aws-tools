#!/bin/bash
# Set to fail script if any command fails.
set -e

# TODO - fill in the TODOs
REPO_HOME=TODO-1/aws-multi-account-viewer
userPoolId=TODO
userPoolWebClientId=TODO
apidId=TODO

sed -i 's/ap-southeast-2_UsrPlId/${userPoolId}/g' "$REPO_HOME/Front-End/src/App.js"
sed -i 's/123usrPoolWebClientID456/${userPoolWebClientId}/g' "$REPO_HOME/Front-End/src/App.js"
sed -i 's/abcd1234/${apidId}/g' "$REPO_HOME/Front-End/src/App.js"

pushd ${REPO_HOME}/Front-End/
yarn
yarn start
popd
