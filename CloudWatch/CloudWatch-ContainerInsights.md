# Container Insights

The Container Insights setup process is different for **Amazon ECS** and **Amazon EKS and Kubernetes**. 

- [Setting Up Container Insights on Amazon ECS](
  https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-ECS.html)
- [Setting Up Container Insights on Amazon EKS and Kubernetes](
  https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-EKS.html)

(Last updated on 2019-11-05)

1. You can enable Container Insights on existing Amazon ECS clusters and on new clusters that you create. 
2. For existing clusters, you use the AWS CLI. For new clusters, use either the Amazon ECS console or the AWS CLI.
3. If you're using Amazon ECS on an Amazon EC2 instance, to collect network and storage metrics from Container Insights
   you must launch that instance using an AMI that includes Amazon ECS agent version 1.29. 
4. Currently, you can't enable Container Insights when you use AWS CloudFormation to create a new cluster. 
   As a workaround, you can use the AWS CLI to set account-level permission to enable Container Insights for any new
   Amazon ECS clusters created in your account. To do so, enter the following command: 
   `aws ecs put-account-setting --name "containerInsights" --value "enabled"`
5. To enable Container Insights on an existing Amazon ECS cluster, you must be running version 1.16.200 or later of 
   the AWS CLI:  
   `aws ecs update-cluster-settings --cluster myCICluster --settings name=containerInsights,value=enabled`

