# Notes

- [Enforcing enterprise-wide preventive controls with AWS Organizations](https://aws.amazon.com/blogs/mt/enforcing-enterprise-wide-preventive-controls-with-aws-organizations/), AWS, 2025-01-09
    - Choosing the right policy: when to use SCPs, RCPs, and declarative policies


## RCP (Resource Control Policy)

- [aws-samples/resource-control-policy-examples](https://github.com/aws-samples/resource-control-policy-examples)
- https://github.com/aws-samples/data-perimeter-policy-examples/blob/main/resource_control_policies/identity_perimeter_rcp.json

## SCP

- [Prevent Expensive AWS API Actions with SCPs](https://hackingthe.cloud/aws/general-knowledge/block-expensive-actions-with-scps/), July 30, 2024
- Denies access to AWS based on the requested Region [example](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_deny-requested-region.html)
- [matthewdfuller/safer-scps](https://github.com/matthewdfuller/safer-scps) - Safer SCPs: Real-Time SCP Error Monitor
