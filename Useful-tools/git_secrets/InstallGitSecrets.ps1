# https://github.com/awslabs/git-secrets

pushd C:\Workspaces\github

Write-Host "Cloning git-secrets..."
git clone https://github.com/awslabs/git-secrets

pushd C:\Workspaces\github\git-secrets

Write-Host "Installing git-secrets..."
./install.ps1

popd
popd

Write-Host "Adding a configuration template if you want to add hooks to all repositories you initialize or clone in the future..."
git secrets --register-aws --global

Write-Host "Add hooks to all your local repositories..."
git secrets --install $env:USERPROFILE\.git-templates\git-secrets
git config --global init.templateDir $env:USERPROFILE\.git-templates\git-secrets
