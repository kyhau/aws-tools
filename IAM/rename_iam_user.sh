#!/bin/bash
# Console does not support renaming an IAM User
aws iam update-user --user-name devpos --new-user-name devops
