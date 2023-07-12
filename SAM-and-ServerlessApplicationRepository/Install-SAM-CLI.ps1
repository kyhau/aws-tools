# Install SAM CLI
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-windows.html

Write-Host "Downloading..."

Invoke-WebRequest -Uri https://github.com/awslabs/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi -OutFile AWS_SAM_CLI_64_PY3.msi -UseBasicParsing

Write-Host "Installing..."

Start-Process msiexec.exe -Wait -ArgumentList '/I AWS_SAM_CLI_64_PY3.msi /quiet'

Remove-Item AWS_SAM_CLI_64_PY3.msi -Force

Write-Host "Removed AWS_SAM_CLI_64_PY3.msi"

sam --version
