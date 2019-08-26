#!/bin/bash

function dynamo() {
  cd /etc/dynamodblocal
  nohup sudo java -Djava.library.path=./DynamoDBLocal_lib/ -jar DynamoDBLocal.jar -sharedDb -port 4569 &
}

dynamo

aws dynamodb list-tables --endpoint-url http://localhost:4569
