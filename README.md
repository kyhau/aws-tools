# python-repo-template

[![Build Status](https://travis-ci.org/kyhau/python-repo-template.svg?branch=master)](https://travis-ci.org/kyhau/python-repo-template)
[![codecov](https://codecov.io/gh/kyhau/python-repo-template/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/python-repo-template)

This is a template repository that you can use to quickly create a python application that can be built, tested, and released as an internal python module.

## Setting up a new repository from this template
**Create a directory and pull all the files in this template into it**

```bash
mkdir new_repo_name
cd new_repo_name
git init
git pull https://github.com/kyhau/python-repo-template
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

If the library is py2/py3 compatible then remove the `bdist_wheel` lines in tox.ini and use this bdist_wheel line in test.sh/test.bat instead

```
python setup.py bdist_wheel --universal
```
