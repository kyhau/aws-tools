# Notes

1. Ref: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
> After you restore a DB cluster with a SnapshotIdentifier property, you must specify the same SnapshotIdentifier property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the DB cluster snapshot again, and the data in the database is not changed. However, if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified SnapshotIdentifier property, and the original DB cluster is deleted. 

## Aurora Serverless

1. Performance / throughput
    > Instead of provisioning and managing database servers, you specify Aurora capacity units (ACUs). Each ACU is a combination of approximately 2 gigabytes (GB) of memory, corresponding CPU, and networking. Database storage automatically scales from 10 gibibytes (GiB) to 128 tebibytes (TiB), the same as storage in a standard Aurora DB cluster.

    See https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless.how-it-works.html

## RDS Proxy
- https://github.com/aws-samples/serverless-rds-proxy-demo
