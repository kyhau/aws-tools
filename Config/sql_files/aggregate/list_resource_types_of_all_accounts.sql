SELECT
  COUNT(*),
  resourceType,
  accountId
GROUP BY
  resourceType,
  accountId
