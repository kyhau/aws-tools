#!/bin/bash
set -e

echo "CheckPt: Building ${PKG_NAME}"

mkdir -p app/

cat <<EOT > app/__init__.py
VERSION = "1.0.0"
EOT

cat <<EOT > app/test.py
from . import VERSION
def print_version():
    print(VERSION)
EOT

cat <<EOT > setup-app.py
from setuptools import setup
setup(
    name='${PKG_NAME}',
    version='1.0.0',
    packages=['.app'],
)
EOT

pip3 install wheel setuptools

python3 setup-app.py bdist_wheel --universal --bdist-dir ~/temp/bdistwheel

rm -rf app/ setup-app.py *.egg-info build dist/app dist/*.egg-info dist/*.dist-info
