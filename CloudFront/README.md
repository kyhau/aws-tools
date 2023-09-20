# CloudFront

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [CloudFront Functions and Lambda@Edge](#cloudfront-functions-and-lambdaedge)
- [OAC vs. OAI](#oac-vs-oai)
- [S3 Website endpoint vs. S3 REST API endpoint](#s3-website-endpoint-vs-s3-rest-api-endpoint)
- [Provision CloudFront with templates in this directory](#steps-to-provision-cloudfront)
- [My QuickStart CloudFormation templates](./cfn/)


---
## Useful Libs and Tools

- [amazon-cloudfront-dynamic-content-timings](https://github.com/aws-samples/amazon-cloudfront-dynamic-content-timings) - A python script for CloudFront timings measurement.
- [amazon-cloudfront-functions-testing-tool](https://github.com/aws-samples/amazon-cloudfront-functions-testing-tool) - Amazon CloudFront Functions Test based on production traffic
- [amazon-cloudfront-multi-function-packager](https://github.com/aws-samples/amazon-cloudfront-multi-function-packager) - Amazon CloudFront Multi-function packager tool - This tool allows you to package multiple Edge Functions - Lambda@Edge or CloudFront Functions into a single function with minimal code changes.


---
## Useful Articles and Blogs

Performance / HA
- [Accelerate and protect your websites using Amazon CloudFront and AWS WAF](https://aws.amazon.com/blogs/networking-and-content-delivery/accelerate-and-protect-your-websites-using-amazon-cloudfront-and-aws-waf/), AWS, 2023-09-12
- [Achieving Zero-downtime deployments with Amazon CloudFront using blue/green continuous deployments](https://aws.amazon.com/blogs/networking-and-content-delivery/achieving-zero-downtime-deployments-with-amazon-cloudfront-using-blue-green-continuous-deployments/), AWS, 2023-05-30
- [Improve Single-Page Application (SPA) Performance with a Same Domain policy using Amazon CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/improve-single-page-application-spa-performance-with-a-same-domain-policy-using-amazon-cloudfront/), AWS, 2023-05-09
    - how you can use a same domain policy with CloudFront, to eliminate the need for enabling Cross-Origin Resource Sharing (CORS), which results in improved performance for Single-Page Applications (SPA).
- [Accelerate, protect and make dynamic workloads delivery cost efficient with Amazon CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/accelerate-protect-and-make-dynamic-workloads-delivery-cost-efficient-with-amazon-cloudfront/), AWS, 2023-04-11
- [Improve web application availability with CloudFront and Route53 hybrid origin failover](https://aws.amazon.com/blogs/networking-and-content-delivery/improve-web-application-availability-with-cloudfront-and-route53-hybrid-origin-failover/), AWS, 2023-03-03
- [Improve Single-Page Application (SPA) Performance with a Same Domain policy using Amazon CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/improve-single-page-application-spa-performance-with-a-same-domain-policy-using-amazon-cloudfront/), AWS, 2023-03-02
    - by using CloudFront's multiple origin capability
- [Three advanced design patterns for high available applications using Amazon CloudFront](https://aws.amazon.com/fr/blogs/networking-and-content-delivery/three-advanced-design-patterns-for-high-available-applications-using-amazon-cloudfront/), AWS, 2022-07-12
    1. Using Route 53 Failover routing policy with health checks on the origin domain name
    1. Using origin failover, a native feature of CloudFront
    1. Using hybrid origin failover pattern combines both (1) and (2)
- [Enhanced origin failover using Amazon CloudFront and AWS Lambda@Edge](https://aws.amazon.com/fr/blogs/media/enhanced-origin-failover-using-amazon-cloudfront-and-aws-lambdaedge/), AWS, 2020-10-14

Other
- [Set up end-to-end tracing with Amazon CloudFront using OpenTelemetry](https://aws.amazon.com/blogs/networking-and-content-delivery/set-up-end-to-end-tracing-with-amazon-cloudfront-using-opentelemetry/), AWS, 2023-07-14
- [Using AWS WAF intelligent threat mitigations with cross-origin API access](https://aws.amazon.com/blogs/networking-and-content-delivery/using-aws-waf-intelligent-threat-mitigations-with-cross-origin-api-access/), AWS, 2023-07-13
- [Amazon CloudFront introduces Origin Access Control (OAC)](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-introduces-origin-access-control-oac/), AWS, 2022-08-25
- [Using Amazon S3 Origins and Custom Origins for Web Distributions](http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [Granting Permission to an Amazon CloudFront Origin Identity](http://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html#example-bucket-policies-use-case-6)
- https://vimalpaliwal.com/blog/2018/10/10f435c29f/serving-multiple-s3-buckets-via-single-aws-cloudfront-distribution.html
- https://stackoverflow.com/questions/20632828/aws-cloud-formation-script-to-create-s3-bucket-and-distribution


---
## CloudFront Functions and Lambda@Edge

- Differences between CloudFront Functions and Lambda@Edge here:
    - [Introducing CloudFront Functions – Run Your Code at the Edge with Low Latency at Any Scale](https://aws.amazon.com/blogs/aws/introducing-cloudfront-functions-run-your-code-at-the-edge-with-low-latency-at-any-scale/), AWS, 2021-05-03

### CloudFront Functions

- [Writing and testing CloudFront Functions with production traffic](https://aws.amazon.com/blogs/networking-and-content-delivery/writing-and-testing-cloudfront-functions-with-production-traffic/), AWS, 2023-02-21
- [Optimize SEO with Amazon CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/optimize-seo-with-amazon-cloudfront/), AWS, 2023-03-28
    - with CloudFront Functions and Lambda@Edge
- [Visitor Prioritization on e-Commerce Websites with CloudFront and CloudFront Functions](https://aws.amazon.com/blogs/networking-and-content-delivery/visitor-prioritization-on-e-commerce-websites-with-cloudfront-and-cloudfront-functions/), AWS, 2023-03-23
    - CloudFront + CloudFront Functions + WAF Bot Control
    - Comparing to [Visitor Prioritization on e-Commerce Websites with CloudFront and Lambda@Edge](https://aws.amazon.com/jp/blogs/networking-and-content-delivery/visitor-prioritization-on-e-commerce-websites-with-cloudfront-and-lambdaedge/), AWS, 2018-07-30

### Lambda@Edge

- [Building a central Amazon CloudWatch Dashboard to monitor Lambda@Edge logs and metrics](https://aws.amazon.com/blogs/mt/building-a-central-amazon-cloudwatch-dashboard-to-monitor-lambdaedge-logs-and-metrics/), AWS, 2023-09-20
- [Tag-based invalidation in Amazon CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/tag-based-invalidation-in-amazon-cloudfront/), AWS, 2023-03-28
    - with Lambda@Edge, Amazon DynamoDB, AWS Lambda, and AWS Step Functions
- [Reduce latency for end-users with multi-region APIs with CloudFront](https://aws.amazon.com/blogs/networking-and-content-delivery/reduce-latency-for-end-users-with-multi-region-apis-with-cloudfront/), AWS, 2023-01-31
    - with Lambda@Edge and Route53 latency routing
- [Limiting requests to a web application using a Gatekeeper Solution](https://aws.amazon.com/blogs/networking-and-content-delivery/limiting-requests-to-a-web-application-using-a-gatekeeper-solution/), AWS, 2023-03-21
    - The Gatekeeper mechanism limits requests to your web applications or APIs and prevents attacks which AWS WAF may not be the best solution.


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
