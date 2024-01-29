## AWS FIS and Chaos Engineering

Jump to
- [Tools and libs](#tools-and-libs)
- [Blog posts](#blog-posts)

---
## Tools and libs

- [amzn/awsssmchaosrunner](https://github.com/amzn/awsssmchaosrunner) - AWS SSM Chaos Runner

- [adhorn/chaos-ssm-documents](https://github.com/adhorn/chaos-ssm-documents) - Chaos Injection for AWS resources using Amazon SSM Run Command and Automation

- [aws-samples/chaos-engineering-on-amazon-eks](https://github.com/aws-samples/chaos-engineering-on-amazon-eks) - This lab shows you how to run some basic chaos engineering experiments on Amazon Elastic Kubernetes Service or EKS.

- [aws-samples/spot-interruption-simulation](https://github.com/aws-samples/spot-interruption-simulation) - This sample provides end to end automation of EC2 Spot Interruption simulation with application availability testing during Spot interruption. This uses AWS Fault Injection Simulator(FIS), Lambda(Python Runtime) and Step Function workflow for end to end automation.

- [aws-samples/aws-anz-devlabs-ecs-fis](https://github.com/aws-samples/aws-anz-devlabs-ecs-fis) - Chaos Enginnering experiments for applications running on Amazon ECS using AWS Fault Injection Simulator

- [aws-samples/chaos-engineering-with-aws-fault-injection-simulator](https://github.com/aws-samples/chaos-engineering-with-aws-fault-injection-simulator) - In this workshop, you will get a hands-on introduction to Chaos Engineering by assuming the role of newest site reliability engineer. As an SRE, you’ll be responsible for keeping microservices architecture up and running during busiest “two days” of the year.

---
## Blog posts

- [Behavior Driven Chaos with AWS Fault Injection Simulator](https://aws.amazon.com/blogs/architecture/behavior-driven-chaos-with-aws-fault-injection-simulator/), AWS, 2024-01-29
    - includes a nice example using [behave](https://github.com/behave/behave) and [Locust](https://locust.io/) to define a behaviour-driven FIS experience
