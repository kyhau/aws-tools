#!/bin/bash

# Set to fail script if any command fails.
set -e

AWS_PROFILE=TODO-1
EMAIL_ADDRESS=TODO-2
SLACK_WEB_HOOK_URL="https://hooks.slack.com/services/XXXXXX/YYYYY/REPLACE_WITH_YOURS"
SLACK_CHANNEL="#securityhub-alerts"

aws cloudformation create-stack --stack-name EnableSecurityHubFindingsEmails \
  --template-body SecurityHubFindingsToEmail.json \
  --parameters ParameterKey=EmailAddress,ParameterValue=${EMAIL_ADDRESS} \
  --profile ${AWS_PROFILE}

aws cloudformation create-stack --stack-name EnableSecurityHubFindingsToSlack \
  --template-body SecurityHubFindingsToSlack.json \
  --parameters ParameterKey=IncomingWebHookURL,ParameterValue="${SLACK_WEB_HOOK_URL}" \
               ParameterKey=SlackChannel,ParameterValue="${SLACK_CHANNEL}" \
  --profile ${AWS_PROFILE}
