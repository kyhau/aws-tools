# S3

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
    - [VPC Enpoints](#vpc-enpoints)
    - [Static Websites](#static-websites)
    - [Uploading objects](#uploading-objects)
    - [Storing sensitive files](#storing-sensitive-files)

---
## Useful Libs and Tools


---
## Useful Articles and Blogs

### VPC Enpoints
- [Using interface endpoints to access Amazon S3 without a gateway endpoint or an internet gateway in the VPC](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#accessing-bucket-and-aps-from-interface-endpoints), AWS User Guide
- [Choosing Your VPC Endpoint Strategy for Amazon S3](https://aws.amazon.com/blogs/architecture/choosing-your-vpc-endpoint-strategy-for-amazon-s3/), AWS, 2021-07-23
    - S3 gateway endpoint and interface endpoint

### Static Websites
- [Hosting Internal HTTPS Static Websites with ALB, S3, and PrivateLink](https://aws.amazon.com/blogs/networking-and-content-delivery/hosting-internal-https-static-websites-with-alb-s3-and-privatelink/), AWS, 2022-12-30
    - ALB, S3 Interface Endpoint, S3


### Uploading objects
- [Patterns for building an API to upload files to Amazon S3](https://aws.amazon.com/blogs/compute/patterns-for-building-an-api-to-upload-files-to-amazon-s3/), AWS, 2023-05-03


### Storing sensitive files
- [What is the most secure option for storing highly sensitive / private files in S3?](https://stackoverflow.com/questions/70238041/what-is-the-most-secure-option-for-storing-highly-sensitive-private-files-in-s)
    - SSE/CSE options and their use cases
