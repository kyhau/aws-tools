# Install saml2aws
# https://github.com/Versent/saml2aws/releases

Param([string]$version = "2.26.1")

Write-Host "Downloading ..."

Invoke-WebRequest `
  https://github.com/Versent/saml2aws/releases/download/v$($version)/saml2aws_$($version)_windows_amd64.tar.gz `
  -outfile saml2aws.tar.gz -UseBasicParsing

Write-Host "Unziping ..."

Start-Process "C:\Program Files\WinRAR\WinRAR.exe" -ArgumentList 'x saml2aws.tar.gz' -PassThru | Wait-Process

Move-Item -Path saml2aws.exe -Destination C:\ProgramData\chocolatey\bin\saml2aws.exe -Force

Remove-Item saml2aws.tar.gz -Force

Write-Host "Removed saml2aws.tar.gz"

saml2aws --version