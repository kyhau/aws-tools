#!/bin/bash
# Ref: https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html

#aws ssm start-session --target instance-id

# TODOs - update variables
CLUSTER_ARN="TODO"
KAFKA_TOPIC="AWSKafkaTutorialTopic"

BOOTSTRAP_BROKER_STR=$(aws kafka get-bootstrap-brokers --query BootstrapBrokerStringTls --cluster-arn ${CLUSTER_ARN})

./kafka-console-producer.sh --producer.config client.properties --topic ${KAFKA_TOPIC} --broker-list ${BOOTSTRAP_BROKER_STR}

./kafka-console-consumer.sh --consumer.config client.properties --topic ${KAFKA_TOPIC} --from-beginning --bootstrap-server ${BOOTSTRAP_BROKER_STR}
