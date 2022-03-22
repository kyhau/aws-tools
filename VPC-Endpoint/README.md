# Notes

## MLA

- Automate time series network visualizations for AWS PrivateLink using Amazon CloudWatch Contributor Insights ([blogpost](https://aws.amazon.com/blogs/mt/automate-time-series-network-visualizations-for-aws-privatelink-using-amazon-cloudwatch-contributor-insights/), AWS, 08 FEB 2022

## Gateway VPC Endpoint

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
