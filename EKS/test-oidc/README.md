
```
VPC_ID="vpc-xxx"
SUBNETS="subnet-xxx,subnet-xxx"
ACCOUNT="123456789012"

aws cloudformation deploy --stack-name k-test-oicd --template-file basic-eks.yaml --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides VpcId=${VPC_ID} ClusterSubnets="${SUBNETS}" \
  --tags Billing="test-oicd" --profile test-oidc

# Cluster has
# 1. OpenID Connect provider UR
# https://oidc.eks.ap-southeast-2.amazonaws.com/id/ABC123ABC123ABC123ABC123ABC123AB

# 2. API server endpoint
# https://ABC123ABC123ABC123ABC123ABC123AB.gr7.ap-southeast-2.eks.amazonaws.com


echo "curl --silent --location https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz | tar xz -C ." > tmp_run.sh
chmod +x tmp_run.sh
./tmp_run.sh
ls -al

eksctl utils associate-iam-oidc-provider --cluster=development-k-test-oicd --approve --region=ap-southeast-2 --profile test-oidc

# associate-iam-oidc-provider requires
# - iam:CreateOpenIDConnectProvider
# - iam:GetOpenIDConnectProvider
# - iam:TagOpenIDConnectProvider

# created
# oidc.eks.ap-southeast-2.amazonaws.com/id/ABC123ABC123ABC123ABC123ABC123AB

# cluster:
# https://ABC123ABC123ABC123ABC123ABC123AB.gr7.ap-southeast-2.eks.amazonaws.com
# https://oidc.eks.ap-southeast-2.amazonaws.com/id/ABC123ABC123ABC123ABC123ABC123AB

# ----------------------------

aws iam list-open-id-connect-providers

aws iam get-open-id-connect-provider --open-id-connect-provider-arn arn:aws:iam::${ACCOUNT}:oidc-provider/oidc.eks.ap-southeast-2.amazonaws.com/id/ABC123ABC123ABC123ABC123ABC123AB

aws iam delete-open-id-connect-provider --open-id-connect-provider-arn arn:aws:iam::${ACCOUNT}:oidc-provider/oidc.eks.ap-southeast-2.amazonaws.com/id/ABC123ABC123ABC123ABC123ABC123AB


# ----------------------------
Create OpenID Provider

aws iam create-open-id-connect-provider --generate-cli-skeleton > create-open-id-connect-provider.json --profile test-oidc

aws iam create-open-id-connect-provider --cli-input-json file://create-open-id-connect-provider.json --profile test-oidc

```
