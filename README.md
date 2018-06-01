# arki

[![Build Status](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)


## Some helper functions

1. **`a_env`**: Support saving and retrieving environment variables.
1. **`a_profile`**: Look up AWS profile and access key and print the export commands to console.


## Build

*Linux*

```
virtualenv -p python3.6 env_36
. env_36/bin/activate
pip install -e .
```

*Windows*
```
virtualenv -P C:\Python36\python.exe env_36_win
env_36_win\Scripts\activate
pip install -e .
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
