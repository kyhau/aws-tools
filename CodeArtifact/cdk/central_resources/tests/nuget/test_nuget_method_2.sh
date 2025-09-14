#!/bin/bash
set -e
# See https://docs.aws.amazon.com/codeartifact/latest/ug/nuget-cli.html
#
# Method 2: Configure nuget or dotnet with the `codeartifact login` command
# This test script uses/requires dotnet.

echo "######################################################################"
echo "CheckPt: Install tools"

pip3 install -i https://pypi.org/simple -U awscli

echo "######################################################################"
echo "CheckPt: Configure the nuget or dotnet CLI"

# Backup NuGet.Config if exists
if [ -f ~/.nuget/NuGet/NuGet.Config ]; then
   cp ~/.nuget/NuGet/NuGet.Config ~/.nuget/NuGet/NuGet.Config.bkup
fi

aws codeartifact login --tool dotnet --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
   --repository ${TARGET_REPO_NAME} --region ${AWS_REGION}

echo "######################################################################"
echo "CheckPt: Package a dummy nupkg"

export PKG_NAME="Dummy.CodeArtifact.Test$(date +%Y%m%d%H%M%S)"
PKG=bin/Debug/${PKG_NAME}.1.0.0.nupkg
[[ -f ./package_dummy_nupkg.sh ]] || { echo "Error: package_dummy_nupkg.sh not found"; exit 1; }
./package_dummy_nupkg.sh

echo "######################################################################"
echo "CheckPt: Test publish"

dotnet nuget push ${PKG} --source ${DOMAIN_NAME}/${TARGET_REPO_NAME}

echo "######################################################################"
echo "CheckPt: Test list-package-versions"

aws codeartifact list-package-versions --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} --format nuget --package ${PKG_NAME} --region ${AWS_REGION}

echo "######################################################################"
echo "CheckPt: Test install ${PKG_NAME}"

[[ -f ./create_dummy_consumer_csproj.sh ]] || { echo "Error: create_dummy_consumer_csproj.sh not found"; exit 1; }
./create_dummy_consumer_csproj.sh

dotnet add package ${PKG_NAME} --version "1.0.0"

echo "######################################################################"
echo "CheckPt: Test delete package"

aws codeartifact delete-package --domain ${DOMAIN_NAME} --domain-owner ${DOMAIN_OWNER} \
  --repository ${TARGET_REPO_NAME} --format nuget --package ${PKG_NAME} --region ${AWS_REGION}

echo "######################################################################"
echo "CheckPt: Cleanup"

# Restore NuGet.Config if exists
if [ -f ~/.nuget/NuGet/NuGet.Config.bkup ]; then
   mv ~/.nuget/NuGet/NuGet.Config.bkup ~/.nuget/NuGet/NuGet.Config
fi

rm -rf *.csproj bin/ obj/
