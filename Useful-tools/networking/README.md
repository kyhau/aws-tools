# Notes

- [Cheat Sheet on Curl Performance Metrics: how to benchmark server latency with curl](https://speedtestdemon.com/a-guide-to-curls-performance-metrics-how-to-analyze-a-speed-test-result/)
```
time_namelookup: how long DNS lookup took (translating domain name to IP address)
time_connect: how long TCP handshake took (done by both HTTP and HTTPS)
time_appconnect: how long SSL handshake took (only for HTTPS)
time_redirect: how long the redirect took. It is 0 if there is no redirect. Need “-L” flag in curl to redirect.
time_pretransfer: This is essentially an alias for either time_appconnect or time_connect (depending on HTTP or HTTPS). It is only useful as a delineator of when the specific request to the server has begun.
time_starttransfer: This is when the server is ready to deliver bytes. Same as TTFB (Time To First Byte). It includes time_pretransfer, just subtract time_pretransfer from the time_starttransfer to get the amount of time spent in this phase
time_total: The total time of the entire curl call. Calculate time_total - time_starttransfer to get the data transfer (a.k.a. download) time.
```

- [How do I troubleshoot network performance issues between EC2 Linux instances in a VPC and an on-premises host over the internet gateway?](
https://aws.amazon.com/premiumsupport/knowledge-center/network-issue-vpc-onprem-ig/)

Linux
- https://www.binarytides.com/linux-commands-monitor-network/
```
# iftop reports the bandwidth used by individual connections
# it cannot report the process name/id involved in the particular socket connection.
# The n option prevents iftop from resolving ip addresses to hostname, which causes additional network traffic of its own.
sudo iftop -n

sudo iptraf

tcptrack

```

Windows
- [Wireshark](https://www.wireshark.org/)
- [PktMon - Windows 10 built-in Packet Sniffer](https://www.helpmegeek.com/windows-10-packet-sniffer-pktmon-guide/)
