#!/bin/bash
set -e
# https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-remove

aws_path=$(which aws)

if [[ "$aws_path" = "/usr/local/bin/aws" ]]; then
  sudo rm /usr/local/bin/aws
  sudo rm /usr/local/bin/aws2_completer
  sudo rm -rf /usr/local/aws-cli
else
  echo "Not installed in default location. Please delete manually."
fi

