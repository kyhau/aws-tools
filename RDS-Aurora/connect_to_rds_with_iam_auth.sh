#!/bin/bash
# Set to fail script if any command fails.
set -e

# See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.AWSCLI.html

RDSHOST="rdsmysql.cdgmuqiadpid.ap-southeast2.rds.amazonaws.com"
UNAME=jane_doe
RDS_CA=/etc/ca-certificates/rds-combined-ca-bundle.pem

[[ -e "$RDS_CA" ]] || wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem -O ${RDS_CA}

TOKEN="$(aws rds generate-db-auth-token --hostname $RDSHOST --port 3306 --region ap-southeast2 --username ${UNAME} )"

mysql --host=$RDSHOST --port=3306 --ssl-ca=${RDS_CA} --enable-cleartext-plugin --user=${UNAME} --password=$TOKEN
