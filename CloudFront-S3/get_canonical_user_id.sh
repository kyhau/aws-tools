#!/bin/bash

# https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html

# The canonical user ID is an identifier for your account.
# The canonical user ID is a long string, such as 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be.

# You can use canonical user IDs in an Amazon S3 bucket policy for cross-account access, which means an AWS account can
# access resources in another AWS account.

# Because this identifier is used by Amazon S3, only this service provides IAM users with access to the canonical user
# ID. You can also view the canonical user ID for your account from the AWS Management Console while signed in as the
# AWS account root user.

# 1. To use the the AWS API or AWS CLI to view the canonical user ID, the IAM user must have permissions to perform the
#    s3:ListAllMyBuckets action.
# 2. To use the Amazon S3 console, the IAM user must have permissions to perform these 2 actions
#    2.1)  s3:ListAllMyBuckets
#    2.2)  s3:GetBucketAcl.

canonical_user_id=$(aws s3api list-buckets --query "Owner.ID" --output text)
echo "$canonical_user_id"
