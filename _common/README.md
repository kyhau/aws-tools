# helper

[![githubactions](https://github.com/kyhau/aws-tools/workflows/Build-Test/badge.svg)](https://github.com/kyhau/aws-tools/actions)
[![travisci](https://travis-ci.org/kyhau/aws-tools.svg?branch=master)](https://travis-ci.org/kyhau/aws-tools)
[![codecov](https://codecov.io/gh/kyhau/aws-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/aws-tools)

## Build

```bash
# Create virtual env and install the required packages
# Supports Python 3.10, 3.11, and 3.12

virtualenv env -p python3.12
. env/bin/activate
pip install -r requirements.txt
```

## Run Unit Tests with Tox

```
pip install -r requirements-build.txt
tox -r
```

## Build Wheel

```bash
python setup.py bdist_wheel
```
