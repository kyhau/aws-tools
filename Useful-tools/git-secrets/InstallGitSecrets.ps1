# https://github.com/awslabs/git-secrets

Param([string]$LocalRepoDirectory = "C:\Workspaces\github\git-secrets")

Write-Host "Checking to see if $LocalRepoDirectory exists..."
if (-not (Test-Path $LocalRepoDirectory))
{
    Write-Host "Cloning git-secrets..."
    git clone https://github.com/awslabs/git-secrets $LocalRepoDirectory
}
else
{
    Write-Host "$LocalRepoDirectory exists"
}
Push-Location $LocalRepoDirectory

Write-Host "Installing git-secrets..."
./install.ps1

Pop-Location

Write-Host "Checking if $LocalRepoDirectory already exists in System Path..."
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
if ($currentPath -notlike "*$LocalRepoDirectory*")
{
    Write-Host "Adding $LocalRepoDirectory to path."
    $newPath = $currentPath
    if (-not ($newPath.EndsWith(";")))
    {
        $newPath = $newPath + ";"
    }
    $newPath = $newPath + $LocalRepoDirectory
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
}
else
{
    Write-Host "$LocalRepoDirectory already in Path."
}

Write-Host "Adding a configuration template if you want to add hooks to all repositories you initialize or clone in the future..."
git secrets --register-aws --global

Write-Host "Add hooks to all your local repositories..."
git secrets --install $env:USERPROFILE\.git-templates\git-secrets
git config --global init.templateDir $env:USERPROFILE\.git-templates\git-secrets
