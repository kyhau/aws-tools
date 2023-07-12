#!/bin/bash
# Set to fail script if any command fails.
set -e

# Ref: https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html#open-monitoring

# Run as ec2-user

# TODOs - update variables
PROMETHEUS_VERSION="2.18.0-rc.1"
MSK_CLUSTER_NAME="TODO"
BOOTSTRAP_BROKER_HOST_PORT_PAIR_1="TODO"
BOOTSTRAP_BROKER_HOST_PORT_PAIR_2="TODO"
BOOTSTRAP_BROKER_HOST_PORT_PAIR_3="TODO"
ZOOKEEPER_HOST_PORT_PAIR_1="TODO"
ZOOKEEPER_HOST_PORT_PAIR_2="TODO"
ZOOKEEPER_HOST_PORT_PAIR_3="TODO"

################################################################################
# Download latest version from https://prometheus.io/download/#prometheus or https://github.com/prometheus/prometheus/releases/download/
echo "Installing prometheus into /opt/..."
wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz
tar xfz prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz -C /opt
rm prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz

CONFIG_FILE="/opt/prometheus-${PROMETHEUS_VERSION}.linux-amd64/prometheus.yml"
TARGET_FILE="/opt/prometheus-${PROMETHEUS_VERSION}.linux-amd64/targets.json"

################################################################################
echo "Creating ${CONFIG_FILE}..."
cat > ${CONFIG_FILE} << EOF
# file: prometheus.yml
# my global config
global:
  scrape_interval:     10s

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'
    static_configs:
    # 9090 is the prometheus server port
    - targets: ['localhost:9090']
  - job_name: 'broker'
    file_sd_configs:
    - files:
      - 'targets.json'
EOF

################################################################################
echo "Creating ${TARGET_FILE}..."
cat > ${TARGET_FILE} << EOF
[
  {
    "labels": {
      "job": "jmx"
    },
    "targets": [
      "broker_dns_1:11001",
      "broker_dns_2:11001",
      .
      .
      .
      "broker_dns_N:11001"
    ]
  },
  {
    "labels": {
      "job": "node"
    },
    "targets": [
      "broker_dns_1:11002",
      "broker_dns_2:11002",
      .
      .
      .
      "broker_dns_N:11002"
    ]
  }
]
EOF


./opt/prometheus-${PROMETHEUS_VERSION}.linux-amd64/prometheus

echo "To access the Prometheus web UI, open a browser that can access your Amazon EC2 instance, and go to"
echo "Prometheus-Instance-Public-IP:9090, where Prometheus-Instance-Public-IP is the public IP address you"
echo "got in the previous step."
