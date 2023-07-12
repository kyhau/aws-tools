#!/bin/bash

#aws ssm start-session --target instance-id

source /home/ec2-user/.bash_profile

KAFKA_TOPIC="AWSKafkaTutorialTopic"
KAFKA_GROUP="consumer-2"

./bin/kafka-topics.sh --bootstrap-server $KAFKA_BROKERS --command-config config/client.properties --list

while true; do ./bin/kafka-consumer-perf-test.sh --threads 60 --timeout 5000 --consumer.config config/client.properties --topic ${KAFKA_TOPIC} --messages 250 --group ${KAFKA_GROUP} --broker-list ${KAFKA_BROKERS}; done > consumer.log &


# ./bin/kafka-consumer-groups.sh --command-config config/client.properties --bootstrap-server ${KAFKA_BROKERS} --describe --group ${KAFKA_GROUP}

# cat consumer.log  | grep 2020 | awk -F, '{print $5}' | paste -sd+ | bc
