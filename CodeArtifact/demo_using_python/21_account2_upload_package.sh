#!/bin/bash
set -e

source .env

# Download a wheel
# mkdir dist
# cd dist
# pip wheel click
# pip wheel fire
# cd ..

# pip install -i https://pypi.org/simple twine

REPO=${ACCOUNT_2_TEAM_2_REPO}

aws codeartifact login --tool twine --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
   --repository ${REPO} --profile ${AWS_PROFILE_2}

cat ~/.pypirc

twine upload --repository codeartifact dist/click-8.1.3-py3-none-any.whl
twine upload --repository codeartifact dist/fire-0.5.0-py2.py3-none-any.whl

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${REPO} --format pypi --package click --profile ${AWS_PROFILE_2}

aws codeartifact list-package-versions --domain ${DOMAIN} --domain-owner ${ACCOUNT_2_ID} \
  --repository ${REPO} --format pypi --package fire --profile ${AWS_PROFILE_2}

rm ~/.pypirc
