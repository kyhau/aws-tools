#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref-1: https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html
# Ref-2: https://docs.aws.amazon.com/msk/latest/developerguide/produce-consume.html

# TODOs - update variables
CLUSTER_ARN="TODO"
KAFKA_TOPIC="AWSKafkaTutorialTopic"

ZOOKEEPER_CONNECT_STR=$(aws kafka describe-cluster --query ClusterInfo.ZookeeperConnectString --cluster-arn ${CLUSTER_ARN})

################################################################################
echo "Installing Kafka..."

pushd /opt
sudo yum -y install java-1.8.0
wget https://archive.apache.org/dist/kafka/2.2.1/kafka_2.12-2.2.1.tgz
tar -xzf kafka_2.12-2.2.1.tgz

pushd kafka_2.12-2.2.1
bin/kafka-topics.sh --create --replication-factor 3 --partitions 1 --topic ${KAFKA_TOPIC} --zookeeper ${ZOOKEEPER_CONNECT_STR}

# If the command succeeds, you see the following message: Created topic $KAFKA_TOPIC.

################################################################################
echo "Setting up client.properties file in kafka_xxx/bin/..."

CLIENT_PROPERTIES_FILE="/opt/kafka_2.12-2.2.1/bin/client.properties"

cat > ${CLIENT_PROPERTIES_FILE} << EOF
security.protocol=SSL
ssl.truststore.location=/tmp/kafka.client.truststore.jks
EOF

cp /usr/lib/jvm/jre-1.8.0-openjdk-1.8.0.242.b08-0.amzn2.0.1.x86_64/lib/security/cacerts /tmp/kafka.client.truststore.jks

popd
popd
