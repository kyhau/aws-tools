# Bedrock

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Agents for Amazon Bedrock](#agents-for-amazon-bedrock)
- [Knowledge Base](#knowledge-base)
- [Chunking](#chunking)
- [Guardrails](#guardrails)
- [Security and Access Control](#security-and-access-control)

## Useful Libs and Tools

- [Converse API](https://aws.amazon.com/about-aws/whats-new/2024/05/amazon-bedrock-new-converse-api/)
- [powertools-lambda-python](https://github.com/aws-powertools/powertools-lambda-python) - Powertools for AWS Lambda (Python) adds support for Agents for Amazon Bedrock ([2024.05](https://aws.amazon.com/about-aws/whats-new/2024/05/powertools-aws-lambda-python-support-agents-bedrock/))
- https://github.com/aws-samples/genai-messaging-hotel-assistant
- https://github.com/aws-samples/serverless-rag-demo/tree/main/infrastructure
- https://subaud.io/blog/cdk-bedrock-knowledge-base
- Bedrock, LangChain, RAG (Retrieval Augmented Generation), streamlit

## Agents for Amazon Bedrock

- [Knowledge Bases for Amazon Bedrock now supports advanced RAG capabilities](https://aws.amazon.com/about-aws/whats-new/2024/07/knowledge-bases-amazon-bedrock-advanced-rag-capabilities/), 2024-07
    - Custom chunking. With this, customers can write their own chunking code as a Lambda function, and even use off the shelf components from frameworks like LangChain and LlamaIndex.
    - Built-in chunking options such as semantic and hierarchical chunking.
- [Agents for Amazon Bedrock now retain memory (Preview)](https://aws.amazon.com/about-aws/whats-new/2024/07/agents-amazon-bedrock-retain-memory-preview/), AWS, 2024-07
- [Agents for Amazon Bedrock now support code interpretation (Preview)](https://aws.amazon.com/about-aws/whats-new/2024/07/agents-amazon-bedrock-code-interpretation-preview/), AWS, 2024-07

## Knowledge Base

Knowledge Bases for Amazon Bedrock is a fully managed Retrieval-Augmented Generation (RAG) capability that allows you to connect foundation models (FMs) to internal company data sources to deliver relevant and accurate responses.

- Data Sources
    - S3 buckets
    - Supports the web data source allowing you to index public web pages.
    - Atlassian Confluence
    - Microsoft SharePoint, and
    - Salesforce.

- Using Knowledge base
    1. AWS SDK/CLI - `Retrieve` and `RetrieveAndGenerate`
    2. Opensource LangChain - Bedrock integration
    3. Agent for Bedrock

- Knowledge Bases now supports observability, offering log delivery choice through CloudWatch, S3 buckets, and Firehose streams. This capability provides enhanced visibility and timely insights into the execution of knowledge ingestion steps.

# Chunking

- How content chunking and parsing works for Amazon Bedrock knowledge bases ([link](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html))
    - Standard chunking
    - Hierarchical chunking
    - Semantic chunking
    - Advanced parsing options
    - Custom transformation

## Guardrails

- [Guardrails for Amazon Bedrock can now detect hallucinations and safeguard apps built using custom or third-party FMs](https://aws.amazon.com/blogs/aws/guardrails-for-amazon-bedrock-can-now-detect-hallucinations-and-safeguard-apps-built-using-custom-or-third-party-fms/), AWS, 2024-07


## Security and Access Control

- [Private network for data movement in generative AI](https://aws.amazon.com/blogs/networking-and-content-delivery/private-network-for-data-movement-in-generative-ai/), AWS, 2024-07-16
