# CloudFront


## Steps to provision infrastructure

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

1. Use CloudFormation template `CloudFront-S3-WebDistribution-xxx.template` to
    1. Create S3 bucket with Static Website, Versioning and Logging enabled.
    1. Create Bucket Policy for PublicRead access (if using Custom Origins approach).
    1. Create a Managed Policy for managing and uploading files to the S3 bucket.
    1. Attach the Managed Policy to the given Group.
    1. Create a CloudFront Distribution

1. Add new Route53 record set for each CloudFront Alias as CNAME pointing to
   the CloudFront Domain name.


---
## Notes

1. S3 Website endpoint vs. S3 REST API endpoint

    1. If you use an **S3 bucket as the origin**, CloudFront uses the **REST API** interface of S3 to communicate with the origin.

        1. S3 REST API is more versatile, allowing the client to pass richer information like AWS Identity, thereby allowing the exchange of information that makes **OAI** possible.

    2. If you use the **website endpoint as the origin**, CloudFront uses the **website URL** as the origin.

        1. E.g. http://bucket-name.s3-website.Region.amazonaws.com/object-name

        2. **OAI** cannot be used when CloudFront is using the **website endpoint** where only **GET** and **HEAD** requests are allowed on objects.

        3. **OAI** cannot be used. Instead, we have to use an **origin custom header** that only **CloudFront** can inject into the **Origin-bound HTTP** request.

        4. The **bucket policy** of the S3 bucket hosting the static website can then check for **the existence of said header**. The assumption here is that if any browser ever directly uses the website URL of the S3 hosted static website, their request will not contain this header, and hence will be rejected by the bucket policy.

        5. Also, S3 hosted static websites **do not support HTTPS**.
            1. We can only set **Viewer Protocol Policy**. Only the **browser to CloudFront half** will be HTTPS. The **CloudFront to Origin half** cannot be HTTPS in this case.
            2. Therefore, **Origin Protocol Policy**, in this case, **cannot be set to HTTPS Only**.

    3. See also https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteEndpoints.html#WebsiteRestEndpointDiff.


1. CloudFront: Error: NoSuchKey?
    ([Ref](https://stackoverflow.com/questions/15309113/amazon-cloudfront-doesnt-respect-my-s3-website-buckets-index-html-rules))

    1. Check the “Origin Domain Name” of that distribution.
    1. DO NOT use the domain name of the S3 bucket which was provided in the auto-complete droplist, e.g. “mywebsite.s3.amazonaws.com”.
    1. Use the actual hosting domain name, e.g. “mywebsite.s3-website-us-east-1.amazonaws.com”.


1. When granting permission to CloudFront to access S3 through Origin Access Identity

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


---

## Useful links
- [Using Amazon S3 Origins and Custom Origins for Web Distributions](
  http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [Granting Permission to an Amazon CloudFront Origin Identity](
  http://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html#example-bucket-policies-use-case-6)
- https://vimalpaliwal.com/blog/2018/10/10f435c29f/serving-multiple-s3-buckets-via-single-aws-cloudfront-distribution.html
- https://stackoverflow.com/questions/20632828/aws-cloud-formation-script-to-create-s3-bucket-and-distribution
