"""
aws configservice list-discovered-resources ---resource-type ##

See also _multi_services/list_resources_with_resourcegroupstaggingapi.py
"""
import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.CRITICAL)

# See https://docs.aws.amazon.com/config/latest/APIReference/API_ListDiscoveredResources.html
RESOURCE_TYPES = """
AWS::EC2::CustomerGateway | AWS::EC2::EIP | AWS::EC2::Host | AWS::EC2::Instance | AWS::EC2::InternetGateway |
AWS::EC2::NetworkAcl | AWS::EC2::NetworkInterface | AWS::EC2::RouteTable | AWS::EC2::SecurityGroup |
AWS::EC2::Subnet | AWS::CloudTrail::Trail | AWS::EC2::Volume | AWS::EC2::VPC | AWS::EC2::VPNConnection |
AWS::EC2::VPNGateway | AWS::EC2::RegisteredHAInstance | AWS::EC2::NatGateway | AWS::EC2::EgressOnlyInternetGateway |
AWS::EC2::VPCEndpoint | AWS::EC2::VPCEndpointService | AWS::EC2::FlowLog | AWS::EC2::VPCPeeringConnection |
AWS::Elasticsearch::Domain | AWS::IAM::Group | AWS::IAM::Policy | AWS::IAM::Role | AWS::IAM::User |
AWS::ElasticLoadBalancingV2::LoadBalancer | AWS::ACM::Certificate | AWS::RDS::DBInstance | AWS::RDS::DBSubnetGroup |
AWS::RDS::DBSecurityGroup | AWS::RDS::DBSnapshot | AWS::RDS::DBCluster | AWS::RDS::DBClusterSnapshot |
AWS::RDS::EventSubscription | AWS::S3::Bucket | AWS::S3::AccountPublicAccessBlock | AWS::Redshift::Cluster |
AWS::Redshift::ClusterSnapshot | AWS::Redshift::ClusterParameterGroup | AWS::Redshift::ClusterSecurityGroup |
AWS::Redshift::ClusterSubnetGroup | AWS::Redshift::EventSubscription | AWS::SSM::ManagedInstanceInventory |
AWS::CloudWatch::Alarm | AWS::CloudFormation::Stack | AWS::ElasticLoadBalancing::LoadBalancer |
AWS::AutoScaling::AutoScalingGroup | AWS::AutoScaling::LaunchConfiguration | AWS::AutoScaling::ScalingPolicy |
AWS::AutoScaling::ScheduledAction | AWS::DynamoDB::Table | AWS::CodeBuild::Project | AWS::WAF::RateBasedRule |
AWS::WAF::Rule | AWS::WAF::RuleGroup | AWS::WAF::WebACL | AWS::WAFRegional::RateBasedRule | AWS::WAFRegional::Rule |
AWS::WAFRegional::RuleGroup | AWS::WAFRegional::WebACL | AWS::CloudFront::Distribution |
AWS::CloudFront::StreamingDistribution | AWS::Lambda::Function | AWS::ElasticBeanstalk::Application |
AWS::ElasticBeanstalk::ApplicationVersion | AWS::ElasticBeanstalk::Environment | AWS::WAFv2::WebACL |
AWS::WAFv2::RuleGroup | AWS::WAFv2::IPSet | AWS::WAFv2::RegexPatternSet | AWS::WAFv2::ManagedRuleSet |
AWS::XRay::EncryptionConfig | AWS::SSM::AssociationCompliance | AWS::SSM::PatchCompliance | AWS::Shield::Protection |
AWS::ShieldRegional::Protection | AWS::Config::ResourceCompliance | AWS::ApiGateway::Stage | AWS::ApiGateway::RestApi |
AWS::ApiGatewayV2::Stage | AWS::ApiGatewayV2::Api | AWS::CodePipeline::Pipeline |
AWS::ServiceCatalog::CloudFormationProvisionedProduct | AWS::ServiceCatalog::CloudFormationProduct |
AWS::ServiceCatalog::Portfolio | AWS::SQS::Queue | AWS::KMS::Key | AWS::QLDB::Ledger
"""


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        """Process request for a region of an account"""
        client = session.client("config", region_name=region)

        for resource_type in list(map(str.strip, RESOURCE_TYPES.split("|"))):
            for item in self.paginate(client, "list_discovered_resources", {"resourceType": resource_type}):
                print(item)


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(profile, region):
    Helper().start(profile, region, "config")


if __name__ == "__main__":
    main()
