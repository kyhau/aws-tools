#!/bin/bash
set -e

assign_permissions() {
  USER_NAME="$1"
  GROUP_NAME=${USER_NAME}

  aws iam create-user --user-name ${USER_NAME}
  aws iam create-access-key --user-name ${USER_NAME}

  aws iam create-group --group-name ${GROUP_NAME}

  # aws iam attach-group-policy --group-name ${GROUP_NAME} --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
  # aws iam attach-group-policy --group-name ${GROUP_NAME} --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
  aws iam put-group-policy --group-name ${GROUP_NAME} --policy-name ${GROUP_NAME} --policy-document file://policies/create-github-oidc-role-policy.json

  aws iam add-user-to-group --group-name ${GROUP_NAME} --user-name ${USER_NAME}
}

assign_permissions github-oidc-setup
