# SQS notes

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)


---
## Useful Libs and Tools

- [awslabs/amazon-sqs-java-extended-client-lib](https://github.com/awslabs/amazon-sqs-java-extended-client-lib) - useful for storing and retrieving messages with a message payload size greater than the current SQS limit of 256 KB, up to a maximum of 2 GB.
- [awslabs/amazon-sqs-python-extended-client-lib/](https://github.com/awslabs/amazon-sqs-python-extended-client-lib/) - useful for storing and retrieving messages with a message payload size greater than the current SQS limit of 256 KB, up to a maximum of 2 GB.


---
## Useful Articles and Blogs

- [Implementing AWS Well-Architected best practices for Amazon SQS](https://aws.amazon.com/blogs/compute/implementing-aws-well-architected-best-practices-for-amazon-sqs-part-1/), AWS, 2023-06-27
- [How to set up least privilege access to your encrypted Amazon SQS queue](https://aws.amazon.com/blogs/security/how-to-set-up-least-privilege-access-to-your-encrypted-amazon-sqs-queue/), AWS, 2023-03-03
    - Least-privilege key policy for SQS
    - Restrict message reception to a specific VPC endpoint (`DenyReceivingIfNotThroughVPCE`)
- [SQS and Lambda: the missing guide on failure modes](https://lumigo.io/blog/sqs-and-lambda-the-missing-guide-on-failure-modes/), Aug 14 2019
- [Avoiding insurmountable queue backlogs](https://d1.awsstatic.com/builderslibrary/pdfs/avoiding-insurmountable-queue-backlogs.pdf), 2019
