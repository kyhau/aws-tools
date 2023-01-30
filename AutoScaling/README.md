# Auto Scaling

1. AWS scaling options - AWS Auto Scaling vs. Amazon EC2 Auto Scaling vs. Auto Scaling for Other Services
    - See "Q. How is AWS Auto Scaling different than the scaling capabilities for individual services?" in https://aws.amazon.com/autoscaling/faqs/
2. AWS Auto Scaling Custom Resources - [aws/aws-auto-scaling-custom-resource](https://github.com/aws/aws-auto-scaling-custom-resource)

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

## ECS
- AWS::ApplicationAutoScaling::ScalableTarget
- CLI https://gist.github.com/toricls/fea9d8a4eb606a27f6666a1abc6a6fd8
- Doc https://docs.aws.amazon.com/autoscaling/application/userguide/application-auto-scaling-scheduled-scaling.html

## ASG
- AWS::AutoScaling::ScheduledAction
- CLI https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scheduled-scaling.html#create-sch-actions-aws-cli
