# https://www.powershellgallery.com/packages/AWS.Tools.Installer

# Recommend that you don't run PowerShell as an administrator with elevated permissions except when required by
# the task at hand. This is because of the potential security risk and is inconsistent with the principle of least
# privilege.

#Install-Module -Name AWS.Tools.Installer -Scope CurrentUser -Force
Install-Module -Name AWS.Tools.Installer

Install-Module -Name AWSPowerShell

Install-Module -Name AWS.Tools.Common
Install-Module -Name AWS.Tools.SimpleSystemsManagement

# For AWS related packages, see https://www.powershellgallery.com/packages?q=aws
