# Templates for CloudFront and S3 - Web Distribution

```
 ____________     _____     
| CloudFront |-->| S3  |
|____________|   |_____|
```

Two ways to integrate CloudFront with S3 for Web Distributions (e.g. api.example.com):

1. Use Custom Origins
    1. Use the S3 bucket as static website (use url: http://api-example-com.s3-website-ap-southeast-2.amazonaws.com)
    1. The S3 bucket needs to set to Public Read, i.e. it can be accessible directly without through CloudFront 

1. Use S3 Origins
    1. Use the S3 bucket as a bucket (use url: api-example-com.s3.amazonaws.com)
    1. Use Origin Access Identity to restrict S3 access only to CloudFront
    1. Need to give a Default Root Object (i.e. index.html) for accessing the single page app 
    1. Need to redirect 403 to index page

See also [Using Amazon S3 Origins and Custom Origins for Web Distributions](
  http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)


1. Use S3 with static website hosting for storing static content of [fond_ui](https://bitbucket.org/example/fond_ui).
1. Use CloudFront and Route53 for supporting https requests and defining custom (api) domain. 
1. Upload example.com SSL certificate to AWS Certificate Manager (ACM).


## Steps to create infrastructure

1. Create a IAM Group for deployment using `IAM-Group-ForDeployment.template` with CloudFormation.

1. Create a S3 Log bucket as the root-logs bucket (for all logging) using `S3-RootLogs.template` with CloudFormation.

1. Upload a server (ssl) certificate to IAM [using aws-cli](
   http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html#upload-server-certificate):

   ```
   > aws iam upload-server-certificate \
        --server-certificate-name example \
        --certificate-body file://example.crt \
        --private-key file://example.key \
        --certificate-chain file://intermediate.crt \
        --path /cloudfront/
   ```

   To retrieve the `ServerCertificateId` or other certificate details:
   
   ```
   > aws iam list-server-certificates (--profile your-aws-profile)
   ```

1. Add Origin Access Identity for CloudFront to interact with S3 buckets.

   (if you use `CloudFront-S3-WebDistribution-UseS3Origin.template`)

   Note that an Origin Access Identity [cannot be created with CloudFormation](
     https://stackoverflow.com/questions/20632828/aws-cloud-formation-script-to-create-s3-bucket-and-distribution).

1. Use CloudFormation template `CloudFront-S3-WebDistribution-xxx.template` to

    1. Create S3 bucket with Static Website, Versioning and Logging enabled.
    1. Create Bucket Policy for PublicRead access (if using Custom Origins approach).
    1. Create a Managed Policy for managing and uploading files to the S3 bucket.
    1. Attach the Managed Policy to the given Group.
    1. Create a CloudFront Distribution
    
1. Add new Route53 record set for each CloudFront Alias as CNAME pointing to
   the CloudFront Domain name.


#### Notes

##### CloudFront: Error: NoSuchKey? [Ref](https://stackoverflow.com/questions/15309113/amazon-cloudfront-doesnt-respect-my-s3-website-buckets-index-html-rules)

1. Check the “Origin Domain Name” of that distribution.
1. DO NOT use the domain name of the S3 bucket which was provided in the auto-complete droplist, e.g. “mywebsite.s3.amazonaws.com”.
1. Use the actual hosting domain name, e.g. “mywebsite.s3-website-us-east-1.amazonaws.com”.

##### When granting permission to CloudFront to access S3 through Origin Access Identity

In the CloudFormation template, specify (where xxxxxx is S3 CanonicalUser ID)

```
"Principal": {
  {"CanonicalUser": "xxxxxx"}
},
```

Then the BucketPolicy to be created will become:

```
"Principal": {
  "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity xxxxxxxxxxxx"
},
```

See also [Granting Permission to an Amazon CloudFront Origin Identity](
  http://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html#example-bucket-policies-use-case-6).
