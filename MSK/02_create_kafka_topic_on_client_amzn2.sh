#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref-1: https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html
# Ref-2: https://docs.aws.amazon.com/msk/latest/developerguide/produce-consume.html

# TODOs - update variables
CLUSTER_ARN="TODO"
KAFKA_TOPIC="AWSKafkaTutorialTopic"

BOOTSTRAP_BROKER_STR=$(aws kafka get-bootstrap-brokers --query BootstrapBrokerStringTls --cluster-arn ${CLUSTER_ARN})
ZOOKEEPER_CONNECT_STR=$(aws kafka describe-cluster --query ClusterInfo.ZookeeperConnectString --cluster-arn ${CLUSTER_ARN})


pushd /home/ec2-user/kafka_2.12-2.2.1/bin
./kafka-topics.sh --create --replication-factor 3 --partitions 1 --topic ${KAFKA_TOPIC} --zookeeper ${ZOOKEEPER_CONNECT_STR}

# If the command succeeds, you see the following message: Created topic $KAFKA_TOPIC.

echo "To list topics: ./kafka-topics.sh --list --zookeeper ${ZOOKEEPER_CONNECT_STR}"
echo "To delete this topic: ./kafka-topics.sh --delete --topic ${KAFKA_TOPIC} --zookeeper ${ZOOKEEPER_CONNECT_STR}"

popd