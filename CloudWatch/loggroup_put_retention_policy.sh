#!/bin/bash
set -e

declare -r retention="1"

# Updating Log Groups that do not have "Expire Events After" (i.e. Retention) specified
for L in $(aws logs describe-log-groups \
  --query 'logGroups[?!not_null(retentionInDays)] | [].logGroupName' \
  --output text)
do
  echo "Updating $L"
  aws logs put-retention-policy --log-group-name "${L}" \
    --retention-in-days ${retention}
done
