# Install AWS Tools
# https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html

# Recommend that you don't run PowerShell as an administrator with elevated permissions except when required by
# the task at hand. This is because of the potential security risk and is inconsistent with the principle of least
# privilege.

Install-Module -Name AWS.Tools.Installer -Scope CurrentUser -Force

# You can now install the module for each AWS service that you want to use by using the Install-AWSToolsModule cmdlet.

# Install-AWSToolsModule AWS.Tools.EC2,AWS.Tools.S3 -CleanUp