# Install AWS Session Manager Plugin on Windows for AWS CLI
# https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html

Write-Host "Downloading SessionManagerPluginSetup.exe from S3..."

Invoke-WebRequest `
  https://s3.amazonaws.com/session-manager-downloads/plugin/latest/windows/SessionManagerPluginSetup.exe `
  -outfile SessionManagerPluginSetup.exe -UseBasicParsing

Write-Host "Installing SessionManagerPluginSetup.exe..."

Start-Process SessionManagerPluginSetup.exe -ArgumentList '/passive' -PassThru | Wait-Process

Remove-Item SessionManagerPluginSetup.exe

Write-Host "Removed SessionManagerPluginSetup.exe"

Param([string]$BinDirectory = "C:\Program Files\Amazon\SessionManagerPlugin\bin")
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
if ($currentPath -notlike "*$BinDirectory*")
{
    Write-Host "Adding $BinDirectory to path."
    $newPath = $currentPath
    if (-not ($newPath.EndsWith(";")))
    {
        $newPath = $newPath + ";"
    }
    $newPath = $newPath + $BinDirectory
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
}
else
{
    Write-Host "$BinDirectory already in Path."
}

session-manager-plugin --version
