# Networking

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blog Posts](#useful-articles-and-blog-posts)
- [Other Tools](#other-tools)
- [kyhau/workspace/useful-tools/networking](https://github.com/kyhau/workspace/tree/main/useful-tools/networking)


---
## Useful Libs and Tools

| Description | Repo/Link |
| :--- | :--- |
| AWS CIDR Finder | [aws-samples/aws-cidr-finder](https://github.com/aws-samples/aws-cidr-finder) |
| AWS IP Ranges | [aws-samples/awsipranges](https://github.com/aws-samples/awsipranges) |
| AWS Network Firewall CFN templates | [aws-samples/aws-networkfirewall-cfn-templates](https://github.com/aws-samples/aws-networkfirewall-cfn-templates) |
| Non Routable Secondary CIDR Patterns | [aws-samples/non-routable-secondary-vpc-cidr-patterns](https://github.com/aws-samples/non-routable-secondary-vpc-cidr-patterns) |
| [Serverless Transit Network Orchestrator](https://aws.amazon.com/solutions/serverless-transit-network-orchestrator/) | [awslabs/serverless-transit-network-orchestrator](https://github.com/awslabs/serverless-transit-network-orchestrator) |
| TGW (Transit Gateway) Migrator Tool | [TGW Migrator Tool](https://aws.amazon.com/blogs/networking-and-content-delivery/migrate-from-transit-vpc-to-aws-transit-gateway/) |
| TGW Route Limits Monitoring | [aws-samples/how-to-monitor-tgw-route-limits-using-serverless-architecture](https://github.com/aws-samples/how-to-monitor-tgw-route-limits-using-serverless-architecture) |
| TGW to solve overlapping CIDRs | [aws-samples/aws-transit-gateway-overlapping-cidrs](https://github.com/aws-samples/aws-transit-gateway-overlapping-cidrs) |
| Visual Fn.Cidr tool | [kyhau/visual-subnet-tools](https://kyhau.github.io/visual-subnet-tools/fncidr.html) |
| Visual subnet calculator | [kyhau/visual-subnet-tools](vhttps://kyhau.github.io/visual-subnet-tools/subnets.html) |


---
## Useful Articles and Blog Posts

- [How do I troubleshoot network performance issues between EC2 Linux instances in a VPC and an on-premises host over the internet gateway?](
https://aws.amazon.com/premiumsupport/knowledge-center/network-issue-vpc-onprem-ig/)

- [Introducing Prefix Lists in AWS Network Firewall Stateful Rule Groups](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-prefix-lists-in-aws-network-firewall-stateful-rule-groups/)

---
## Other Tools


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
