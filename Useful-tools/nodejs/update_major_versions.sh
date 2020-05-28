
################################################################################
# To update to a new major version all the packages, install the npm-check-updates package globally:

sudo npm install -g npm-check-updates
ncu -u       # Upgrade all the version hints in the package.json file, to dependencies and devDependencies
npm update
npm install
