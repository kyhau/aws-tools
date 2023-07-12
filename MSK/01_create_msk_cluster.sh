#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref: https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html

# TODOs - update variables
CLUSTER_NAME="AWSKafkaTutorialCluster"
CLUSTER_SG="sg-TODO"
CLUSTER_SUBNET_1="subnet-TODO"
CLUSTER_SUBNET_2="subnet-TODO"
CLUSTER_SUBNET_3="subnet-TODO"

cat > clusterinfo.json << EOF
{
  "BrokerNodeGroupInfo": {
    "BrokerAZDistribution": "DEFAULT",
    "InstanceType": "kafka.t3.small",
    "ClientSubnets": [
      "${CLUSTER_SUBNET_1}",
      "${CLUSTER_SUBNET_2}",
      "${CLUSTER_SUBNET_3}"
    ],
    "SecurityGroups": [
      "${CLUSTER_SG}"
    ]
  },
  "ClusterName": "${CLUSTER_NAME}",
  "EncryptionInfo": {
    "EncryptionInTransit": {
      "InCluster": true,
      "ClientBroker": "TLS"
    }
  },
  "EnhancedMonitoring": "PER_TOPIC_PER_BROKER",
  "OpenMonitoring": {
    "Prometheus": {
      "JmxExporter": {
        "EnabledInBroker": true
      },
      "NodeExporter": {
        "EnabledInBroker": true
      }
    }
  },
  "KafkaVersion": "2.2.1",
  "NumberOfBrokerNodes": 3
}
EOF

aws kafka create-cluster --cli-input-json file://clusterinfo.json

echo "Wait for few minutes, then try:"
echo "aws kafka describe-cluster --cluster-arn ClusterArn"

echo "To delete the cluster, run:"
echo "aws kafka delete-cluster --cluster-arn ClusterArn"
