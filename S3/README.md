# S3

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
    - [Data Perimeter at scale](#data-perimeter-at-scale)
    - [CloudTrail Events vs. Server Access Logs](#cloudtrail-events-vs-server-access-logs)
    - [S3 Incident Response](#s3-incident-response)
    - [S3 Access Control](#s3-access-control)
    - [VPC Enpoints](#vpc-enpoints)
    - [Static Websites](#static-websites)
    - [Uploading objects](#uploading-objects)
    - [Storing sensitive files](#storing-sensitive-files)
    - [Getting "The bucket does not allow ACLs" Error](#getting-the-bucket-does-not-allow-acls-error)
- [Bucket policies](#bucket-policies)

---

## Useful Libs and Tools

- [aws/boto3-s3-access-grants-plugin](https://github.com/aws/boto3-s3-access-grants-plugin) - AWS S3 Access Grants Plugin provides the functionality to enable S3 customers to configure S3 ACCESS GRANTS as a permission layer on top of the S3 Clients.
- [awslabs/mountpoint-s3](https://github.com/awslabs/mountpoint-s3) - Mountpoint for Amazon S3 is a simple, high-throughput file client for mounting an Amazon S3 bucket as a local file system.


## Useful Articles and Blogs

### Data Perimeter at scale

- [Blog Post Series](https://aws.amazon.com/identity/data-perimeters-blog-post-series/): Establishing a Data Perimeter on AWS - (with nice diagrams and practical use cases)
- [Data perimeters on AWS](https://aws.amazon.com/identity/data-perimeters-on-aws/) - with nice summary
- [Examples](https://github.com/aws-samples/data-perimeter-policy-examples) on GitHub


### CloudTrail Events vs. Server Access Logs

- CloudTrail Events
    - Logs Delay
        - Data events: 5 minutes
        - Management events: 15 minutes
    - Log Coverage
        - Bucket operations: covered by default
        - Object operations: if data events are enabled
    - Cost
        - Management events: Free
        - Data events: Pay according to number of API calls
    - Log Format
        - JSON
- Server Access Log
    - Logs Delay
        - A few hours
    - Log Coverage
        - The completeness of server loggins is not guaranteed
    - Cost
        - Free (only pay for 3 storage of logs)
    - Log Format
        - Non-standard, requires normalisation
    - Lifecycle deletion actions are not caught by CloudTrail data event logs, only Server Access Logs.


### S3 Incident Response

- [The Rise of S3 Ransomware: How to Identify and Combat It](https://thehackernews.com/2023/10/the-rise-of-s3-ransomware-how-to.html), The Hacker News, 2023-10-25
- Related SQL queries from https://github.com/axon-git/threat-hunting
- Playbook and workshop from AWS
    - https://github.com/aws-samples/aws-customer-playbook-framework/blob/main/docs/Ransom_Response_S3.md
    - https://catalog.workshops.aws/aws-cirt-ransomware-simulation-and-detection/en-US


### S3 Access Control

- [IAM Policies and Bucket Policies and ACLs! Oh, My! (Controlling Access to S3 Resources)](https://aws.amazon.com/blogs/security/iam-policies-and-bucket-policies-and-acls-oh-my-controlling-access-to-s3-resources/), AWS, 2023-07-07


### VPC Enpoints
- [Using interface endpoints to access Amazon S3 without a gateway endpoint or an internet gateway in the VPC](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#accessing-bucket-and-aps-from-interface-endpoints), AWS User Guide
- [Choosing Your VPC Endpoint Strategy for Amazon S3](https://aws.amazon.com/blogs/architecture/choosing-your-vpc-endpoint-strategy-for-amazon-s3/), AWS, 2021-07-23
    - S3 gateway endpoint and interface endpoint

### Static Websites
- [S3 static website hosting with AWS Amplify Hosting](https://aws.amazon.com/blogs/aws/simplify-and-enhance-amazon-s3-static-website-hosting-with-aws-amplify/), AWS, 2024-10-30
- [Hosting Internal HTTPS Static Websites with ALB, S3, and PrivateLink](https://aws.amazon.com/blogs/networking-and-content-delivery/hosting-internal-https-static-websites-with-alb-s3-and-privatelink/), AWS, 2022-12-30
    - ALB, S3 Interface Endpoint, S3


### Uploading objects
- [Patterns for building an API to upload files to Amazon S3](https://aws.amazon.com/blogs/compute/patterns-for-building-an-api-to-upload-files-to-amazon-s3/), AWS, 2023-05-03


### Storing sensitive files
- [What is the most secure option for storing highly sensitive / private files in S3?](https://stackoverflow.com/questions/70238041/what-is-the-most-secure-option-for-storing-highly-sensitive-private-files-in-s)
    - SSE/CSE options and their use cases

### Getting "The bucket does not allow ACLs" Error
- https://aws.amazon.com/about-aws/whats-new/2022/12/amazon-s3-automatically-enable-block-public-access-disable-access-control-lists-buckets-april-2023/
- https://stackoverflow.com/questions/76097031/aws-s3-bucket-cannot-have-acls-set-with-objectownerships-bucketownerenforced-s
- https://stackoverflow.com/questions/71080354/getting-the-bucket-does-not-allow-acls-error
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/ensure-object-ownership.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-accesscontrol
    - "S3 buckets are created with ACLs disabled by default. Therefore, unless you explicitly set the AWS::S3::OwnershipControls property to enable ACLs, your resource will fail to deploy with any value other than Private. Use cases requiring ACLs are uncommon."

## Bucket policies

### Block the use of SSE-C encryption

If your applications don’t use SSE-C as an encryption method, you can block the use of SSE-C with a resource policy applied to an S3 bucket, or by a resource control policy (RCP) applied to an organization in AWS Organizations.
   - [Preventing unintended encryption of Amazon S3 objects](https://aws.amazon.com/blogs/security/preventing-unintended-encryption-of-amazon-s3-objects/), AWS, 2025-01-15

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RestrictSSECObjectUploads",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::<your-bucket-name>/*",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption-customer-algorithm": "false"
                }
            }
        }
    ]
 }
```
