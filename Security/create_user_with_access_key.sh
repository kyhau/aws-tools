#!/bin/bash

username="TODO"
policy_arn=


aws iam create-user --user-name "$username"

aws iam create-access-key --user-name "$username"

aws attach-user-policy --username "$username" --policy-arn "$policy_arn"
