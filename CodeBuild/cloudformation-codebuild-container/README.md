## Build container images using AWS CloudFormation

Original Source: 
https://github.com/aws-quickstart/quickstart-examples/tree/develop/samples/cloudformation-codebuild-container

See also blog: 
https://aws.amazon.com/blogs/infrastructure-and-automation/using-a-long-lived-compute-resource-as-a-custom-resource-in-aws-cloudformation/

This stack uses CloudFormation and Custom Lambda-backed resource to run a CodeBuild project, creating a Docker
 container image and uploading it to ECR.

![Overview](
https://github.com/aws-quickstart/quickstart-examples/tree/develop/samples/cloudformation-codebuild-container/overview.png)

