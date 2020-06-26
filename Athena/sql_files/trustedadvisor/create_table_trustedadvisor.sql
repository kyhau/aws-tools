CREATE EXTERNAL TABLE IF NOT EXISTS k_collection.trustedadvisor (
  `AccountId` string,
  `Category` string,
  `Id` string,
  `Name` string,
  `ResourcesFlaggedCnt` int,
  `ResourcesFlagged` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION 's3://k-collection-data-xxxxxxxxxx/trustedadvisor/'
TBLPROPERTIES ('has_encrypted_data'='false');