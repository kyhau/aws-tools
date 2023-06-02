# ECR

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Image Scanning](#image-scanning)
- [Pull Through Cache](#pull-through-cache)


---
## Useful Libs and Tools

- [awslabs/amazon-ecr-credential-helper](https://github.com/awslabs/amazon-ecr-credential-helper) - Amazon ECR Docker Credential Helper
- [gallery.ecr.aws](https://gallery.ecr.aws/) - Amazon ECR Public Gallery


---
## Useful Articles and Blogs


---
## Image Scanning
https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html

```
# Configure an existing repository to Scan on Push
aws ecr put-image-scanning-configuration --repository-name name --image-scanning-configuration scanOnPush=true --region ap-southeast-2

# Create a repository configured for scan on push
aws ecr create-repository --repository-name name --image-scanning-configuration scanOnPush=true --region ap-southeast-2

# Start image scan
aws ecr start-image-scan --repository-name name --image-id imageTag=tag_name --region ap-southeast-2

aws ecr start-image-scan --repository-name name --image-id imageDigest=sha256_hash --region ap-southeast-2

# Retrieve image scan findings
aws ecr describe-image-scan-findings --repository-name name --image-id imageTag=tag_name --region ap-southeast-2

aws ecr describe-image-scan-findings --repository-name name --image-id imageDigest=sha256_hash --region ap-southeast-2
```


---
## Pull Through Cache

ECR currently supports creating pull through cache rules for
- ECR Public ([ECR Public Gallery](https://gallery.ecr.aws/));
- Quay (Red Hat [Quay.io](http://quay.io/)); and
- Kubernetes container image registry ([registry.k8s.io](https://github.com/kubernetes/registry.k8s.io)).

in which Docker Official Images are [available](https://aws.amazon.com/blogs/containers/docker-official-images-now-available-on-amazon-elastic-container-registry-public/) on ECR Public (only the images labelled with DOCKER OFFICIAL IMAGE; e.g. [node](https://hub.docker.com/_/node)).
