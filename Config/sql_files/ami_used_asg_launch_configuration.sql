SELECT
    resourceId,
    configuration.imageId
WHERE
    resourceType = 'AWS::AutoScaling::LaunchConfiguration'
