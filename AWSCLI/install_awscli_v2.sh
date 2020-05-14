#!/bin/bash
set -e
# See https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install
# See https://aws.amazon.com/blogs/developer/aws-cli-v2-now-supports-aws-single-sign-on/

pushd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip

if [[ -e "/usr/local/bin/aws" ]]; then
  sudo ./aws/install --update
else
  sudo ./aws/install
fi
# By default, the files are all installed to /usr/local/aws, and a symlink is created in /usr/local/bin.
# The command includes sudo to grant write permissions to those folders. You can install without sudo if
# you specify folders that you already have write permissions to.
# See also
#   --install-dir or -i
#   --bin-dir or -b

/usr/local/bin/aws --version

rm -rf awscliv2.zip aws
popd
