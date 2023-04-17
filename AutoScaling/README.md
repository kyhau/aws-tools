# Auto Scaling

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Scheduled scaling](#scheduled-scaling)
- [Pre-scaling](#pre-scaling)


---
## Useful Libs and Tools

- AWS Auto Scaling Custom Resources - [aws/aws-auto-scaling-custom-resource](https://github.com/aws/aws-auto-scaling-custom-resource)


---
## Useful Articles and Blogs

- [Choosing the right health check with Elastic Load Balancing and EC2 Auto Scaling](https://aws.amazon.com/blogs/networking-and-content-delivery/choosing-the-right-health-check-with-elastic-load-balancing-and-ec2-auto-scaling/), AWS, 11 Apr 2023
    - There are three strategies to measure instance health:
        1. liveness checks,
        2. local health checks (or shallow health checks), and
        3. dependency health checks (or deep health checks).
    - See also [Implementing health checks](https://aws.amazon.com/builders-library/implementing-health-checks/)
- AWS scaling options - AWS Auto Scaling vs. Amazon EC2 Auto Scaling vs. Auto Scaling for Other Services
    - See "Q. How is AWS Auto Scaling different than the scaling capabilities for individual services?" in https://aws.amazon.com/autoscaling/faqs/

---
## Scheduled scaling

ℹ️ The cron expression formats used in `AWS::AutoScaling::ScheduledAction` and `AWS::ApplicationAutoScaling::ScalableTarget` are different.
- For ASG / `AWS::AutoScaling::ScheduledAction`
  (see [details](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscaling-scheduledaction)):
   ```
   [Minute] [Hour] [DayOfMonth] [MonthOfYear] [DayOfWeek]
   ```
- For Fargate / `AWS::ApplicationAutoScaling::ScalableTarget`
  (see [details](https://docs.aws.amazon.com/autoscaling/application/userguide/scheduled-scaling-using-cron-expressions.html)):
   ```
   cron(Minutes Hours DayOfMonth Month DayOfWeek Year)
   ```

### ECS
- AWS::ApplicationAutoScaling::ScalableTarget
- CLI https://gist.github.com/toricls/fea9d8a4eb606a27f6666a1abc6a6fd8
- Doc https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-scheduled-scaling.html

### ASG
- AWS::AutoScaling::ScheduledAction
- CLI https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html#create-sch-actions-aws-cli


---
## Pre-scaling

As `desired = running + pending - terminating`,
but scaling calculates only use `running`, so it can get into race conditions when setting `desired` out of band.

Possible solutions:
- Include `ScalingSuspend` and `ScalingResume` calls around any pre-scaling tasks.
- Use scaling policy to scale up/down, instead of setting `desired` count.
