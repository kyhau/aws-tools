# arki_common

[![githubactions](https://github.com/kyhau/arki/workflows/Build-Test/badge.svg)](https://github.com/kyhau/arki/actions)
[![travisci](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)

## Build

```
# Create virtual env and install the required packages

virtualenv env -p python3.8
. env/bin/activate
pip install -r requirements.txt
```

## Run Unit Tests with Tox

```
pip install -r requirements-build.txt
tox -r
```

## Build Wheel

```
python setup.py bdist_wheel --universal
```
