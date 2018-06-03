# arki

[![Build Status](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)


## Some helper functions

1. **`arki`**: Show all tools
1. **`aws_profile`**: Look up AWS profile and access key and print the export commands to console.
1. **`env_store`**: Support saving and retrieving environment variables.
1. **`venv`**: Create `virtualenv` of a Python version on the current platform (Linux or Windows).
1. **`deploy_apig`**: Update a swagger file to AWS and make a stage deployment.

## Build

*Linux*

```
virtualenv -p python3.6 env_36
. env_36/bin/activate
pip install -e .

// OR

python3.6 -m pip install -e . --user

```

*Windows*
```
virtualenv -P C:\Python36\python.exe env_36_win
env_36_win\Scripts\activate
pip install -e .

// OR

C:\Python36\python.exe -m pip install -e .

```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```

## Building Wheels

```
python setup.py bdist_wheel --universal
```
