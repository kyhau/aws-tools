# Firewall Manager, WAF, Shield

Jump to
- [Firewall Manager, WAF](#firewall-manager-waf)
- [Shield](#shield)


## Firewall Manager, WAF

AWS WAF supports monitoring HTTP and HTTPS requests that are forwarded to
- CloudFront distribution,
- API Gateway REST API,
- ALB,
- AppSync GraphQL API,
- Cognito user pool, or
- App Runner service

Complex custom AWS WAF JSON rules examples
- https://repost.aws/knowledge-center/waf-create-complex-custom-rules
- NotStatement
   - https://stackoverflow.com/questions/59673364/aws-waf-create-an-acl-and-rule-to-allow-access-to-only-one-country-to-access-the

MTLA
- [How to use Amazon Athena queries to analyze AWS WAF logs and provide the visibility needed for threat detection](https://aws.amazon.com/blogs/networking-and-content-delivery/how-to-use-amazon-athena-queries-to-analyze-aws-waf-logs-and-provide-the-visibility-needed-for-threat-detection/), AWS, 2024-05-22
   - AWS WAF dashboards
   - AWS WAF logging
   - Examples of threat detection analysis using AWS WAF logs and Athena
      - Example 1: Top talkers by different criteria
      - Example 2: Get counts of various bot traffic for a given set of days
      - Example 3: Get counts of labels per IP address
      - Example 4: Top talker with additional details
      - Example 5: Website scraping and attacks
      - Example 6: AWS WAF tokens analysis (activity by IP and token misuse)
      - Example 7: Session tracking – Lifecycle of a client request (client session activity by token)
   - Tips to make Athena queries faster

Useful blog posts
- [How to enforce a security baseline for an AWS WAF ACL across your organization using AWS Firewall Manager](https://aws.amazon.com/blogs/security/how-to-enforce-a-security-baseline-for-an-aws-waf-acl-across-your-organization-using-aws-firewall-manager/), AWS, 2024-05-09
- [Cost-effective ways for securing your web applications using AWS WAF](https://aws.amazon.com/blogs/networking-and-content-delivery/cost-effective-ways-for-securing-your-web-applications-using-aws-waf/), AWS, 2023-09-13
- [Accelerate and protect your websites using Amazon CloudFront and AWS WAF](https://aws.amazon.com/blogs/networking-and-content-delivery/accelerate-and-protect-your-websites-using-amazon-cloudfront-and-aws-waf/), AWS, 2023-09-12
- [Discover the benefits of AWS WAF advanced rate-based rules](https://aws.amazon.com/blogs/security/discover-the-benefits-of-aws-waf-advanced-rate-based-rules/), AWS, 2023-09-01
- [Using AWS WAF intelligent threat mitigations with cross-origin API access](https://aws.amazon.com/blogs/networking-and-content-delivery/using-aws-waf-intelligent-threat-mitigations-with-cross-origin-api-access/), AWS, 2023-07-13


Other links
- AWS WAF Security Automations - [awslabs/aws-waf-security-automations](https://github.com/awslabs/aws-waf-security-automations)
- https://docs.aws.amazon.com/fms/2018-01-01/APIReference/API_SecurityServicePolicyData.html
- https://docs.aws.amazon.com/waf/latest/developerguide/waf-bot-control-example-scope-down-dynamic-content.html
- https://d1.awsstatic.com/whitepapers/guidelines-implementing-aws-waf.pdf
- https://blog.serverworks.co.jp/wafcharm/awsmanagedrulesknownbadInputsruleset-log4jrce


## Shield
- AWS Shield Engagement Lambda - https://s3.amazonaws.com/aws-shield-lambda/ShieldEngagementLambda.pdf
- AWS Shield Advanced can protect the following resources:
   - CloudFront Distributions
   - Route53 zones
   - Application Load Balancers
   - Network Load Balancers (Only when the NLB has a public IP which therefore falls under EIP protection - NLBs are not natively supported)
   - Classic Load Balancers
   - EIPs
   - Global Accelerators
