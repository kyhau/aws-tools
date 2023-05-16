SELECT
  COUNT(*),
  resourceType,
  accountId
WHERE
  resourceType = 'AWS::EKS::Cluster'
GROUP BY
  resourceType,
  accountId
