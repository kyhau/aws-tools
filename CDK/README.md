# CDK Notes

Jump to
- [My small examples for demo](#my-small-examples-for-demo)
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blog-posts)


---
## My small examples for demo

- https://github.com/kyhau/slack-chat-app-cdk (CDK v2 and testing wth SAM CLI)
- https://github.com/kyhau/slack-command-app-cdk (CDK v2 and testing wth SAM CLI)
- https://github.com/kyhau/cdk-examples (CDK v2 and v1)
- https://github.com/kyhau/have-a-smile (CDK v2)


---
## Useful Libs and Tools

- For CDK8s, see [EKS/README.md](../EKS/README.md)
- [aws-cdk](https://github.com/aws/aws-cdk) - AWS CDK
- [cdk-validator-cfnguard](https://github.com/cdklabs/cdk-validator-cfnguard) - Locally validate CDK app using AWS Control Tower proactive controls or AWS CloudFormation Guard rules before deploying the AWS infrastructure.
    - Example [Python](https://github.com/aws-samples/aws-cdk-examples/blob/master/python/cdk-validator-cfnguard/app.py)
- [cdk-nag](https://github.com/cdklabs/cdk-nag) - Manage application security and compliance
- [cdk-import](https://github.com/cdklabs/cdk-import) - Generates CDK L1 constructs for public CloudFormation Registry types and modules
- [cdk-assume-role-credential-plugin](https://github.com/aws-samples/cdk-assume-role-credential-plugin) - [AWS CDK Assume Role Credential Plugin](https://aws.amazon.com/blogs/devops/cdk-credential-plugin/)
- Constructs
    - [constructs.dev](https://constructs.dev/) - AWS CDK Construct Hub - Find reusable components for your cloud applications
    - [awslabs/aws-solutions-constructs](https://github.com/awslabs/aws-solutions-constructs) - [AWS Solutions Constructs](https://docs.aws.amazon.com/solutions/latest/constructs/api-reference.html)
    - [cdk-pipelines-github](https://constructs.dev/packages/cdk-pipelines-github) - A construct library for continuous delivery of CDK applications, deployed via GitHub Workflows
- Test
    - [How to write and execute integration tests for AWS CDK applications](https://aws.amazon.com/blogs/devops/how-to-write-and-execute-integration-tests-for-aws-cdk-applications/), AWS, 2023-07-23
    - [Testing CDK Applications in Any Language](https://aws.amazon.com/blogs/developer/testing-cdk-applications-in-any-language/), AWS, 2021-11-09
    - [How to use the AWS SAM CLI with the AWS CDK to test a Lambda function locally?](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-cdk-getting-started.html)
- [aws/jsii](https://github.com/aws/jsii) - AWS JSII allows code in any language to naturally interact with JavaScript classes
- [jsii-docgen](https://github.com/cdklabs/jsii-docgen) - Generates markdown reference documentation for jsii modules
- [cdk-patterns/serverless](https://github.com/cdk-patterns/serverless) - CDK Patterns
- [aws-samples/aws-refactoring-to-serverless](https://github.com/aws-samples/aws-refactoring-to-serverless) - CDK implementation for the patterns in [Refactorings to Serverless](https://serverlessland.com/refactoring-serverless/intro).
- [serverless-stack](https://github.com/serverless-stack/serverless-stack) - Serverless Stack Toolkit (SST) (extension of AWS CDK)
- [kolomied/awesome-cdk](https://github.com/kolomied/awesome-cdk) - Awesome CDK

---
## Useful Articles and Blog Posts

- [Bootstrapping multiple AWS accounts for AWS CDK using CloudFormation StackSets](https://aws.amazon.com/blogs/mt/bootstrapping-multiple-aws-accounts-for-aws-cdk-using-cloudformation-stacksets/), AWS, 2022-10-04
- [Manage application security and compliance with the AWS Cloud Development Kit and cdk-nag](https://aws.amazon.com/blogs/devops/manage-application-security-and-compliance-with-the-aws-cloud-development-kit-and-cdk-nag/), AWS, 2022-05-25
- [Testing CDK Applications in Any Language](https://aws.amazon.com/blogs/developer/testing-cdk-applications-in-any-language/), AWS, 2021-11-09
