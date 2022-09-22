# EC2

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [CloudWatch Agent](../CloudWatch/README.md)
- [On-Demand Instance vCPUs limits](#on-demand-instance-vcpus-limits)
- [Quick Start Linux utilities](#quick-start-linux-utilities)


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
