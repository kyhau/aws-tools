#!/bin/bash

# Simple script just to generate the initial template, which
# 1. creates IAM Users
# 2. assigns IAM User to the same existing IAM Group(s)

OUTPUT_FILE=tmp_users.template

declare -a USERS=(
  "Firstname Lastname"
)

# Add Header
cat > ${OUTPUT_FILE} << EOF
AWSTemplateFormatVersion: '2010-09-09'
Description: >-
  Create IAM Users and assign users to the corresponding IAM Groups.

Resources:
EOF

# Add Resources
for user in "${USERS[@]}"
do
  echo "Adding $user"
  name_no_space=${user//[ ]/}
  user_name=$(echo "print('${user//[ ]/.}'.lower())" | python)

cat >> ${OUTPUT_FILE} << EOF
  ${name_no_space}IamUser:
    Type: AWS::IAM::User
    Properties:
      UserName: ${user_name}
      Groups:
        - ConsoleUsers
        - Developers

EOF
done
