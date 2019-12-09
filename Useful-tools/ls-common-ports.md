##  Common TCP and UDP Ports
```
Protocol  Port   Name
ICMP      8      PING
TCP       20     FTP data
TCP       21     FTP control
TCP       22     SSH
TCP       23     Telnet
TCP       25     SMTP (E-mail)
TCP/UDP   53     DNS query, DNS servers
UDP       67/68  DHCP (Dynamic IP address configuration)
TCP       80     HTTP (Web)
TCP       110    POP3 (E-mail)
TCP       119    NNTP (Newsgroups)
TCP       143    IMAP4 (E-mail)
TCP       179    BGP (Border Gateway Protocol)
TCP       389    LDAP (Directory service)
TCP       443    HTTPS (Web SSL)
UDP       500    VPN, IPSec
UDP       1701   L2TP (Virtual Private Networks)
TCP       1723   PPTP (Virtual Private Networks)
TCP       3389   RDP
TCP       4369   (RabbitMQ) Erlang makes use of a Port Mapper Daemon (epmd) for resolution of node names in a cluster.
TCP       5672   RabbitMQ main port
TCP       8080   Apache Tomcat; alternative to port 80, as proxy and caching port.
TCP       15672  RabbitMQ Management Console
TCP       35197  (RabbitMQ) set by inet_dist_listen_min/max Firewalls must permit traffic in this range to pass between clustered nodes
```
