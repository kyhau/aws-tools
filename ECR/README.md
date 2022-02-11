# ECR

| ECR  | Repo/Link |
| :--- | :--- |
| Amazon ECR Docker Credential Helper | [awslabs/amazon-ecr-credential-helper](https://github.com/awslabs/amazon-ecr-credential-helper) |
| Amazon ECR Public Gallery | https://gallery.ecr.aws/ |

```
################################################################################
aws ecr get-login --no-include-email | bash

# OR, for Ubuntu 19.04 Disco Dingo and newer
# use https://github.com/awslabs/amazon-ecr-credential-helper
sudo apt install amazon-ecr-credential-helper


################################################################################
# Image scanning
# https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html

# Configure an existing repository to Scan on Push
aws ecr put-image-scanning-configuration --repository-name name --image-scanning-configuration scanOnPush=true --region ap-southeast-2

# Create a repository configured for scan on push
aws ecr create-repository --repository-name name --image-scanning-configuration scanOnPush=true --region ap-southeast-2

# Start image scan
aws ecr start-image-scan --repository-name name --image-id imageTag=tag_name --region ap-southeast-2

aws ecr start-image-scan --repository-name name --image-id imageDigest=sha256_hash --region ap-southeast-2

# Retrieve image scan findings
aws ecr describe-image-scan-findings --repository-name name --image-id imageTag=tag_name --region ap-southeast-2

aws ecr describe-image-scan-findings --repository-name name --image-id imageDigest=sha256_hash --region ap-southeast-2

```
