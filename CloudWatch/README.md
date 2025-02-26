# CloudWatch

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [CloudWatch Agent](#cloudwatch-agent)
- [CloudWatch Alarm](#cloudwatch-alarm)
    - [What alerts should you have for serverless applications?](https://lumigo.io/blog/what-alerts-should-you-have-for-serverless-applications/)
    - [Some known issues](#some-known-issues)
- [CloudWatch Application Signals](#cloudwatch-application-signals)
- [CloudWatch Synthetics](#cloudwatch-synthetics)


---
### Useful Libs and Tools

- [awslabs/aws-embedded-metrics-python](https://github.com/awslabs/aws-embedded-metrics-python)


---
### CloudWatch Agent

- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent-New-Instances-CloudFormation.html
    - append_dimensions, AutoScalingGroupName
    - metrics_collected, mem_used_percent, swap_used_percent
- https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-failed-signal/
    - /var/log/cloud-init-output.log
    - /var/log/cloud-init.log
    - /var/log/cfn-init.log
    - /var/log/cfn-init-cmd.log
    - /var/log/cfn-wire.log
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-common-scenarios.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AgentReference.html
- https://stackoverflow.com/questions/55098841/cloudformation-output-of-cloudformation-init


---
### CloudWatch Alarm

#### Some known issues

1. Delay in ASG Cloudwatch Alarm issue

    - There's a post from people who experienced "Delay in ASG Cloudwatch Alarm issue" and they mentioned a response from AWS ([Source: stackoverflow](https://stackoverflow.com/questions/64044268/delay-in-aws-cloudwatch-alarm-state-change), Oct 11 '20)

    - **"The ALB metric delay is due to an Ingestion delay time of 3 minutes and this delay cannot be reduced at this stage"**

    - > CloudWatch being a push based service, the data is pushed from the source service- ELB. Some delay in metrics is expected, which is inherent for any monitoring systems- as they depend on several variables such as delay with the service publishing the metric, propagation delays and ingestion delay within CloudWatch to name a few. I do understand that a consistent 3 or 4 minute delay for ALB metrics is on the higher side. Upon further investigation, **I found out that the ALB metric delay is due to an Ingestion delay time of 3 minutes and this delay cannot be reduced at this stage**.
    Furthermore, please kindly note that the CloudWatch OPS and internal service team are still working on this issue, however, the ETA (Estimated Time of Availability) is still unknown. I sincerely apologize for any inconvenience this has caused on your side."


---
### CloudWatch Application Signals

- [Application Signals supported systems](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals-supportmatrix.html)
- [Use a custom setup to enable Application Signals on Amazon ECS](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals-Enable-ECS.html)


---
### CloudWatch Synthetics

- [How to validate authentication with self-signed certificates in Amazon CloudWatch Synthetics](https://aws.amazon.com/blogs/mt/how-to-validate-authentication-with-self-signed-certificates-in-amazon-cloudwatch-synthetics/), AWS, 2023-08-13
- [Create fine-grained CloudWatch canary schedules with cron expressions](https://aws.amazon.com/blogs/mt/create-fine-grained-cloudwatch-canary-schedules-with-cron-expressions/), AWS, 2021-08-24
- [Delete Amazon CloudWatch Synthetics dependent resources when you delete a CloudFormation stack](https://aws.amazon.com/blogs/mt/delete-amazon-cloudwatch-synthetics-dependent-resources-when-you-delete-a-cloudformation-stack/), AWS, 2021-05-07
- [Multi-step API monitoring using Amazon CloudWatch Synthetics](https://aws.amazon.com/blogs/mt/multi-step-api-monitoring-using-amazon-cloudwatch-synthetics/), AWS, 2021-03-31
- [Running a canary on a VPC](https://github.com/awsdocs/amazon-cloudwatch-user-guide/blob/master/doc_source/CloudWatch_Synthetics_Canaries_VPC.md)
