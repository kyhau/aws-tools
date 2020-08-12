#!/bin/bash
set -eo pipefail

rm -rf package

cd functions
pip install --target ../package/python -r requirements.txt
