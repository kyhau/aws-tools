# Notes

- [Enforcing enterprise-wide preventive controls with AWS Organizations](https://aws.amazon.com/blogs/mt/enforcing-enterprise-wide-preventive-controls-with-aws-organizations/), AWS, 2025-01-09
    - Service control policy (SCP)
        - Governs: IAM principals (within your organization)
        - Usage: Restrict the permissions of IAM principals in member accounts of your organization.
        - Considerations:
            - SCPs don’t affect IAM principals from accounts outside your organization.
            - SCPs affect requests to resources that live in accounts outside of your organization.
    - Resource control policy (RCP)
        - Governs: AWS resources (within your organization)
        - Usage: Control access to resources within your organization by IAM principals external to your organization.
        - Considerations:
            - RCPs affect IAM principals from all accounts, even those outside of your organization.
            - RCPs don’t affect requests to resources that live in accounts outside of your organization.
    - Declarative policy
        - Governs: Service configuration
        - Usage: Ensure consistent and compliant configurations for AWS services across your organization.


## RCP (Resource Control Policy)

- [aws-samples/resource-control-policy-examples](https://github.com/aws-samples/resource-control-policy-examples)
- [aws-samples/data-perimeter-policy-examples](https://github.com/aws-samples/data-perimeter-policy-examples/blob/main/resource_control_policies/identity_perimeter_rcp.json)
- [Preventing unintended encryption of Amazon S3 objects](https://aws.amazon.com/blogs/security/preventing-unintended-encryption-of-amazon-s3-objects/), AWS, 2025-01-15
    - If your applications don’t use SSE-C as an encryption method, you can block the use of SSE-C with a resource policy applied to an S3 bucket, or by a resource control policy (RCP) applied to an organization in AWS Organizations.

## SCP (Service control policy)

- [Prevent Expensive AWS API Actions with SCPs](https://hackingthe.cloud/aws/general-knowledge/block-expensive-actions-with-scps/), July 30, 2024
- Denies access to AWS based on the requested Region [example](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_deny-requested-region.html)
- [matthewdfuller/safer-scps](https://github.com/matthewdfuller/safer-scps) - Safer SCPs: Real-Time SCP Error Monitor
