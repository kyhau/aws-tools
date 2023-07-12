#!/bin/bash

curl -X POST \
  -H 'Content0Type: application/json' \
  my-neptune-database.xxxxxx.us-east-1.neptune.amazonaws.com:8182/loader -d '
  {
    "source": "s3://database-demp/neptune/",
    "format": "csv",
    "iamRoleArn": "arn:aws:iam::xxxxxxxxxxxx:role/NeptuneLoadFromS3",
    "Region": "us-east-1",
    "failOnError": "FALSE",
    "Parallelism": "MEDIUM"
  }'

# Sample output
# {
#     "status" : "200 OK",
#     "payload" : {
#         "loadId": "4169b07e-f123-6222-1d2f-123456789012"
#     }
# }

