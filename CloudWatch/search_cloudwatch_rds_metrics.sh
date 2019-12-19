#!/bin/bash
# https://www.cloudconformity.com/knowledge-base/aws/RDS/idle-instance.html
# https://stackoverflow.com/questions/50839596/aws-rds-how-to-get-hold-of-the-current-activity-number-of-connections


# 14 days
period=1209600

func() {
  aws cloudwatch get-metric-statistics --namespace AWS/RDS \
    --metric-name DatabaseConnections \
    --start-time 2019-12-06T00:00:00Z \
    --end-time 2019-12-20T00:00:00Z \
    --period $period \
    --statistics "Maximum" \
    --dimensions Name=DBInstanceIdentifier,Value=${1} \
    --output text
}

db_list=$(aws rds describe-db-instances --query 'DBInstances[*].DBInstanceIdentifier' --output text)

for db in $db_list; do
  echo $db
  func $db
done
