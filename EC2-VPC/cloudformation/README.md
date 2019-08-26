# Templates for creating EC2 and VPC aws resources

1. `BaseInfrastructure-Linux-SaltMaster.template`
    - Create VPC (at Sydney)
    - Create public Subnet, RouteTable, Route, InternetGateway, NetworkAcl 
    - Create SecurityGroup for EC2 (Salt-master)
        - Special inbound rules
            - tcp 4505 0.0.0.0/0  salt-master publish-port
            - tcp 4506 0.0.0.0/0  salt-master ret-port
    - Create SecurityGroup for VPN

1. `BaseInfrastructure-LinuxEC2Instances.template`
    - Create VPC
    - Create public Subnet, RouteTable, Route, InternetGateway, NetworkAcl 
    - Create SecurityGroup for EC2 instances (Linux)
    - Create SecurityGroup for VPN

1. `BaseInfrastructure-WinEC2Instances.template`
    - Create VPC
    - Create public Subnet, RouteTable, Route, InternetGateway, NetworkAcl 
    - Create SecurityGroup for EC2 instances (Windows)
    - Create SecurityGroup for VPN

1. `EC2-SaltMaster.template`
    - Create an EC2 instance from an AMI with the specified `EC2HostName`.
    - If `SaltVersion` is specified, Salt-Master and Salt-Minion will be installed with initial configurations.
    - Create an Elastic IP, attached to the EC2 instance.

1. `EC2-Basic-Linux.template`
    - Create an EC2 instance from an AMI with the specified `EC2HostName`.
    - If `SaltMasterHost` and `SaltVersion` are specified, Salt-Minion will be installed
      and the the salt-master host will be specified in `/etc/salt/minion`.    
    - Create an Elastic IP, attached to the EC2 instance.

1. `EC2-Basic-Windows.template`
    - Create an EC2 instance from an AMI with the specified `EC2HostName`.
    - Create an Elastic IP, attached to the EC2 instance.

1. `EC2-and-SecurityGroup-support-NFS-Rabbitmq.template`
    - Create an EC2 instance with an additional volume and Security Group supporting NFS and Rabbitmq ports.
    - Create an additional EBS and attached to the EC2 instance.
    - Create SecurityGroup for EC2 instances (Linux)
        - Special inbound rules
            - tcp 2049 NFS-port
            - tcp 5672 Rabbitmq-port 
    - Create an Elastic IP, attached to the EC2 instance.

