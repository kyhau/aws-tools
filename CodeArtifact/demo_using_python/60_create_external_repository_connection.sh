#!/bin/bash
set -e
# Ref: https://aws.amazon.com/blogs/devops/integrating-aws-codeartifact-package-mgmt-flow/

source .env

# You can only add one external connection to a CodeArtifact repository.
# https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html

aws codeartifact create-repository --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_EXTERNAL_PYPI} --description "External connection pypi" --profile ${AWS_PROFILE_1}

# CodeArtifact enables you to set external repository connections and replicate them within CodeArtifact.
# An external connection reduces the downstream dependency on the remote external repository.
# When you request a package from the CodeArtifact repository that’s not already present in the repository,
# the package can be fetched from the external connection.
# This makes it possible to consume open-source dependencies used by your application.

aws codeartifact associate-external-connection --domain ${DOMAIN} --domain-owner ${ACCOUNT_1_ID} \
  --repository ${ACCOUNT_1_EXTERNAL_PYPI} --external-connection public:pypi --profile ${AWS_PROFILE_1}


# public:npmjs - for the npm public repository.
# public:pypi - for the Python Package Index.
# public:maven-central - for Maven Central.
# public:maven-googleandroid - for the Google Android repository.
# public:maven-gradleplugins - for the Gradle plugins repository.
# public:maven-commonsware - for the CommonsWare Android repository.

# Using an external connection reduces interruption in your development process for package external dependencies,
# an example is if a package is removed from a public repository, you will still have a copy of the package stored
# in CodeArtifact.

# You should have a one-to-one mapping with external repositories, and rather than have multiple CodeArtifact
# repositories pointing to the same public repository.

# Each asset that CodeArtifact imports into your repository from a public repository is billed as a single request,
# and each connection must reconcile and fetch the package before the response is returned.

# By having a one-to-one mapping, you can increase cache hits, reducing time to download an application dependency
# from CodeArtifact, and reduce the number of external package resolution requests.
