#!/bin/bash

# https://docs.aws.amazon.com/cli/latest/reference/logs/filter-log-events.html

# start_time (milliseconds)
start_time=`python -c '
from datetime import datetime
print(int((datetime(2018, 11, 26) - datetime(1970, 1, 1)).total_seconds() * 1000))'
`

aws logs filter-log-events --log-group-name API-Gateway-Execution-Logs_fakeouufg3/v1 --filter-pattern "tool_name" --start-time $start_time
