# AWS Config

Jump to
- [Using tools in this repo](#using-tools-in-this-repo)
- [AWS Config Cost Surprise](#aws-config-cost-surprise)
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Querying AWS resources](#querying-aws-resources)


---
## Using tools in this repo

- [list_all_aws_config_resource_types.sh](./list_all_aws_config_resource_types.sh) - List all currently supported AWS Config Resource Types.
- [query_configservice_aggregate.py](./query_configservice_aggregate.py) - Using select_aggregate_resource_config to query resources through Aggregator.
- [query_configservice.py](./query_configservice.py) - Using select_resource_config to query resources for individual accounts.
- Some predefined SQL files can be found in [sql_files](./sql_files/)


---
## AWS Config Cost Surprise

There could be new Config configuration items created even you have not made a new deployment.

E.g., ECS workload using VPC Networking mode
- https://repost.aws/questions/QUQ20A2JVBTvaeZlpIgdwljg/aws-config-cost-increase
- https://cloudsoft.io/blog/surprise-aws-config-costs-and-how-to-avoid-them

Config tracks everything, so an ENI is in a subnet so it tracks it back that way too. ENI has an Security Group associated so it also counts that. VPC is in the same boat.

If you look at Config history or CloudTrail creating that interface should be able to track down the root cause. Things we have seen before:
- Task cycling due to health checks or schedule
- Glue with bad data or config (it uses ENIs internally)
- Lambdas firing other things that in turn fire lambdas



---
## Useful Libs and Tools

- [awslabs/aws-config-resource-schema](https://github.com/awslabs/aws-config-resource-schema) - AWS Config Resource Schema
- [awslabs/aws-config-rdk](https://github.com/awslabs/aws-config-rdk) - AWS Config Rules Development Kit (RDK) CLI
- [awslabs/aws-config-rdklib](https://github.com/awslabs/aws-config-rdklib) - AWS Config Rules Development Kit (RDK) Library (Python)
- [aws-samples/aws-cfn-for-optimizing-aws-config-for-aws-security-hub](https://github.com/aws-samples/aws-cfn-for-optimizing-aws-config-for-aws-security-hub) - AWS CloudFormation for optimizing AWS Config for AWS Security Hub

---
## Useful Articles and Blogs

- [Optimize AWS Config for AWS Security Hub to effectively manage your cloud security posture](https://aws.amazon.com/blogs/security/optimize-aws-config-for-aws-security-hub-to-effectively-manage-your-cloud-security-posture/), AWS, 2023-07-17


---
## Querying AWS resources

- [Querying AWS resources](
  https://docs.aws.amazon.com/config/latest/developerguide/querying-AWS-resources.html)
- [Resource Types supported](
  https://docs.aws.amazon.com/en_pv/config/latest/developerguide/resource-config-reference.html)

### Using CLI
```
aws configservice select-resource-config --expression "$(cat ec2.sql)"
```

The SQL SELECT query components are as follows.
```
SELECT property [, ...]
[ WHERE condition ]
[ GROUP BY property ]
[ ORDER BY property [ ASC | DESC ] [, property [ ASC | DESC ] ...] ]
```

Examples
```
SELECT resourceId WHERE resourceType='AWS::EC2::Instance'
```

```
SELECT configuration.complianceType, COUNT(*)
WHERE resourceType = 'AWS::Config::ResourceCompliance'
GROUP BY configuration.complianceType
```

```
SELECT
    resourceId,
    resourceType,
    configuration.instanceType,
    configuration.placement.tenancy,
    configuration.imageId,
    availabilityZone
WHERE
    resourceType = 'AWS::EC2::Instance'
    AND configuration.imageId = 'ami-99c7e87ff8cf57a8e'
```
