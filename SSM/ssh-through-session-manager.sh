#!/bin/bash
# Set to fail script if any command fails.
set -e

INSTANCE_ID="TODO"


CONFIG_FILE="~/.ssh/config"
cat > ${CONFIG_FILE} << EOF
host i-* mi-*
ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
EOF
chmod 600 ${CONFIG_FILE}

ssh -i MyKeyPair.pem ec2-user@${INSTANCE_ID}
