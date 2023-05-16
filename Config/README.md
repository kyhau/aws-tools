# AWS Config

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Querying AWS resources](#querying-aws-resources)


---
## Useful Libs and Tools

- [awslabs/aws-config-resource-schema](https://github.com/awslabs/aws-config-resource-schema) - AWS Config Resource Schema
- [awslabs/aws-config-rdk](https://github.com/awslabs/aws-config-rdk) - AWS Config Rules Development Kit (RDK) CLI
- [awslabs/aws-config-rdklib](https://github.com/awslabs/aws-config-rdklib) - AWS Config Rules Development Kit (RDK) Library (Python)


---
## Useful Articles and Blogs


---
## Querying AWS resources

- [Querying AWS resources](
  https://docs.aws.amazon.com/config/latest/developerguide/querying-AWS-resources.html)
- [Resource Types supported](
  https://docs.aws.amazon.com/en_pv/config/latest/developerguide/resource-config-reference.html)

### Using tools in this repo

- [list_all_aws_config_resource_types.sh](./list_all_aws_config_resource_types.sh) - List all currently supported AWS Config Resource Types.
- [query_configservice_aggregate.py](./query_configservice_aggregate.py) - Using select_aggregate_resource_config to query resources through Aggregator.
- [query_configservice.py](./query_configservice.py) - Using select_resource_config to query resources for individual accounts.
- Some predefined SQL files can be found in [sql_files](./sql_files/)

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
