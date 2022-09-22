# Bottlerocket Notes

Jump to
- [CDK/CloudFormation examples for demo](#cdkcloudformation-examples-for-demo)
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Bottlerocket Security](#bottlerocket-security)
    - Reduced attack surface, verified software, enforced permission boundaries
    - ECS/EBS encryption vs. OS crypto
    - CIS Hardening Benchmark for Bottlerocket
    - FIPS Support / Validation
    - Does Bottlerocket have integration with AWS Inspector?
    - Is OS host logs available? Does it have integration with CloudWatch Log?
- [Bottlerocket AMIs and Containers](#bottlerocket-amis-and-containers)
    - Bottlerocket AMIs optimized for ECS and EKS
    - Bottlerocket AMI update frequency
    - Updates and reboots (how much memory does it need?)
- [Bottlerocket vs. Fargate](#bottlerocket-vs-fargate)
- [Using Bottlerocket with or without a container orchestrator?](#using-bottlerocket-with-or-without-a-container-orchestrator)
- ["No pod metric collected" error when using Bottlerocket for EKS](#no-pod-metric-collected-error-when-using-bottlerocket-for-eks)


---
## CDK/CloudFormation examples for demo
- https://github.com/kyhau/bottlerocket-ecs-cdk


---
## Useful Libs and Tools

- Update Bottlerocket https://github.com/bottlerocket-os/bottlerocket#updates
- ECS
    - [ECS-optimized Bottlerocket AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-bottlerocket.html)
    - [bottlerocket-ecs-updater](https://github.com/bottlerocket-os/bottlerocket-ecs-updater) - Bottlerocket ECS Updater is a service you can install into your ECS cluster that helps you keep your Bottlerocket container instances up to date.
    - [adamjkeller/bottlerocket-ecs-updater-cdk](https://github.com/adamjkeller/bottlerocket-ecs-updater-cdk) - deploy a demo container to Amazon ECS using Bottlerocket OS for the compute. In addition, a construct was created for the Bottlerocket updater based off of the CFN template required to deploy it.
- EKS
    - [EKS-optimized Bottlerocket AMIs](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami-bottlerocket.html)
    - [bottlerocket-update-operator](https://github.com/bottlerocket-os/bottlerocket-update-operator) - Bottlerocket update operator is a Kubernetes operator that coordinates Bottlerocket updates on hosts in a cluster.
    - [aws-samples/amazon-eks-bottlerocket-nodes-on-graviton2](https://github.com/aws-samples/amazon-eks-bottlerocket-nodes-on-graviton2) - deploy a EKS cluster composed of two Managed Node Groups, one configured with x86-based and the other with Graviton2-based EC2 instance type, both of which utilize Bottlerocket-based AMI.


---
## Useful Articles and Blogs

- [Using a Bottlerocket AMI with Amazon ECS](https://github.com/bottlerocket-os/bottlerocket/blob/develop/QUICKSTART-ECS.md)
- https://aws.amazon.com/blogs/containers/bottlerocket-a-year-in-the-life/
- Quick Start
    - https://aws.amazon.com/blogs/containers/getting-started-with-bottlerocket-and-amazon-ecs/
    - https://github.com/bottlerocket-os/bottlerocket/blob/develop/QUICKSTART-ECS.md
- [Bottlerocket Security Guidance](https://github.com/bottlerocket-os/bottlerocket/blob/develop/SECURITY_GUIDANCE.md)
- [Bottlerocket Packages](https://github.com/bottlerocket-os/bottlerocket/tree/develop/packages)
- [Bottlerocket Public Roadmap](https://github.com/orgs/bottlerocket-os/projects/1)


---
## Bottlerocket Security

### Reduced attack surface, verified software, enforced permission boundaries

- Bottlerocket contains less software, and notably eliminates some components you might expect: **Bottlerocket doesn’t have SSH, any interpreters like Python, or even a shell**; it is expected that Bottlerocket to be "hands-off" most of the time, and removing components like this makes it harder for an attacker to gain a foothold in the system. Beyond removal of software, Bottlerocket also reduces the attack surface of the operating system by applying software hardening techniques like:
    - building **position-independent executables (PIE)**,
    - using **relocation read-only (RELRO) linking**, and
    - building all **first-party software with memory-safe languages like Rust and Go**.
- Bottlerocket uses [SELinux](https://github.com/SELinuxProject) in enforcing mode to restrict modifications to itself even from privileged containers. SELinux is an implementation of Mandatory Access Control (MAC) enforced by the Linux kernel, and **limits the set of actions processes can take**. Today, Bottlerocket’s SELinux policy is intended to restrict orchestrated containers from causing undesired and unexpected changes to the operating system. Going forward, we want to extend this policy to apply to all categories of persistent threats.

See
- Blog post: https://aws.amazon.com/blogs/containers/bottlerocket-a-special-purpose-container-operating-system/
- [Bottlerocket Packages](https://github.com/bottlerocket-os/bottlerocket/tree/develop/packages)

### ECS/EBS encryption vs. OS crypto

#### Bottlerocket operates with 2 default storage volumes - standard EBS encryption applicable

- The root device, holds the active and passive partition sets. It also contains the `bootloader`, the `dm-verity` hash tree for verifying the immutable root filesystem, and the data store for the Bottlerocket API.
- The data device is used as persistent storage for container images, container orchestration, host-containers, and bootstrap containers.

#### Bottlerocket cryptographically verifies itself

The operating system is composed of a disk image that is verified on boot with dm-verity; unexpected changes to the contents of the disk image will cause the operating system to fail to boot.

Bottlerocket uses its own software updater rather than a more common Linux package manager. Updates to Bottlerocket are vended from a repository that follows The Update Framework (TUF) specification; TUF mitigates common classes of attacks against software repositories present in traditional package manager systems.

Source: https://aws.amazon.com/blogs/containers/bottlerocket-a-special-purpose-container-operating-system/

### CIS Hardening Benchmark for Bottlerocket

Bottlerocket now has a Center for Internet Security (CIS) Benchmark. The CIS Benchmark is a catalog of security-focused configuration settings that help Bottlerocket customers configure or document any non-compliant configurations in a simple and efficient manner. The CIS Benchmark for Bottlerocket includes both Level 1 and Level 2 configuration profiles.

See also https://github.com/bottlerocket-os/bottlerocket/issues/1297

### FIPS Support / Validation

Issue (Open): https://github.com/bottlerocket-os/bottlerocket/issues/1667

> FIPS compliance is our second most requested feature, behind CIS (which is in progress), and I'm planning to focus on it once the CIS benchmark is complete.

### Does Bottlerocket have integration with AWS Inspector?

Coming Soon - Issue (Open) https://github.com/bottlerocket-os/bottlerocket/issues/2056

> We're working with the AWS Inspector team to add first-class support for Bottlerocket - meaning that its vulnerability scan would be aware of our security advisories and flag nodes that are not running versions of Bottlerocket that contain the fix.
> It's tentatively slotted into the 1.10.0 release, roughly August.

### Is OS host logs available? Does it have integration with CloudWatch Log?

No. There is no current plan to add a logging agent to the host OS.

Issue (Open) https://github.com/bottlerocket-os/bottlerocket/issues/850

Comments from Maintainers:

> We have no current plans to add a logging agent to the host OS.

> When talking with many EKS customers, we found that a common pattern is to use Kubernetes’ facilities for log streaming, even for system level logs. Another method is to use Fluent Bit as covered in this blog post. These are our suggested methods for customers to get both container logs as well as other logs off the box.


---
## Bottlerocket AMIs and Containers

### Bottlerocket AMIs optimized for ECS and EKS

- [Amazon ECS-optimized Bottlerocket AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-bottlerocket.html)
    - Standard: `aws-ecs-1/x86_64`, `aws-ecs-1/arm64`
    - NVIDIA: `aws-ecs-1-nvidia/x86_64`, `aws-ecs-1-nvidia/arm64`
- [Amazon EKS-optimized Bottlerocket AMIs](https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami-bottlerocket.html) for Kubernetes version (1.22, 1.21, 1.20, 1.19, 1.18)
    - Standard: `aws-k8s-1.22/x86_64`, `aws-k8s-1.22/arm64`
    - NVIDIA: `aws-k8s-1.22-nvidia/x86_64`, `aws-k8s-1.22-nvidia/arm64`

### Bottlerocket AMI update frequency

Non-regular releases.

You can find the release versions and Changelog from
- GitHub Bottlerocket [Releases](https://github.com/bottlerocket-os/bottlerocket/releases) and [Bottlerocket Tags](https://github.com/bottlerocket-os/bottlerocket/tags), or
- AWS SSM console > Parameter Store > Public parameters > select "bottlerocket" in the drop down list.

See also [Enable automatic updates](https://github.com/bottlerocket-os/bottlerocket/blob/develop/SECURITY_GUIDANCE.md#enable-automatic-updates).

### Updates and reboots (how much memory does it need?)

- ECS in-place update and reboot - memory usage test
    - E.g. Instance type: t3.large (2 vCPUs, 8 GiB memory)
    - No (or insignificant) memory usage during "downloading and applying update to disk".
    - Lost the terminal session. But can connect to terminal immediately
    - Instance state remains Running (at least it’s showing Running after refresh the console).
    - Instance status check remains 2/2 checks passed.
- ECS auto update
    - See also [Enable automatic updates](https://github.com/bottlerocket-os/bottlerocket/blob/develop/SECURITY_GUIDANCE.md#enable-automatic-updates).
    - The Bottlerocket ECS Updater attempts to update container instances without disrupting the workloads in your cluster. Applying an update to Bottlerocket requires a reboot. To avoid disruption in your cluster, the Bottlerocket ECS Updater uses the container instance draining feature of ECS. A container instance may be skipped for update when:
    - See also https://aws.amazon.com/blogs/containers/a-deep-dive-into-bottlerocket-ecs-updater/
- EKS auto update
    - https://github.com/bottlerocket-os/bottlerocket-update-operator

---
## Bottlerocket vs. Fargate

**Fargate utilizes VM level isolation, while Bottlerocket aims to make container-level isolation safer**. But we are designing Bottlerocket for all types of workloads that need a secure host for multiple containers: both internal workloads as well as end customer workloads. ([Source](https://twitter.com/nathankpeck/status/1414613664267653120))

## Using Bottlerocket with or without a container orchestrator?

> We actually launched Bottlerocket for EKS first, before Bottlerocker for ECS. You could theoretically use Bottlerocket without a container orchestrator but it wouldn't be easy. It's designed to be used with container orchestration.

([Source](https://twitter.com/nathankpeck/status/1414613664267653120))

---
## "No pod metric collected" error when using Bottlerocket for EKS

Bottlerocket is a Linux-based open source operating system that is purpose-built by AWS for running containers. Bottlerocket uses a different containerd path on the host, so you need to change the volumes to its location. If you don't, you see an error in the logs that includes W! No pod metric collected. See the following example: ([Source](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights-troubleshooting.html))
