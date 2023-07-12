#!/bin/bash
set -e

date

curl -X POST https://todo_apig_id.execute-api.ap-southeast-2.amazonaws.com/prod/execution
