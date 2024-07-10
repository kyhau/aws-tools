# OpenSearch Service

- [SQL Support for Amazon Elasticsearch Service](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/sql-support.html)
   - [Workbench](https://opendistro.github.io/for-elasticsearch-docs/docs/sql/workbench/)
   - [SQL CLI](https://opendistro.github.io/for-elasticsearch-docs/docs/sql/cli/)
- [Cross-Cluster Search for Amazon Elasticsearch Service](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/cross-cluster-search.html)

## OpenSearch Serverless

### Private Access
- To specify private access, include one or both of the following elements:
    - SourceVPCEs – Specify one or more OpenSearch Serverless–managed VPC endpoints.
    - SourceServices – Specify the identifier of one or more supported AWS services. Currently, the following service identifiers are supported:
      - `bedrock.amazonaws.com` – Amazon Bedrock
   - For examples see https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html#serverless-network-cli