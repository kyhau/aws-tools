# Install awscli v2
# https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html
# Or
# https://chocolatey.org/packages/awscli
# (availability of latest version is a bit slower)
# choco install awscli

Write-Host "Downloading..."
Invoke-WebRequest `
  https://awscli.amazonaws.com/AWSCLIV2.msi `
  -outfile AWSCLIV2.msi -UseBasicParsing

Write-Host "Installing..."
Start-Process msiexec.exe -Wait -ArgumentList '/I AWSCLIV2.msi /quiet'

Remove-Item AWSCLIV2.msi -Force
Write-Host "Removed AWSCLIV2.msi"

aws --version
