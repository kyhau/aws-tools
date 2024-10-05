#!/bin/bash

cat <<EOT > Dummy.CodeArtifact.Consumer.csproj
<Project Sdk="Microsoft.NET.Sdk">
    <PropertyGroup>
        <TargetFramework>netstandard2.0</TargetFramework>
        <PackageId>Dummy.CodeArtifact.Consumer</PackageId>
        <Version>1.0.0</Version>
        <Authors>kyhau</Authors>
        <Description>Dummy package for CodeArtifact unit tests</Description>
    </PropertyGroup>
</Project>
EOT
