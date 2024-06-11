# Inspector

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Blog Posts](#useful-blog-posts)
- [Inspector 2](#inspector-2)


## Useful Libs and Tools
- [vulnerability-scan-github-action-for-amazon-inspector](https://github.com/aws-actions/vulnerability-scan-github-action-for-amazon-inspector) - GitHub Action for Inspector
- Inspector 1/Classic
  - [awslabs/amazon-inspector-finding-forwarder](https://github.com/awslabs/amazon-inspector-finding-forwarder)
  - [awslabs/amazon-inspector-agent-autodeploy](https://github.com/awslabs/amazon-inspector-agent-autodeploy)
  - [awslabs/amazon-inspector-auto-remediate](https://github.com/awslabs/amazon-inspector-auto-remediate) -
  This is an AWS Lambda job, written in Python, to automatically patch EC2 instances when an inspector assessment generates a CVE finding.
  - https://github.com/degica/scheduled-inspector-run


## Useful Blog Posts
- [Enhance container software supply chain visibility through SBOM export with Amazon Inspector and QuickSight](https://aws.amazon.com/blogs/security/enhance-container-software-supply-chain-visibility-through-sbom-export-with-amazon-inspector-and-quicksight/), AWS, 2024-02-28


## Inspector 2
- Inspector 2 only scan things changed modified within 30 days.
- Inspector 2 supports ECR.
    - When you turn on Inspector 2, ECR scan will be disabled (cannot be enabled at the same time).
- Inspector 2 can be enabled across your organization with a single click. Once enabled, Inspector automatically discovers all of your workloads and continually scans them for software vulnerabilities and unintended network exposure. No need to schedule scaning windows.
- Inspector 2 now uses SSM agent for EC2 vulnerability scanning. No need to install additional inspector agent.
- The Inspector findings are also routed to Security Hub and pushed to EventBridge to automate with partner solutions to reduce mean time to resolution (MTTR).
