#!/bin/bash
# Set to fail script if any command fails.
set -e

aws ssm get-inventory --filters '[{"Key":"Custom:DatabaseProcesses.Name","Values":["sqlservr"],"Type":"Equal"}]'

aws ssm get-inventory --filters '[{"Key":"AWS:Service.DisplayName","Values":["Windows Firewall"],"Type":"Equal"},{"Key":"AWS:Service.Status","Values":["Stopped"],"Type":"Equal"},{"Key":"AWS:Tag.Key","Values":["env"],"Type":"Equal"},{"Key":"AWS:Tag.Value","Values":["Prod"],"Type":"Equal"}]'
