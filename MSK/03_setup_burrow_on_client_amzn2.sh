#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref: https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html#burrow

# Run as ec2-user

# TODOs - update variables
MSK_CLUSTER_NAME="TODO"
BOOTSTRAP_BROKER_HOST_PORT_PAIR_1="TODO"
BOOTSTRAP_BROKER_HOST_PORT_PAIR_2="TODO"
BOOTSTRAP_BROKER_HOST_PORT_PAIR_3="TODO"
ZOOKEEPER_HOST_PORT_PAIR_1="TODO"
ZOOKEEPER_HOST_PORT_PAIR_2="TODO"
ZOOKEEPER_HOST_PORT_PAIR_3="TODO"

################################################################################
echo "Installing Burrow to /home/ec2-user/..."
pushd /home/ec2-user

sudo yum -y install go git
go get github.com/linkedin/Burrow
curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh

pushd /home/ec2-user/go/src/github.com/linkedin/Burrow
/home/ec2-user/go/bin/dep init
/home/ec2-user/go/bin/dep ensure
go install
popd
popd

################################################################################
echo "Preparing /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml..."

mv /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml.old

cat > /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml << EOF
[zookeeper]
servers=[ "${ZOOKEEPER_HOST_PORT_PAIR_1}", "${ZOOKEEPER_HOST_PORT_PAIR_2}", "${ZOOKEEPER_HOST_PORT_PAIR_3}" ]
timeout=6
root-path="/burrow"

[client-profile.test]
client-id="burrow-test"
kafka-version="0.10.0"

[cluster.${MSK_CLUSTER_NAME}]
class-name="kafka"
servers=[ "${BOOTSTRAP_BROKER_HOST_PORT_PAIR_1}", "${BOOTSTRAP_BROKER_HOST_PORT_PAIR_2}", "${BOOTSTRAP_BROKER_HOST_PORT_PAIR_3}" ]
client-profile="test"
topic-refresh=120
offset-refresh=30

[consumer.${MSK_CLUSTER_NAME}]
class-name="kafka"
cluster="${MSK_CLUSTER_NAME}"
servers=[ "${BOOTSTRAP_BROKER_HOST_PORT_PAIR_1}", "${BOOTSTRAP_BROKER_HOST_PORT_PAIR_2}", "${BOOTSTRAP_BROKER_HOST_PORT_PAIR_3}" ]
client-profile="test"
group-blacklist="^(console-consumer-|python-kafka-consumer-|quick-).*$"
group-whitelist=""

[consumer.${MSK_CLUSTER_NAME}_zk]
class-name="kafka_zk"
cluster="${MSK_CLUSTER_NAME}"
servers=[ "${ZOOKEEPER_HOST_PORT_PAIR_1}", "${ZOOKEEPER_HOST_PORT_PAIR_2}", "${ZOOKEEPER_HOST_PORT_PAIR_3}" ]
zookeeper-path="/kafka-cluster"
zookeeper-timeout=30
group-blacklist="^(console-consumer-|python-kafka-consumer-|quick-).*$"
group-whitelist=""
EOF

################################################################################
pushd /home/ec2-user/go/bin
./Burrow --config-dir /home/ec2-user/go/src/github.com/linkedin/Burrow/config
popd

echo "Check for errors: bin/log/burrow.log"
echo "Test your setup: curl -XGET 'HTTP://your-localhost-ip:8000/v3/kafka'"
echo "For all of the supported HTTP requests and links, see https://github.com/linkedin/Burrow/wiki/HTTP-Endpoint"
