#!/bin/bash
# InstallAWS API Gateway Developer Portal
# https://github.com/awslabs/aws-api-gateway-developer-portal
set -e

YOUR_LAMBDA_ARTIFACTS_BUCKET_NAME="k-artifacts"
CUSTOM_PREFIX="k-default"
STACK_NAME="API-Gateway-Developer-Portal"

[ -d "aws-api-gateway-developer-portal" ] || git clone git@github.com:awslabs/aws-api-gateway-developer-portal.git

pushd aws-api-gateway-developer-portal

echo "CheckPt: Uploading lambda artifacts to bucket..."

sam package --template-file ./cloudformation/template.yaml \
    --output-template-file ./cloudformation/packaged.yaml \
    --s3-bucket ${YOUR_LAMBDA_ARTIFACTS_BUCKET_NAME}

echo "CheckPt: Deploying stack..."

sam deploy --template-file ./cloudformation/packaged.yaml \
    --stack-name ${STACK_NAME} \
    --s3-bucket ${YOUR_LAMBDA_ARTIFACTS_BUCKET_NAME} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
    DevPortalSiteS3BucketName="${CUSTOM_PREFIX}-dev-portal-static-assets" \
    ArtifactsS3BucketName="${CUSTOM_PREFIX}-dev-portal-artifacts" \
    CognitoDomainNameOrPrefix="${CUSTOM_PREFIX}"

#echo "Setup a custom domain for your Developer Portal"

#sam deploy --template-file ./cloudformation/packaged.yaml \
#    --stack-name ${STACK_NAME} \
#    --s3-bucket ${YOUR_LAMBDA_ARTIFACTS_BUCKET_NAME} \
#    --capabilities CAPABILITY_NAMED_IAM \
#    --parameter-overrides \
#    DevPortalSiteS3BucketName="${CUSTOM_PREFIX}-dev-portal-static-assets" \
#    ArtifactsS3BucketName="${CUSTOM_PREFIX}-dev-portal-artifacts" \
#    CustomDomainName="my.acm.managed.domain.name.com" \
#    CustomDomainNameAcmCertArn="arn:aws:acm:us-east-1:111111111111:certificate/12345678-1234-1234-1234-1234567890ab" \
#    UseRoute53Nameservers="false"


popd

echo "CheckPt: Removing the cloned repo..."
#rm -rf aws-api-gateway-developer-portal

echo "CheckPt: Done"
