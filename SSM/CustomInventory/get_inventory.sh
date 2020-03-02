#!/bin/bash
# Set to fail script if any command fails.
set -e

aws ssm get-inventory --filters '[{"Key":"Custom:DatabaseProcesses.Name","Values":["sqlservr"],"Type":"Equal"}]' --profile infra-prd-admin