# RDS / Aurora

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Aurora](#aurora)
- [Aurora MySQL](#aurora-mysql)
- [Aurora PostgreSQL](#aurora-postgresql)
- [Aurora Serverless](#aurora-serverless)
- [RDS Proxy](#rds-proxy)
- [Traps](#traps)

See also [kyhau/aws-notebook/Databases](https://github.com/kyhau/aws-notebook/blob/main/Databases.md).

---
## Useful Libs and Tools

- [Mpartman](https://github.com/awslabs/mpartman) - Modern partition manager for PostgreSQL (Mpartman)


---
## Useful Articles and Blogs

- For RDS MySQL insert/delete event -> Lambda processing events
    1. Enable query logging with custom parameter group (for MySQL it should be the Audit Log, see [MySQL database log files](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.MySQL.html#USER_LogAccess.MySQL.Auditlog))
    2. Then, publish logs to CloudWatch Logs (see [Publishing MySQL logs to CloudWatch Logs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.MySQL.html#USER_LogAccess.MySQL.Auditlog))
    3. Then, create [CloudWatch Logs Subscription Filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html) with Lambda for processing the log group entries.


---
## Aurora

## Aurora MySQL

- [Local write forwarding with Amazon Aurora](https://aws.amazon.com/blogs/database/local-write-forwarding-with-amazon-aurora/), AWS, 2023-07-31
    - can now issue transactions containing both reads and writes on Aurora read replicas and the writes will be automatically forwarded to the single writer instance for execution.
    - makes it simple to scale read workloads which require "read after write" consistency, without the need to maintain complex application logic that separates reads from writes

## Aurora PostgreSQL

---
## Aurora Serverless

1. Performance / throughput
    > Instead of provisioning and managing database servers, you specify Aurora capacity units (ACUs). Each ACU is a combination of approximately 2 gigabytes (GB) of memory, corresponding CPU, and networking. Database storage automatically scales from 10 gibibytes (GiB) to 128 tebibytes (TiB), the same as storage in a standard Aurora DB cluster.

    See https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html


---
## RDS Proxy
- https://github.com/aws-samples/serverless-rds-proxy-demo


---
## Traps

1. Ref: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
> After you restore a DB cluster with a SnapshotIdentifier property, you must specify the same SnapshotIdentifier property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the DB cluster snapshot again, and the data in the database is not changed. However, if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified SnapshotIdentifier property, and the original DB cluster is deleted.
