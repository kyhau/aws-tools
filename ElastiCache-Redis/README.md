# ElastiCache for Redis

Where [at-rest encryption](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/at-rest-encryption.html) applies (on-disk data):
- Data stored on SSDs (solid-state drives) in data tiering enabled clusters is always encrypted by default.
- Disk during sync, backup and swap operations
- Backups stored in S3

See also
- Data tiering - https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/data-tiering.html
- Why does swapping occur in ElastiCache? https://aws.amazon.com/premiumsupport/knowledge-center/elasticache-swap-activity/
