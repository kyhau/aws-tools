# EC2

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [CloudWatch Agent](../CloudWatch/README.md)
- [On-Demand Instance vCPUs limits](#on-demand-instance-vcpus-limits)
- [Quick Start Linux utilities](#quick-start-linux-utilities)
- [Amazon Linux 2 amazon-linux-extras repository](#amazon-linux-2-amazon-linux-extras-repository)


---
## Useful Libs and Tools

- [ec2-net-utils](https://github.com/aws/ec2-net-utils) - AWS EC2 ENI Utilities (ec2-net-utils)
- [AWS Instance Scheduler](https://aws.amazon.com/solutions/instance-scheduler/)


---
## On-Demand Instance vCPUs limits

There is a limit on the number of running On-Demand Instances per AWS account per Region. On-Demand Instance limits are managed in terms of the **number of vCPUs** that your running On-Demand Instances are using, regardless of the instance type. [Each limit specifies the vCPU limit for one or more instance families](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html#ec2-on-demand-instances-limits).

- To see the current vCPUs limits of your account from AWS EC2 console
    - Enter "vcpu" in the "Find limits" to shortlist the limits
- To find out the current running instances (of the same instance family of the EC2 type you want to check), go to EC2 console.
- Calculate how many vCPUs you nee
    - You can use the [vCPU limits calculator](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances.html#vcpu-limits-calculator) to see what will be the numbers for adding instances of certain type.
- Request a limit increase
    - Even though EC2 automatically increases your On-Demand Instance limits based on your usage, you can request a limit increase if necessary. See Request a limit increase for details.

See also https://aws.amazon.com/premiumsupport/knowledge-center/ec2-on-demand-instance-vcpu-increase/.


---
## Quick Start Linux utilities

- Quick Start Linux utilities provide a simple and easy way to automate the installation of AWS CloudFormation tools across common Linux distributions.
- Note that AWS conveniently provides a Linux distribution called Amazon Linux, which has this utility built-in.
- Git repo: https://github.com/aws-quickstart/quickstart-linux-utilities
- For details, see https://aws.amazon.com/blogs/infrastructure-and-automation/introduction-to-quickstart-linux-utilities/

```
UserData: !Base64
    Fn::Sub:
    - |
        #!/bin/bash -x
        until git clone https://github.com/aws-quickstart/quickstart-linux-utilities.git; do echo "Retrying"; done
        cd /quickstart-linux-utilities
        source quickstart-cfn-tools.source
        qs_update-os || qs_err
        qs_bootstrap_pip || qs_err
        qs_aws-cfn-bootstrap || qs_err
```


---
## Amazon Linux 2 amazon-linux-extras repository

### How do I install a software package from the Extras Library on an EC2 instance running Amazon Linux 2?

For the steps please see https://aws.amazon.com/premiumsupport/knowledge-center/ec2-install-extras-library-software/.


### Package list of amazon-linux-extras

ℹ️ The amazon-linux-extras repository is updated regularly, so the topics and versions that you see might differ from the following list.

Last updated on 2022-09-09

```
[ec2-user@xxx /]$ amazon-linux-extras
  0  ansible2                 available    [ =2.4.2  =2.4.6  =2.8  =stable ]
  2  httpd_modules            available    [ =1.0  =stable ]
  3  memcached1.5             available    [ =1.5.1  =1.5.16  =1.5.17 ]
  5  postgresql9.6            available    [ =9.6.6  =9.6.8  =stable ]
  6  postgresql10             available    [ =10  =stable ]
  9  R3.4                     available    [ =3.4.3  =stable ]
 10  rust1                    available    [ =1.22.1  =1.26.0  =1.26.1  =1.27.2  =1.31.0  =1.38.0  =stable ]
 11  vim                      available    [ =8.0  =stable ]
 18  libreoffice              available    [ =5.0.6.2_15  =5.3.6.1  =stable ]
 19  gimp                     available    [ =2.8.22 ]
 20  docker                   available    [ =17.12.1  =18.03.1  =18.06.1  =18.09.9  =stable ]
 21  mate-desktop1.x          available    [ =1.19.0  =1.20.0  =stable ]
 22  GraphicsMagick1.3        available    [ =1.3.29  =1.3.32  =1.3.34  =stable ]
 23  tomcat8.5                available    [ =8.5.31  =8.5.32  =8.5.38  =8.5.40  =8.5.42  =8.5.50  =stable ]
 24  epel                     available    [ =7.11  =stable ]
 25  testing                  available    [ =1.0  =stable ]
 26  ecs                      available    [ =stable ]
 27  corretto8                available    [ =1.8.0_192  =1.8.0_202  =1.8.0_212  =1.8.0_222  =1.8.0_232  =1.8.0_242  =stable ]
 28  firecracker              available    [ =0.11  =stable ]
 29  golang1.11               available    [ =1.11.3  =1.11.11  =1.11.13  =stable ]
 30  squid4                   available    [ =4  =stable ]
 32  lustre2.10               available    [ =2.10.5  =2.10.8  =stable ]
 33  java-openjdk11           available    [ =11  =stable ]
 34  lynis                    available    [ =stable ]
 36  BCC                      available    [ =0.x  =stable ]
 37  mono                     available    [ =5.x  =stable ]
 38  nginx1                   available    [ =stable ]
 39  ruby2.6                  available    [ =2.6  =stable ]
 40  mock                     available    [ =stable ]
 41  postgresql11             available    [ =11  =stable ]
 42  php7.4                   available    [ =stable ]
 43  livepatch                available    [ =stable ]
 44  python3.8                available    [ =stable ]
 45  haproxy2                 available    [ =stable ]
 46  collectd                 available    [ =stable ]
 47  aws-nitro-enclaves-cli   available    [ =stable ]
 48  R4                       available    [ =stable ]
 49  kernel-5.4               available    [ =stable ]
 50  selinux-ng               available    [ =stable ]
 51  php8.0                   available    [ =stable ]
 52  tomcat9                  available    [ =stable ]
 53  unbound1.13              available    [ =stable ]
 54  mariadb10.5              available    [ =stable ]
 55  kernel-5.10              available    [ =stable ]
 56  redis6                   available    [ =stable ]
 57  ruby3.0                  available    [ =stable ]
 58  postgresql12             available    [ =stable ]
 59  postgresql13             available    [ =stable ]
 60  mock2                    available    [ =stable ]
 61  dnsmasq2.85              available    [ =stable ]
 62  kernel-5.15              available    [ =stable ]
 63  postgresql14             available    [ =stable ]
 64  firefox                  available    [ =stable ]
 65  lustre                   available    [ =stable ]
```