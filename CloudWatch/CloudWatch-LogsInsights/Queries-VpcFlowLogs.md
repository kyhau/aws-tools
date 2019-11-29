# VPC Flow Logs

IP addresses using UDP as a data transfer protocol. 
See also https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
```
filter protocol=17 | stats count(*) by srcAddr
```

IP addresses (top 20) with highest number of rejected requests.
```
filter action="REJECT"
| stats count(*) as numRejections by srcAddr
| sort numRejections desc | limit 20
```

Avg, min and max byte transfers by source and destination IP addresses.
```
stats avg(bytes), min(bytes), max(bytes) by srcAddr, dstAddr
```

Top 15 byte transfers by source and destination IP addresses.
```
stats sum(bytes) as bytesTransferred by srcAddr, dstAddr
| sort bytesTransferred desc | limit 15
```

Top 15 byte transfers for a given host.
```
filter srcAddr LIKE "192.0.2."
| stats sum(bytes) as bytesTransferred by dstAddr
| sort bytesTransferred desc | limit 15
```

Top 15 packet transfers across hosts.
```
stats sum(packets) as packetsTransferred by srcAddr, dstAddr
| sort packetsTransferred  desc | limit 15
```

IP addresses where flow records were skipped during the capture window.
```
filter logStatus="SKIPDATA"
| stats count(*) by bin(1h) as t
| sort t
```