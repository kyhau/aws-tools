#!/bin/bash
# Set to fail script if any command fails.
set -e

# https://www.gorillastack.com/news/important-aws-cloudtrail-security-events-tracking/

declare -a SECURITY_EVENTS=(
  #"ConsoleLogin"

  #"StopLogging"

  #"CreateNetworkAclEntry"
  #"CreateRoute"

  "AuthorizeSecurityGroupEgress"
  "AuthorizeSecurityGroupIngress"
  "RevokeSecurityGroupEgress"
  "RevokeSecurityGroupIngress"

  #"AuthorizeDBSecurityGroupIngress"
  #"RevokeDBSecurityGroupIngress"
  #"CreateDBSecurityGroup"
  #"DeleteDBSecurityGroup"
)

for event_to_check in "${SECURITY_EVENTS[@]}"
  do
    aws cloudtrail lookup-events \
      --lookup-attributes AttributeKey=EventName,AttributeValue=${event_to_check} \
      --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,resource:(Resources[0].ResourceName)}' \
      --output table --region ap-southeast-2
done
