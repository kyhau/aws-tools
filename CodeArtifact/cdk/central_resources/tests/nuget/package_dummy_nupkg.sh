#!/bin/bash
set -e

echo "CheckPt: Building ${PKG_NAME}"

cat <<EOT > ${PKG_NAME}.csproj
<Project Sdk="Microsoft.NET.Sdk">
    <PropertyGroup>
        <TargetFramework>netstandard2.0</TargetFramework>
        <PackageId>${PKG_NAME}</PackageId>
        <Version>1.0.0</Version>
        <Authors>kyhau</Authors>
        <Description>Dummy package for CodeArtifact unit tests</Description>
    </PropertyGroup>
</Project>
EOT

dotnet pack ${PKG_NAME}.csproj

rm -rf ${PKG_NAME}.csproj obj/ bin/Debug/netstandard2.0/
