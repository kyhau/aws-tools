# arki

[![Build Status](https://travis-ci.org/kyhau/arki.svg?branch=master)](https://travis-ci.org/kyhau/arki)
[![codecov](https://codecov.io/gh/kyhau/arki/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/arki)


## Some helper functions

1. **`arki`**: Show all tools
1. **`aws_apig_deploy`**: Update a swagger file to AWS and make a stage deployment.
1. **`aws_cognito`**: 
   * Get Cognito tokens.
   * List all users of a User Pool.
1. **`aws_ddb`**: Show all DynamoDB tables, info of a table, scan items, delete items.
1. **`aws_ecs_list_task_definitions`**: Show/filter registered task definitions.
1. **`aws_ecs_register_task_definition`**: Register task definitions.
1. **`aws_lambda_deploy`**: Deploy a lambda function and make a stage deployment.
1. **`aws_lambda_permissions_to_apig`**: Add Lambda Permissions for API Gateway resources.
1. **`aws_profile`**: Look up AWS profile and access key and print the export commands to console.
1. **`dockerc`**: Find and remove non-running containers.
1. **`dockeri`**: Find and remove dangling images.
1. **`env_store`**: Support saving and retrieving environment variables.
1. **`venv`**: Create `virtualenv` of a Python version on the current platform (Linux or Windows).

## Build

*Linux*

```
virtualenv -p python3.6 env_36
. env_36/bin/activate
pip install -e .

// OR

python3.6 -m pip install --user -e .

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
