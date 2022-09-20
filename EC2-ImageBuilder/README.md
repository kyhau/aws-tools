# ImageBuilder Notes

- [Gotchas](#gotchas)
    - [Gotchas - AWS::ImageBuilder::ContainerRecipe](#gotchas---awsimagebuildercontainerrecipe)
- [Useful Templates](#useful-templates)

---
## Gotchas

- If something is not right at early stage (e.g. parse file in Component Data) => `Internal Failure` in CDN console, but not log in S3 nor CW Logs.

- CloudWatch Logs - `/aws/imagebuilder/${ImageName}`
	- Logging things happen in the EC2 instance of the build only
	- Not for Component Data syntax error, Version conflict

- Tags are not inherited from CFN stack for all ImageBuilder resources (Component, Image Recipe / Container Recipe, Infrastructure configuration, Distribution, Image Pipeline)

- Adding, removing, renaming Tags, need to change Version; otherwise `Internal Failure` will be shown in CFN console, nothing in S3 log nor CW logs. Also need to update upstream resource's version e.g. Recipe Version.

- Separating Component and Recipe in different templates?
	- ARN includes build number: `arn:aws:imagebuilder:ap-southeast-2:123456789012:component/git/1.0.1/1`
	- Use [semantic versioning](https://docs.aws.amazon.com/imagebuilder/latest/userguide/ibhow-semantic-versioning.html)

- Whenever a change to Recipe (include Git Component)
    - Build time ~30 mins

### Gotchas - AWS::ImageBuilder::ContainerRecipe

- In `AWS::ImageBuilder::ContainerRecipe`, `Parameters` is supported only from Console and AWS CLI, but not from CloudFormation.

- In `AWS::ImageBuilder::ContainerRecipe`, `ParentImage` (or `Base image` in Console) cannot reference in another AWS account's ECR repo - this is not mentioned in [AWS documentation](https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-container-recipes.html). Confirmed with AWS support.


---
## Useful Templates
- [aws-samples/amazon-ec2-image-builder-samples](https://github.com/aws-samples/amazon-ec2-image-builder-samples)
- [aws-samples/build-and-deploy-docker-images-to-aws-using-ec2-image-builder](https://github.com/aws-samples/build-and-deploy-docker-images-to-aws-using-ec2-image-builder/)
