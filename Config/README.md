# Querying AWS resources

See also 
- [Querying AWS resources](
  https://docs.aws.amazon.com/config/latest/developerguide/querying-AWS-resources.html)
- [Resource Types supported](
  https://docs.aws.amazon.com/en_pv/config/latest/developerguide/resource-config-reference.html)

CLI
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