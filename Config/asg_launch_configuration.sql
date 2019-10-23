SELECT
    resourceId,
    configuration.launchConfigurationName
WHERE
    resourceType = 'AWS::AutoScaling::AutoScalingGroup'
