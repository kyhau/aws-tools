# Lambda Logs

Determine the amount of over-provisioned memory.
```
filter @type = "REPORT"
| stats max(@memorySize / 1024 / 1024) as provisonedMemoryMB,
    min(@maxMemoryUsed / 1024 / 1024) as smallestMemoryRequestMB,
    avg(@maxMemoryUsed / 1024 / 1024) as avgMemoryUsedMB,
    max(@maxMemoryUsed / 1024 / 1024) as maxMemoryUsedMB,
    provisonedMemoryMB - maxMemoryUsedMB as overProvisionedMB
```

Report latency statistics for 5-minute intervals.
```
filter @type = "REPORT" 
| stats avg(@duration), max(@duration), min(@duration) by bin(5m)
```

Find the most expensive requests
```
filter @type = "REPORT"
| fields @requestId, @billedDuration
| sort by @billedDuration desc
```