CREATE OR REPLACE VIEW "trustedadvisor_findings" AS
SELECT metricname, category, accountname,
CASE
  WHEN resourcesflaggedcnt is null THEN 0
  ELSE resourcesflaggedcnt
END AS flaggedcount
FROM (
  SELECT 'Amazon EBS Public Snapshots' metricname
  UNION
  SELECT 'Amazon RDS Public Snapshots' metricname
  UNION
  SELECT 'Amazon S3 Bucket Permissions' metricname
  UNION
  SELECT 'Auto Scaling Group Resources' metricname
  UNION
  SELECT 'CloudFront Custom SSL Certificates in the IAM Certificate Store' metricname
  UNION
  SELECT 'CloudFront SSL Certificate on the Origin Server' metricname
  UNION
  SELECT 'IAM Access Key Rotation' metricname
)
LEFT JOIN k_collection.trustedadvisor
ON metricname = name
