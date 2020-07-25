## Private and Automatic IP Address Ranges
```
A      10.0.0.0    to 10.255.255.255  (10.0.0.0/8)
B      172.16.0.0  to 172.31.255.255  (172.16.0.0/12)
C      192.168.0.0 to 192.168.255.255 (192.168.0.0/16)
APIPA  169.254.0.0 to 169.254.255.255 (169.254.0.0/16)
```

## RFC 1918 private (non-publicly routable) CIDR blocks / IP addresses
```
- 10.0.0.0/8         10.0.0.0 – 10.255.255.255
- 172.16.0.0/12      172.16.0.0 – 172.31.255.255
- 192.168.0.0/16     192.168.0.0 – 192.168.255.255
```

## AWS: Secondary IPv4 CIDR blocks
```
- Can use: non-RFC 1918, or 100.64.0.0/10 (RFC 6598)
- Cannot use: 198.19.0.0/16
- Primary 10.0.0.0/8 => any other CIDR from 10.0.0.0/8 range
    - If primary CIDR falls within 10.0.0.0/15, cannot add a CIDR block from 10.0.0.0/16
- Primary 172.16.0.0/12 => any other CIDR from 172.16.0.0/12, except 172.31.0.0/16
- Primary 192.168.0.0/16 => any other CIDR from 192.168.0.0/16
- Primary 198.19.0.0/16
- Primary Non-RFC 1918, 100.64.0.0/10
```

## Calculate IP range
```
E.g. 10.0.8.0/21 encompasses addresses from 10.0.8.0 to 10.0.15.255. 
Calculation: (Source)
10.0.8.0 in binary:    00000010 00000000 00001000 00000000
Network mask (21):     11111111 11111111 11111000 00000000 (twenty-one 1s)
                        ----------------------------------- [Logical AND]
FirstIP/NetworkAddr:   00000010 00000000 00001000 00000000 ----> 10.0.8.0

10.0.8.0 in binary:    00000010 00000000 00001000 00000000
Host bit mask (21):    00000000 00000000 00000hhh hhhhhhhh ----> 2^11 = 2048 IPs
                        ----------------------------------- [Force host bits]
LastIP/BroadcastAddr:  00000010 00000000 00001111 11111111 ----> 10.0.15.255
```

# AWS: IPv4, IPv6
```
IPv4: largest, /16 (HostBitMask 11111111 11111111 hhhhhhhh hhhhhhhh → 2^16 = 65536 IPs)
IPV4: smallest,/28 (HostBitMask 11111111 11111111 11111111 1111hhhh → 2^(32-28) = 2^4 = 16 IPs)
IPv6: VPC fixed size of /56
IPv6: Subnet fixed size of /64

MaskBits   IPs-in-range
/28        16
/27        32
/26        64
/25        128
/24        256
/23        512
/22        1024
/21        2048
/20        4096
/19        8192
/18        16384
/17        32768
/16        65536
```