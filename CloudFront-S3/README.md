# CloudFront

Jump to
- [Provision CloudFront with templates in this directory](#steps-to-provision-cloudfront)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [OAC vs. OAI](#oac-vs-oai)
- [S3 Website endpoint vs. S3 REST API endpoint](#s3-website-endpoint-vs-s3-rest-api-endpoint)
- [My QuickStart CloudFormation templates](./cfn/)


---
## Steps to provision CloudFront

If using custom domain/CNAME, do also (1), (2) and (4); if not, only (3).

1. Upload a server (ssl) certificate to IAM [using aws-cli](
   http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html#upload-server-certificate):

   ```
   aws iam upload-server-certificate \
       --server-certificate-name example \
       --certificate-body file://example.crt \
       --private-key file://example.key \
       --certificate-chain file://intermediate.crt \
       --path /cloudfront/
   ```

2. To retrieve the `ServerCertificateId` or other certificate details:

   ```
   aws iam list-server-certificates (--profile your-aws-profile)
   ```

3. Use CloudFormation template `CloudFront-S3-WebDistribution-xxx.template` to
    1. Create S3 bucket with Static Website, Versioning and Logging enabled.
    1. Create Bucket Policy for PublicRead access (if using Custom Origins approach).
    1. Create a Managed Policy for managing and uploading files to the S3 bucket.
    1. Attach the Managed Policy to the given Group.
    1. Create a CloudFront Distribution

4. Add new Route53 record set for each CloudFront Alias as CNAME pointing to the CloudFront Domain name.


---
## Useful Articles and Blogs
- [Amazon CloudFront introduces Origin Access Control (OAC)](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-introduces-origin-access-control-oac/)
- [Using Amazon S3 Origins and Custom Origins for Web Distributions](http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [Granting Permission to an Amazon CloudFront Origin Identity](http://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html#example-bucket-policies-use-case-6)
- https://vimalpaliwal.com/blog/2018/10/10f435c29f/serving-multiple-s3-buckets-via-single-aws-cloudfront-distribution.html
- https://stackoverflow.com/questions/20632828/aws-cloud-formation-script-to-create-s3-bucket-and-distribution

---
## OAC vs. OAI

Origin Access Control (OAC) and Origin Access Identity (OAI)
([Source](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-introduces-origin-access-control-oac/))


While OAI provides a secure way to access S3 origins to CloudFront, it has limitations such as not supporting granular policy configurations, HTTP and HTTPS requests that use the POST method in AWS regions that require AWS Signature Version 4 (SigV4), or integrating with SSE-KMS.

OAC is based on an AWS best practice of using IAM service principals to authenticate with S3 origins. Compared with OAI, some of the notable enhancements OAC provide include:

1. Security – OAC is implemented with enhanced security practices like short term credentials, frequent credential rotations, and resource-based policies. They strengthen your distributions’ security posture and provides better protections against attacks like confused deputy.
2. Comprehensive HTTP methods support – OAC supports GET, PUT, POST, PATCH, DELETE, OPTIONS, and HEAD.
3. SSE-KMS – OAC supports downloading and uploading S3 objects encrypted with SSE-KMS.
4. Access S3 in all AWS regions – OAC supports accessing S3 in all AWS regions, including existing regions and all future regions. In contrast, OAI will only be supported in existing AWS regions and regions launched before December 2022.

When using OAC, a typical request and response workflow will be:
1. A client sends HTTP or HTTPS requests to CloudFront.
2. CloudFront edge locations receive the requests. If the requested object is not already cached, CloudFront signs the requests using OAC signing protocol (SigV4 is currently supported.)
3. S3 origins authenticate, authorize, or deny the requests. When configuring OAC, you can choose among three signing behaviors – “Do not sign requests”, “Sign requests”, and sign requests but “Do not override authorization header”. For details, see ([Source](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-introduces-origin-access-control-oac/)).

---
## S3 Website endpoint vs. S3 REST API endpoint

1. If you use an **S3 bucket as the origin**, CloudFront uses the **REST API** interface of S3 to communicate with the origin.
    1. E.g. bucket-name.s3.Region.amazon.com
    1. S3 REST API is more versatile, allowing the client to pass richer information like AWS Identity, thereby allowing the exchange of information that makes **OAC** (or **OAI**) possible.

2. If you use the **website endpoint as the origin**, CloudFront uses the **website URL** as the origin.
    1. E.g. http://bucket-name.s3-website.Region.amazonaws.com/object-name
    2. **OAI** cannot be used when CloudFront is using the **website endpoint** where only **GET** and **HEAD** requests are allowed on objects.
    3. **OAI** cannot be used. Instead, we have to use an **origin custom header** that only **CloudFront** can inject into the **Origin-bound HTTP** request.
    4. The **bucket policy** of the S3 bucket hosting the static website can then check for **the existence of said header**. The assumption here is that if any browser ever directly uses the website URL of the S3 hosted static website, their request will not contain this header, and hence will be rejected by the bucket policy.
    5. Also, S3 hosted static websites **do not support HTTPS**.
        1. We can only set **Viewer Protocol Policy**. Only the **browser to CloudFront half** will be HTTPS. The **CloudFront to Origin half** cannot be HTTPS in this case.
        2. Therefore, **Origin Protocol Policy**, in this case, **cannot be set to HTTPS Only**.

3. See also https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteEndpoints.html#WebsiteRestEndpointDiff.

