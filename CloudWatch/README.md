# CloudWatch

- [What alerts should you have for serverless applications?](https://lumigo.io/blog/what-alerts-should-you-have-for-serverless-applications/)

## Some known Issues

1. Delay in ASG Cloudwatch Alarm issue

    - There's a post from people who experienced "Delay in ASG Cloudwatch Alarm issue" and they mentioned a response from AWS ([Source: stackoverflow](https://stackoverflow.com/questions/64044268/delay-in-aws-cloudwatch-alarm-state-change), Oct 11 '20)

    - **"The ALB metric delay is due to an Ingestion delay time of 3 minutes and this delay cannot be reduced at this stage"**

    - > CloudWatch being a push based service, the data is pushed from the source service- ELB. Some delay in metrics is expected, which is inherent for any monitoring systems- as they depend on several variables such as delay with the service publishing the metric, propagation delays and ingestion delay within CloudWatch to name a few. I do understand that a consistent 3 or 4 minute delay for ALB metrics is on the higher side. Upon further investigation, **I found out that the ALB metric delay is due to an Ingestion delay time of 3 minutes and this delay cannot be reduced at this stage**. 
Furthermore, please kindly note that the CloudWatch OPS and internal service team are still working on this issue, however, the ETA (Estimated Time of Availability) is still unknown. I sincerely apologize for any inconvenience this has caused on your side."

