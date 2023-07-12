#!/bin/bash
set -e

aws iam create-user --user-name github-k-ci-deploy

aws iam put-user-policy --user-name github-k-ci-deploy --policy-name github-k-ci-deploy --policy-document file://default_iam_policy.json

aws iam create-access-key --user-name github-k-ci-deploy
