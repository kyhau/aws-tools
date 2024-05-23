# RDS / Aurora

Jump to
- [kyhau/aws-notebook/Databases](https://github.com/kyhau/aws-notebook/blob/main/Databases.md)
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Rotate RDS database credentials automatically](#rotate-rds-database-credentials-automatically)
- [MySQL](#mysql)
- [Aurora Serverless](#aurora-serverless)
- [RDS Proxy](#rds-proxy)
- [Traps](#traps)

---

## Useful Libs and Tools

- [aws/aws-advanced-python-wrapper](https://github.com/aws/aws-advanced-python-wrapper) - AWS Advanced Python Driver
    - wraps the open-source Psycopg and the MySQL Connector/Python drivers
    - provides support for faster switchover and failover times, and authentication with AWS Secrets Manager or AWS Identity and Access Management (IAM)
- [awslabs/mpartman](https://github.com/awslabs/mpartman) - Modern partition manager for PostgreSQL (Mpartman)

## Rotate RDS database credentials automatically

(1)  A typical AWS documented approach - using an appropriate retry strategy
mentioned in
- [AWS Blog](https://aws.amazon.com/blogs/security/how-to-implement-single-user-secret-rotation-using-amazon-rds-admin-credentials/) - How to implement single-user secret rotation using Amazon RDS admin credentials, AWS, 2024-05-21
- [AWS Blog](https://aws.amazon.com/blogs/security/rotate-amazon-rds-database-credentials-automatically-with-aws-secrets-manager/) - Rotate Amazon RDS database credentials automatically with AWS Secrets Manager, AWS, 2018-04-05
- [AWS prescriptive guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/rotate-database-credentials-without-restarting-containers.html) - Rotate database credentials without restarting containers

> When the secret rotates, open database connections are not dropped. While rotation is happening, there is a short period of time between when the password in the database changes and when the secret is updated. During this time, there is a low risk of the database denying calls that use the rotated credentials. You can mitigate this risk with an appropriate retry strategy. After rotation, new connections use the new credentials.


(2) Alternatively, here is another approach - blue/green strategy

This approach ensures that it never rotates the password of the user currently being used by the container, minimizing disruptions to the system’s functionality.

See https://sitereliabilityengineering.in/seamless-rds-secret-rotation-and-ecs-task-update-no-code-change-dea851210a7d


## MySQL

- For RDS MySQL insert/delete event -> Lambda processing events
    1. Enable query logging with custom parameter group (for MySQL it should be the Audit Log, see [MySQL database log files](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.MySQL.html#USER_LogAccess.MySQL.Auditlog))
    2. Then, publish logs to CloudWatch Logs (see [Publishing MySQL logs to CloudWatch Logs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.MySQL.html#USER_LogAccess.MySQL.Auditlog))
    3. Then, create [CloudWatch Logs Subscription Filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html) with Lambda for processing the log group entries.

- [Local write forwarding with Amazon Aurora](https://aws.amazon.com/blogs/database/local-write-forwarding-with-amazon-aurora/), AWS, 2023-07-31
    - can now issue transactions containing both reads and writes on Aurora read replicas and the writes will be automatically forwarded to the single writer instance for execution.
    - makes it simple to scale read workloads which require "read after write" consistency, without the need to maintain complex application logic that separates reads from writes


## Aurora Serverless

1. Performance / throughput
    > Instead of provisioning and managing database servers, you specify Aurora capacity units (ACUs). Each ACU is a combination of approximately 2 gigabytes (GB) of memory, corresponding CPU, and networking. Database storage automatically scales from 10 gibibytes (GiB) to 128 tebibytes (TiB), the same as storage in a standard Aurora DB cluster.

    See https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html


## RDS Proxy
- https://github.com/aws-samples/serverless-rds-proxy-demo



## Traps

1. Ref: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
> After you restore a DB cluster with a SnapshotIdentifier property, you must specify the same SnapshotIdentifier property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the DB cluster snapshot again, and the data in the database is not changed. However, if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified SnapshotIdentifier property, and the original DB cluster is deleted.
