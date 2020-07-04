SELECT
    resourceId,
    configuration.imageId
WHERE
    resourceType = 'AWS::EC2::Instance'
