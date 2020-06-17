#!/bin/bash

# When you request a package from the CodeArtifact repository that's not already present
# in the repository, the package can be fetched from the external connection. 
# This makes it possible to consume open-source dependencies used by your application. 
# Ref: https://aws.amazon.com/blogs/devops/integrating-aws-codeartifact-package-mgmt-flow/

aws codeartifact associate-external-connection \
  --domain "my-org" --domain-owner "account-id" \
  --repository "my-external-repo" --external-connection public:npmjs

