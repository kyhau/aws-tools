
################################################################################
# Uninstall
npm uninstall -g angular/cli
npm uninstall angular-cli --save-dev
rm -rf node_modules dist
npm cache clean --force
npm audit fix
