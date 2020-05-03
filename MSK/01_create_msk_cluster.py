import boto3

CLUSTER_NAME="AWSKafkaTutorialCluster"
CLUSTER_SG="sg-TODO"
CLUSTER_SUBNET_1="subnet-TODO"
CLUSTER_SUBNET_2="subnet-TODO"
CLUSTER_SUBNET_3="subnet-TODO"


client = boto3.client("kafka")

response = client.create_cluster(
    BrokerNodeGroupInfo={
        "BrokerAZDistribution": "DEFAULT",
        "ClientSubnets": [
            CLUSTER_SUBNET_1,
            CLUSTER_SUBNET_2,
            CLUSTER_SUBNET_3,
        ],
        "InstanceType": "kafka.t3.small",
        "SecurityGroups": [
            CLUSTER_SG,
        ]
    },
    ClusterName=CLUSTER_NAME,
    EncryptionInfo={
        "EncryptionInTransit": {
            "ClientBroker": "TLS",
            "InCluster": True
        }
    },
    EnhancedMonitoring="PER_TOPIC_PER_BROKER", # DEFAULT | PER_BROKER | PER_TOPIC_PER_BROKER
    OpenMonitoring={
        "Prometheus": {
            "JmxExporter": {
                "EnabledInBroker": True
            },
            "NodeExporter": {
                "EnabledInBroker": True
            }
        }
    },
    KafkaVersion="2.2.1",
    NumberOfBrokerNodes=3
)

print(response)