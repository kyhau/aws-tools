import click
from boto3.session import Session

# See https://docs.aws.amazon.com/config/latest/APIReference/API_ListDiscoveredResources.html
RESOURCE_TYPES_STR = "AWS::EC2::CustomerGateway | AWS::EC2::EIP | AWS::EC2::Host | AWS::EC2::Instance | AWS::EC2::InternetGateway | AWS::EC2::NetworkAcl | AWS::EC2::NetworkInterface | AWS::EC2::RouteTable | AWS::EC2::SecurityGroup | AWS::EC2::Subnet | AWS::CloudTrail::Trail | AWS::EC2::Volume | AWS::EC2::VPC | AWS::EC2::VPNConnection | AWS::EC2::VPNGateway | AWS::EC2::RegisteredHAInstance | AWS::EC2::NatGateway | AWS::EC2::EgressOnlyInternetGateway | AWS::EC2::VPCEndpoint | AWS::EC2::VPCEndpointService | AWS::EC2::FlowLog | AWS::EC2::VPCPeeringConnection | AWS::Elasticsearch::Domain | AWS::IAM::Group | AWS::IAM::Policy | AWS::IAM::Role | AWS::IAM::User | AWS::ElasticLoadBalancingV2::LoadBalancer | AWS::ACM::Certificate | AWS::RDS::DBInstance | AWS::RDS::DBSubnetGroup | AWS::RDS::DBSecurityGroup | AWS::RDS::DBSnapshot | AWS::RDS::DBCluster | AWS::RDS::DBClusterSnapshot | AWS::RDS::EventSubscription | AWS::S3::Bucket | AWS::S3::AccountPublicAccessBlock | AWS::Redshift::Cluster | AWS::Redshift::ClusterSnapshot | AWS::Redshift::ClusterParameterGroup | AWS::Redshift::ClusterSecurityGroup | AWS::Redshift::ClusterSubnetGroup | AWS::Redshift::EventSubscription | AWS::SSM::ManagedInstanceInventory | AWS::CloudWatch::Alarm | AWS::CloudFormation::Stack | AWS::ElasticLoadBalancing::LoadBalancer | AWS::AutoScaling::AutoScalingGroup | AWS::AutoScaling::LaunchConfiguration | AWS::AutoScaling::ScalingPolicy | AWS::AutoScaling::ScheduledAction | AWS::DynamoDB::Table | AWS::CodeBuild::Project | AWS::WAF::RateBasedRule | AWS::WAF::Rule | AWS::WAF::RuleGroup | AWS::WAF::WebACL | AWS::WAFRegional::RateBasedRule | AWS::WAFRegional::Rule | AWS::WAFRegional::RuleGroup | AWS::WAFRegional::WebACL | AWS::CloudFront::Distribution | AWS::CloudFront::StreamingDistribution | AWS::Lambda::Function | AWS::NetworkFirewall::Firewall | AWS::NetworkFirewall::FirewallPolicy | AWS::NetworkFirewall::RuleGroup | AWS::ElasticBeanstalk::Application | AWS::ElasticBeanstalk::ApplicationVersion | AWS::ElasticBeanstalk::Environment | AWS::WAFv2::WebACL | AWS::WAFv2::RuleGroup | AWS::WAFv2::IPSet | AWS::WAFv2::RegexPatternSet | AWS::WAFv2::ManagedRuleSet | AWS::XRay::EncryptionConfig | AWS::SSM::AssociationCompliance | AWS::SSM::PatchCompliance | AWS::Shield::Protection | AWS::ShieldRegional::Protection | AWS::Config::ConformancePackCompliance | AWS::Config::ResourceCompliance | AWS::ApiGateway::Stage | AWS::ApiGateway::RestApi | AWS::ApiGatewayV2::Stage | AWS::ApiGatewayV2::Api | AWS::CodePipeline::Pipeline | AWS::ServiceCatalog::CloudFormationProvisionedProduct | AWS::ServiceCatalog::CloudFormationProduct | AWS::ServiceCatalog::Portfolio | AWS::SQS::Queue | AWS::KMS::Key | AWS::QLDB::Ledger | AWS::SecretsManager::Secret | AWS::SNS::Topic | AWS::SSM::FileData | AWS::Backup::BackupPlan | AWS::Backup::BackupSelection | AWS::Backup::BackupVault | AWS::Backup::RecoveryPoint | AWS::ECR::Repository | AWS::ECS::Cluster | AWS::ECS::Service | AWS::ECS::TaskDefinition | AWS::EFS::AccessPoint | AWS::EFS::FileSystem | AWS::EKS::Cluster | AWS::OpenSearch::Domain | AWS::EC2::TransitGateway | AWS::Kinesis::Stream | AWS::Kinesis::StreamConsumer | AWS::CodeDeploy::Application | AWS::CodeDeploy::DeploymentConfig | AWS::CodeDeploy::DeploymentGroup | AWS::EC2::LaunchTemplate | AWS::ECR::PublicRepository | AWS::GuardDuty::Detector | AWS::EMR::SecurityConfiguration | AWS::SageMaker::CodeRepository | AWS::Route53Resolver::ResolverEndpoint | AWS::Route53Resolver::ResolverRule | AWS::Route53Resolver::ResolverRuleAssociation | AWS::DMS::ReplicationSubnetGroup | AWS::DMS::EventSubscription | AWS::MSK::Cluster | AWS::StepFunctions::Activity | AWS::WorkSpaces::Workspace | AWS::WorkSpaces::ConnectionAlias | AWS::SageMaker::Model | AWS::ElasticLoadBalancingV2::Listener | AWS::StepFunctions::StateMachine | AWS::Batch::JobQueue | AWS::Batch::ComputeEnvironment | AWS::AccessAnalyzer::Analyzer | AWS::Athena::WorkGroup | AWS::Athena::DataCatalog | AWS::Detective::Graph | AWS::GlobalAccelerator::Accelerator | AWS::GlobalAccelerator::EndpointGroup | AWS::GlobalAccelerator::Listener | AWS::EC2::TransitGatewayAttachment | AWS::EC2::TransitGatewayRouteTable | AWS::DMS::Certificate"
RESOURCE_TYPES = sorted(list(map(str.strip, RESOURCE_TYPES_STR.split("|"))))


@click.command()
@click.option("--ls", "-l", is_flag=True, help="List all resource types", show_default=True)
@click.option("--resource-type", "-t", help="Resource type, e.g. AWS::IAM::Policy")
@click.option("--profile", "-p", default="default", help="AWS profile name", show_default=True)
@click.option("--region", "-r", default="ap-southeast-2", help="AWS Region", show_default=True)
def main(ls, resource_type, profile, region):
    if ls:
        print("\n".join(RESOURCE_TYPES))
        return

    if resource_type:
        if resource_type not in RESOURCE_TYPES:
            print(f"ERROR: Invalid resource type ({resource_type}) specified")
            return

        client = Session(profile_name=profile).client("config", region_name=region)
        for page in client.get_paginator("list_discovered_resources").paginate(resourceType=resource_type).result_key_iters():
            for item in page:
                print(item)


if __name__ == "__main__":
    main()
