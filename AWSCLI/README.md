# AWS CLI

You can add additional "model" to aws cli with https://docs.aws.amazon.com/cli/latest/reference/configure/add-model.html.
The model will be added to ~/.aws/model/

If you need to use the same model with boto3, you will need to have the model available in botocore/data/.

See also
- https://github.com/aws/aws-cli/issues/2790
- https://github.com/boto/botocore/blob/cac78632cabddbc7b64f63d99d419fe16917e09b/botocore/loaders.py#L33
- https://stackoverflow.com/questions/63512015/boto3-load-custom-models

E.g. https://boto3.amazonaws.com/v1/documentation/api/1.9.56/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_provisioned_capacity
