# Inspector

General approach

1. Amazon Inspector runs and performs a security assessment. It sends a message to an SNS topic at the end of the run.
2. The Lambda function is invoked by the SNS message.
3. The function fetches the findings from the security assessment.
4. The function formats and emails the findings using another SNS topic.


See also

- [Inspector - Supported operating systems and programming languages](https://docs.aws.amazon.com/inspector/latest/user/supported.html)
- [Setting Up Automatic Assessment Runs Through a Lambda Function](
  https://docs.aws.amazon.com/inspector/latest/userguide/inspector_assessments.html#assessment_runs-schedule)
- [Setting Up an SNS Topic for Amazon Inspector Notifications](
  https://docs.aws.amazon.com/inspector/latest/userguide/inspector_assessments.html#sns-topic)
- [ARNs for setting up an SNS Topic for Amazon Inspector Notifications](
  https://docs.aws.amazon.com/inspector/latest/userguide/inspector_assessments.html)
- [How to use an AWS Lambda function to forward Amazon Inspector findings to your ticketing and workflow systems](
  https://aws.amazon.com/blogs/aws/scale-your-security-vulnerability-testing-with-amazon-inspector/)
    - Lambda src: https://github.com/awslabs/amazon-inspector-finding-forwarder
- [awslabs/amazon-inspector-auto-remediate](https://github.com/awslabs/amazon-inspector-auto-remediate) -
  This is an AWS Lambda job, written in Python, to automatically patch EC2 instances when an inspector assessment generates a CVE finding.

Sources
- https://github.com/awslabs/amazon-inspector-finding-forwarder
- https://github.com/awslabs/amazon-inspector-agent-autodeploy
- https://github.com/awslabs/amazon-inspector-auto-remediate
- https://github.com/degica/scheduled-inspector-run
