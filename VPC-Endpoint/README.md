# VPC Endpoints

Jump to
- [MLA](#mla)
- [Gateway VPC endpoint](#gateway-vpc-endpoint)
- [Interface VPC endpoint (powered by AWS PrivateLink)](#interface-vpc-endpoint-powered-by-aws-privatelink)
- [Gateway Load Balancer endpoint (GWLBe) (powered by AWS PrivateLink)](#gateway-load-balancer-endpoint-gwlbe-powered-by-aws-privatelink)

---
And
- **DNS resolution** is required within the VPC.
- If a Lambda function needs to access both VPC resources and the public internet, the VPC needs to have a **NAT gateway** in a **public subnet**.

## MLA

- Automate time series network visualizations for AWS PrivateLink using Amazon CloudWatch Contributor Insights ([blogpost](https://aws.amazon.com/blogs/mt/automate-time-series-network-visualizations-for-aws-privatelink-using-amazon-cloudwatch-contributor-insights/), AWS, 08 FEB 2022


## Gateway VPC endpoint

- Use DynamoDB/S3 public IP addresses
- Do not allow access from on premises
- Do not allow access from another AWS Region
- Not billed
- Region specific (need to be in the same region); support IPv4 only.
- Attach Endpoint policy; not Security Group.
- Prefix list ID: `pl-xxxxxxx`; Prefix list name: `com.amazonaws.us-east-1.s3`
- Subnet route table: `Destination: pl-id-for-s3, Target: vpce-id`

### Gateway VPC Endpoint for S3

1. Attach an **Endpoint Policy** to the endpoint to limit its functionality.
2. Add a **route** in the route tables for any subnets where the gateway will be used.
    - Subnet route table:  `Destination: pl-id-for-s3, Target: vpce-id`
3. Use **bucket policies** to control access to buckets from specific endpoints, or specific VPCs.

### More
- A VPC can have more than one DynamoDB (or S3) Gateway VPC endpoint.
    - A VPC endpoint supports an [MTU of 8500 bytes](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-limits-endpoints.html). Packets with a size larger than 8500 bytes that arrive at the VPC endpoint are dropped.
    - You can create multiple VPC endpoints - each associates to different route table (a route table can only have one DynamoDB VPC endpoint's prefix list).
- Access Control
    1. VPC endpoint policies
        - https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-ddb.html
    2. Security group
        - Only if the security group associated with the EC2 instance restricts outbound traffic
        - > For a gateway endpoint, if your security group's outbound rules are restricted, you must add a rule that allows outbound traffic from your VPC to the service that's specified in your endpoint. To do this, you can use the service's AWS prefix list ID as the destination in the outbound rule.
        - https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-access.html
    3. IAM policy


## Interface VPC endpoint (powered by AWS PrivateLink)

- Use private IP addresses from your VPC to access DynamoDB/S3
- Allow access from on premises
- Allow access from an Amazon VPC endpoint in another AWS Region by using Amazon VPC peering or AWS Transit Gateway
- Billed
- AZ specific
- Through IGW (not using Interface Endpoint): DNS `sns.us-east-1.amazonaws.com, public IP`
- Using Interface Endpoint: DNS `vpce-<id>.sns.<region>.amazonaws.com, private IP`
- Using Interface Endpoint with Private DNS Name: DNS `sns.us-east-1.amazonaws.com, private IP`
- To use private DNS names,
    - Enable `Private DNS Name` (when creating new Interface VPC Endpoint)
    - Set `VPC settings to true: enableDnsHostnames, enableDnsSupport`.

## Gateway Load Balancer endpoint (GWLBe) (powered by AWS PrivateLink)

- A VPC endpoint that provides private connectivity between virtual appliances in the service provider VPC and application servers in the service consumer VPC.
- Traffic to and from a GWLBe is configured using route tables.
- Traffic flows from the service consumer VPC over the GWLBe to the GWLB in the service provider VPC, and then returns to the service consumer VPC.
- You must create the GWLBe and the application servers in different subnets. This enables you to configure the GWLBe as the next hop in the route table for the application subnet.

