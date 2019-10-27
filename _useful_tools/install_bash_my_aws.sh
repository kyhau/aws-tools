#!/bin/bash
# Install https://github.com/bash-my-universe/bash-my-aws

set -e

SRC_HOME="$( cd "$( dirname -- "$0" )" && pwd )/bash-my-aws"

if [[ -d "${SRC_HOME}/bash-my-aws" ]]; then
  echo "$SRC_HOME already exists"
else
  echo "Cloning bash-my-aws to $SRC_HOME"
  git clone https://github.com/bash-my-universe/bash-my-aws.git
fi

# The setup scripts of bash-my-aws assume the default location is ~/.bash-my-aws.
# So, create symlink for setting up the default location required by bash-my-aws.
BASH_MY_AWS_HOME="$HOME/.bash-my-aws"
[[ -e "$BASH_MY_AWS_HOME" ]] || ln -s "${SRC_HOME}/bash-my-aws" "$BASH_MY_AWS_HOME"

export PATH="$PATH:$BASH_MY_AWS_HOME/bin"
. $BASH_MY_AWS_HOME/aliases

# Fix a line in the original file
cp $BASH_MY_AWS_HOME/bash_completion.sh $BASH_MY_AWS_HOME/bash_completion_modified.sh
sed -i -e 's/dirname/dirname --/g' $BASH_MY_AWS_HOME/bash_completion_modified.sh
. $BASH_MY_AWS_HOME/bash_completion_modified.sh
rm $BASH_MY_AWS_HOME/bash_completion_modified.sh
