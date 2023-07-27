# Graviton

Jump to
- [AWS services that benefits from AWS Graviton](#aws-services-that-benefits-from-aws-graviton)
- [Instances Powered by Arm-based AWS Graviton Processors - **Sydney**](#instances-powered-by-arm-based-aws-graviton-processors---sydney)
- [Resources for getting started with AWS Graviton](#resources-for-getting-started-with-aws-graviton)


---
## AWS services that benefits from AWS Graviton

- Amazon EC2 - up to 40% better performance at up to 20% lower cost over comparable x86-based instances
- AWS Lambda - up to 19% better performance at 20% lower cost compared to x86
- AWS Fargate - up to 40% improved performance at 20% lower cost over comparable x86-based instances
- Amazon Aurora - up to 20% better performance at 20% lower cost over comparable x86-based instances
- Amazon RDS - up to 35% better performance at 20% lower cost over comparable x86-based instances
- Amazon Elasticache (Redis, Memcached) - up to 45% better performance at 20% lower cost over comparable x86-based instances
- Amazon EMR - up to 15% improved performance and up to 35% lower cost for Spark workloads versus comparable x86-based instances
- Amazon EKS - up to 40% better performance and 20% lower cost than comparable x86-based instances.
- Amazon OpenSearch Service - up to 30% better price-performance than comparable x86-based instances. (OpenSearch versions and Elasticsearch versions 7.9 and above)

See also [AWS Graviton Fast Start](https://aws.amazon.com/ec2/graviton/fast-start/) and [blog post](https://aws.amazon.com/blogs/aws/graviton-fast-start-a-new-program-to-help-move-your-workloads-to-aws-graviton/).


---
## Instances Powered by Arm-based AWS Graviton Processors - **Sydney**
Source [AWS Graviton](https://aws.amazon.com/ec2/graviton/) and [availability and pricing](https://aws.amazon.com/ec2/pricing/on-demand/) (last checked on 2022-12-22)

| | Instance types | Powered by | SYD | MEL | Built for
|--|--|--|--|--|--|
| General Purpose | M7g | AWS Graviton3 | Yes | No | General purpose workloads with balanced compute, memory, and networking|
| General Purpose | M7gd | AWS Graviton3 | No | No | General purpose workloads with balanced compute, memory, and networking|
| General Purpose | M6g, M6gd | AWS Graviton2 | Yes | No | General purpose workloads with balanced compute, memory, and networking|
| General Purpose | T4g | AWS Graviton2 | Yes | No | Burstable general purpose workloads|
| Compute Optimized | C7g | AWS Graviton3 | Yes | No | Compute-intensive workloads|
| Compute Optimized | C7gd | AWS Graviton3 | No | No | Compute-intensive workloads|
| Compute Optimized | C7gn | AWS Graviton3E | No | No | Compute-intensive workloads|
| Compute Optimized | C6g, C6gd, C6gn | AWS Graviton2 | Yes | No | Compute and network-intensive workloads, such as HPC, video encoding, gaming, and CPU-based ML inference.|
| Memory Optimized | R7g | AWS Graviton3 | Yes | No | Memory-intensive workloads such as open-source databases (MySQL, MariaDB, and PostgreSQL), or in-memory caches (Redis, KeyDB, Memcached).|
| Memory Optimized | R7gd | AWS Graviton3 | No | No | Memory-intensive workloads such as open-source databases (MySQL, MariaDB, and PostgreSQL), or in-memory caches (Redis, KeyDB, Memcached).|
| Memory Optimized | R6g, R6gd | AWS Graviton2 | Yes | No | Memory-intensive workloads such as open-source databases (MySQL, MariaDB, and PostgreSQL), or in-memory caches (Redis, KeyDB, Memcached).|
| Memory Optimized | X2gd | AWS Graviton2 | No | No | Lowest cost per GiB of memory in Amazon EC2|
| Storage Optimized | Im4gn | AWS Graviton2 | No | No | Storage-intensive workloads for databases|
| Storage Optimized | Is4gen | AWS Graviton2 | No | No | Lowest cost per TB of SSD storage in Amazon EC2|
| Accelerated Computing | G5g | AWS Graviton2 | No | No | Android game streaming |


---
## Resources for getting started with AWS Graviton

- [porting-advisor-for-graviton](https://github.com/aws/porting-advisor-for-graviton) - Porting Advisor for Graviton, an open source project by the ARM High Performance Computing group. Originally, it was coded as a Python module that analyzed some known incompatibilities for C and Fortran code.
- https://github.com/aws/aws-graviton-getting-started - This repository is meant to help new users start using the Arm-based AWS Graviton and Graviton2 processors which power the latest generation of Amazon EC2 instances. While it calls out specific features of the Graviton processors themselves, this repository is also **generically useful for anyone running code on Arm**.
- [Using Porting Advisor for Graviton](https://aws.amazon.com/blogs/compute/using-porting-advisor-for-graviton/), AWS, 2023-02-21
