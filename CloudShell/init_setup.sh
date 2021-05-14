#!/bin/bash
# Set up the compute environment the first time in a region.

cat > .bashrc << EOF

# Additional settings
alias ll='ls -al'
alias aws-sts-get-caller-identity='aws sts get-caller-identity'

EOF

source .bashrc

sudo yum install nano -y

