# arki

[![Build Status](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)


## Build

*Linux*

```
virtualenv env
. env/bin/activate
pip install -e .
```

*Windows*
```
virtualenv env
env\Scripts\activate
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
