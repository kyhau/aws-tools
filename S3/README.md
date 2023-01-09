# S3

- Replicate different subsets of objects from one account to another account with [replication configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-add-config.html)

---
## Troubleshooting
See also https://docs.aws.amazon.com/AmazonS3/latest/dev/troubleshooting.html

---
### See "An error occurred (AccessDenied) when calling the UploadPart operation: Access Denied"
If you see "An error occurred (AccessDenied) when calling the UploadPart operation: Access Denied",
it means the file is large and it triggered "multipart" upload.

Solution 1:
- Update `.aws/config` and use `multipart_threshold` to avoid multipart uploading. For example:
   ```
   [profile your-profile-name]
   s3 =
     multipart_threshold = 150MB
   ```
