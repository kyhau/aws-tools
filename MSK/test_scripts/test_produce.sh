#!/bin/bash
# Ref: https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html

#aws ssm start-session --target instance-id

# TODOs - update variables
CLUSTER_ARN="TODO"
KAFKA_TOPIC="AWSKafkaTutorialTopic"

source /home/ec2-user/.bash_profile
# OR
# BOOTSTRAP_BROKER_STR=$(aws kafka get-bootstrap-brokers --query BootstrapBrokerStringTls --cluster-arn ${CLUSTER_ARN})

./bin/kafka-topics.sh --bootstrap-server $KAFKA_BROKERS --command-config config/client.properties --list

./bin/kafka-topics.sh --create --topic ${KAFKA_TOPIC} --partitions 60 --replication-factor 3 --bootstrap-server ${KAFKA_BROKERS} --command-config config/client.properties


run_test(){
  MSG_PER_SEC=$1
  MSG_SIZE=$2
  NUM_RECORDS=$3
  echo "CheckPt ${MSG_PER_SEC} ${MSG_SIZE} ${NUM_RECORDS}"
  echo "CheckPt ${MSG_PER_SEC} ${MSG_SIZE} ${NUM_RECORDS}" >> producer.log
  ./bin/kafka-producer-perf-test.sh --producer.config config/client.properties --topic ${KAFKA_TOPIC} --record-size ${MSG_SIZE} --num-records ${NUM_RECORDS} --throughput ${MSG_PER_SEC} >> producer.log
}

#run_test 11 80000 1000