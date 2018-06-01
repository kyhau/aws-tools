# arki

[![Build Status](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)

This is a template repository that you can use to quickly create a python application that can be built, tested, and released as an internal python module.

## Setting up a new repository from this template
**Create a directory and pull all the files in this template into it**

```bash
mkdir new_repo_name
cd new_repo_name
git init
git pull https://github.com/kyhau/arki
```

## Build

*Linux*

```bash
virtualenv env
. env/bin/activate
pip install -e .
```

*Windows*
```bash
virtualenv env
env\Scripts\activate
pip install -e .
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
# run the python tests
tox -r
```

## Building Wheels

```
python setup.py bdist_wheel --universal
```
