# Install saml2aws
# https://github.com/Versent/saml2aws/releases

Write-Host "Downloading ..."

Invoke-WebRequest `
  https://github.com/Versent/saml2aws/releases/download/v2.22.1/saml2aws_2.22.1_windows_amd64.tar.gz `
  -outfile saml2aws.tar.gz -UseBasicParsing

Write-Host "Unziping ..."

Start-Process "C:\Program Files\WinRAR\WinRAR.exe" -ArgumentList 'x saml2aws.tar.gz' -PassThru | Wait-Process

Move-Item -Path saml2aws.exe -Destination C:\ProgramData\chocolatey\bin\saml2aws.exe -Force

Remove-Item saml2aws.tar.gz -Force

Write-Host "Removed saml2aws.tar.gz"

saml2aws --version