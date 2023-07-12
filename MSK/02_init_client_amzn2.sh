#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref-1: https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html
# Ref-2: https://docs.aws.amazon.com/msk/latest/developerguide/produce-consume.html

BOOTSTRAP_BROKERS_STR=$(aws kafka get-bootstrap-brokers --query BootstrapBrokerStringTls --cluster-arn ${CLUSTER_ARN})
ZOOKEEPER_CONNECT_STR=$(aws kafka describe-cluster --query ClusterInfo.ZookeeperConnectString --cluster-arn ${CLUSTER_ARN})

cat "export BOOTSTRAP_BROKERS=${BOOTSTRAP_BROKERS_STR}" >> /home/ec2-user/.bash_profile

################################################################################
echo "Installing Kafka to /home/ec2-user/kafka_xxx..."

pushd /home/ec2-user/
sudo yum -y install java-1.8.0
wget https://archive.apache.org/dist/kafka/2.2.1/kafka_2.12-2.2.1.tgz
tar -xzf kafka_2.12-2.2.1.tgz
popd

################################################################################
echo "Setting up client.properties file in /opt/kafka_xxx/bin/..."

pushd /home/ec2-user/kafka_2.12-2.2.1/bin
cat > client.properties << EOF
bootstrap.servers=$BOOTSTRAP_BROKERS_STR
security.protocol=SSL
ssl.truststore.location=/tmp/kafka.client.truststore.jks
EOF
popd

################################################################################
echo "Preparing kafka.client.truststore.jks..."

cp /usr/lib/jvm/jre-1.8.0-openjdk-1.8.0.242.b08-0.amzn2.0.1.x86_64/lib/security/cacerts /tmp/kafka.client.truststore.jks
