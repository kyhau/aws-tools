#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref: https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html#burrow

# Run as ec2-user

# TODOs - update variables
CLUSTER_ARN="TODO"
MSK-cluster-name="TODO"
bootstrap-broker-host-port-pair-1="TODO"
bootstrap-broker-host-port-pair-2="TODO"
bootstrap-broker-host-port-pair-3="TODO"
ZooKeeper-host-port-pair-1="TODO"
ZooKeeper-host-port-pair-2="TODO"
ZooKeeper-host-port-pair-3="TODO"

################################################################################
echo "Installing Burrow to /home/ec2-user/..."
pushd /home/ec2-user

sudo yum install go
go get github.com/linkedin/Burrow
curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh

pushd /home/ec2-user/go/src/github.com/linkedin/Burrow
/home/ec2-user/go/bin/dep ensure
go install
popd
popd

################################################################################
echo "Preparing /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml..."

mv /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml.old

cat > /home/ec2-user/go/src/github.com/linkedin/Burrow/config/burrow.toml << EOF
[zookeeper]
servers=[ "${ZooKeeper-host-port-pair-1}", "${ZooKeeper-host-port-pair-2}", "${ZooKeeper-host-port-pair-3}" ]
timeout=6
root-path="/burrow"

[client-profile.test]
client-id="burrow-test"
kafka-version="0.10.0"

[cluster.${MSK-cluster-name}]
class-name="kafka"
servers=[ "${bootstrap-broker-host-port-pair-1}", "${bootstrap-broker-host-port-pair-2}", "${bootstrap-broker-host-port-pair-3}" ]
client-profile="test"
topic-refresh=120
offset-refresh=30

[consumer.${MSK-cluster-name}]
class-name="kafka"
cluster="${MSK-cluster-name}"
servers=[ "${bootstrap-broker-host-port-pair-1}", "${bootstrap-broker-host-port-pair-2}", "${bootstrap-broker-host-port-pair-3}" ]
client-profile="test"
group-blacklist="^(console-consumer-|python-kafka-consumer-|quick-).*$"
group-whitelist=""

[consumer.${MSK-cluster-name}_zk]
class-name="kafka_zk"
cluster="${MSK-cluster-name}"
servers=[ "${ZooKeeper-host-port-pair-1}", "${ZooKeeper-host-port-pair-2}", "${ZooKeeper-host-port-pair-3}" ]
zookeeper-path="/kafka-cluster"
zookeeper-timeout=30
group-blacklist="^(console-consumer-|python-kafka-consumer-|quick-).*$"
group-whitelist=""
EOF

################################################################################
pushd /home/ec2-user/go/bin
./Burrow --config-dir /home/ec2-user/go/src/github.com/linkedin/Burrow/config
popd

# Check for errors
# cat bin/log/burrow.log

# Test your setup:
# curl -XGET 'HTTP://your-localhost-ip:8000/v3/kafka'

# For all of the supported HTTP requests and links, see https://github.com/linkedin/Burrow/wiki/HTTP-Endpoint.
