# Bottlerocket Notes

Jump to
- [CDK/CloudFormation examples for demo](#cdkcloudformation-examples-for-demo)
- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Bottlerocket Security](#bottlerocket-security)
    - [Reduced attack surface of OS with less software and software hardening](#reduced-attack-surface-verified-software-enforced-permission-boundaries)
    - [Enable "kernel lockdown" to prevent attackers from adding kernel modules](#enable-kernel-lockdown-to-prevent-attackers-from-adding-kernel-modules)
    - [Use read-only root file system and dm-verity to prevent attackers from replacing files](#use-read-only-root-file-system-and-dm-verity-to-prevent-attackers-from-replacing-files)
    - [Use SELinux enforcing mode to provide permission boundaries and prevent unprivileged containers accessing resources on the system](#use-selinux-enforcing-mode-to-provide-permission-boundaries-and-prevent-unprivileged-containers-accessing-resources-on-the-system)
    - [Ephemeral storage for configuration](#ephemeral-storage-for-configuration)
    - [ECS/EBS encryption vs. OS crypto](#ecsebs-encryption-vs-os-crypto)
    - [CIS Hardening Benchmark for Bottlerocket](#cis-hardening-benchmark-for-bottlerocket)
    - [FIPS Support / Validation](#fips-support--validation)
    - [Does Bottlerocket have integration with AWS Inspector?](#does-bottlerocket-have-integration-with-aws-inspector)
    - [Is OS host logs available? Does it have integration with CloudWatch Log?](#is-os-host-logs-available-does-it-have-integration-with-cloudwatch-log)
    - [Watch for admin container launches](#watch-for-admin-container-launches)
    - [DO's and DONT's via the TOML config, and example of safe setup](#dos-and-donts-via-the-toml-config)
- [Bottlerocket AMIs and Containers](#bottlerocket-amis-and-containers)
    - Bottlerocket AMIs optimized for ECS and EKS
    - Bottlerocket AMI update frequency
    - Updates and reboots (how much memory does it need?)
- [Bottlerocket vs. Fargate](#bottlerocket-vs-fargate)
- [Using Bottlerocket with or without a container orchestrator?](#using-bottlerocket-with-or-without-a-container-orchestrator)
- ["No pod metric collected" error when using Bottlerocket for EKS](#no-pod-metric-collected-error-when-using-bottlerocket-for-eks)
- [Crowdstrike support](#crowdstrike-support)


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

The following is a summary. For details see
- [Bottlerocket Security Guidance](https://github.com/bottlerocket-os/bottlerocket/blob/develop/SECURITY_GUIDANCE.md)
- [Security features of Bottlerocket, an open source Linux-based operating system](https://aws.amazon.com/blogs/opensource/security-features-of-bottlerocket-an-open-source-linux-based-operating-system/)
- [Bottlerocket: a special-purpose container operating system](https://aws.amazon.com/blogs/containers/bottlerocket-a-special-purpose-container-operating-system/)

### Reduced attack surface, verified software, enforced permission boundaries

- **Bottlerocket contains less software**; doesn't have SSH, any interpreters like Python, or even a shell;
    - _It is expected that Bottlerocket to be "hands-off" most of the time_, and removing components like this makes it harder for an attacker to gain a foothold in the system.
- Bottlerocket also reduces the attack surface of the operating system by applying software hardening techniques like:
    - building **position-independent executables (PIE)**,
    - using **relocation read-only (RELRO) linking**, and
    - building all **first-party software with memory-safe languages** like Rust and Go.
- **Automatic OS updates** to Bottlerocket are applied as a **single unit which can be rolled back**, if necessary, which removes the risk of "botched" updates that can leave the system in an unusable state. Update failures are common with general-purpose OSes because of unrecoverable failures during package-by-package updates.

### Enable "kernel lockdown" to prevent attackers from adding kernel modules

- Bottlerocket supports a **kernel lockdown** configuration.  When you configure **kernel lockdown** in **integrity** mode, this limits an attacker's ability to overwrite the kernel's memory or modify its code. It also can prevent an attacker from loading unsigned kernel modules. Only kernel modules included in the Bottlerocket image can be loaded.

### Use read-only root file system and dm-verity to prevent attackers from replacing files

1. Bottlerocket can offer additional layers of protection by preventing changes to files on the root filesystem by mounting `rootfs` as a read-only volume. (This is the default behaviour)
    ```
    [root@admin]# findmnt
    TARGET                      SOURCE                 FSTYPE     OPTIONS
    ├─/.bottlerocket/rootfs     dev/dm-0               ext4       ro,relatime,seclabel
    ```
2. Bottlerocket also makes use of **dm-verity**, a Linux kernel module that provides transparent integrity checking of block devices using a cryptographic digest.
    - Each time the system boots, the **dm-verity** verifies integrity of the root filesystem and will **refuse to boot** the operating system when there's an error or evidence of corruption.
    - If the node is already running, and there is a data change (e.g from a `dd` command), **dm-verity** will identify hash corruption and **immediately reboot the node**.

### Use SELinux enforcing mode to provide permission boundaries and prevent unprivileged containers accessing resources on the system

1. On Bottlerocket, **SELinux** is being run in **enforcing mode by default** and the kernel is compiled in such a way that it prevents SELinux from being disabled or from enforcement mode being turned off.
2. Additionally, the built-in rules on Bottlerocket automatically restrict the resources that can be accessed by containers that run on the system. All unprivileged containers are automatically assigned the restrictive container_t label. This constrains the actions that the container and its child processes can perform against the host operating system, **even when the container is run as root**.

    ```
    ℹ️ Containers that run as privileged are assigned the `control_t` label, which allows writes to Bottlerocket's API socket in addition to the actions allowed under the `container_t` domain. The `super_t` label (aka. superpowered containers) allows a majority action on the host (those defined in the SELinux policy) and should be reserved solely for the admin container.

    ℹ️ As a best practice, you should create a policy that prohibits the bulk of your containers from running as privileged or that try running with the `control_t` or `super_t` labels.
    ```

### Ephemeral storage for configuration

- On Bottlerocket, users cannot modify system configuration files such as `/etc/resolv.conf` or `/etc/containerd/config.toml` directly.
- `/etc` is a `tmpfs` mount on Bottlerocket rather than a directory on a persisted filesystem. If an attacker were to modify the files in `/etc`, their changes would not be persisted after system rebooted. Using a `tmpfs` volume, along with **dm-verity**, make it difficult for an attacker to persist changes to the file system that will survive a reboot.
- When you do need to change the configuration of the system, you do so through the Bottlerocket API, and these changes are persisted across reboot and migrated through operating system upgrades. They are used to render system configuration files from templates on every boot.

### ECS/EBS encryption vs. OS crypto

- Bottlerocket operates with 2 default storage volumes (**standard EBS encryption applicable**)
- The **root device**, holds the active and passive partition sets. It also contains the **bootloader**, the **dm-verity** hash tree for verifying the immutable root filesystem, and the data store for the Bottlerocket API. Unexpected changes to the contents of the disk image will cause the operating system to fail to boot. (**Bottlerocket cryptographically verifies itself**)
- The **data device** is used as persistent storage for container images, container orchestration, host-containers, and bootstrap containers.

### CIS Hardening Benchmark for Bottlerocket

- Yes. Bottlerocket has a Center for Internet Security (CIS) Benchmark. The CIS Benchmark is a catalog of security-focused configuration settings that help Bottlerocket customers configure or document any non-compliant configurations in a simple and efficient manner. The CIS Benchmark for Bottlerocket includes both Level 1 and Level 2 configuration profiles.
- See also https://github.com/bottlerocket-os/bottlerocket/issues/1297, https://github.com/bottlerocket-os/bottlerocket/issues/2731.

### FIPS Support / Validation

- No, Bottlerocket does not yet have a FIPS certification. FIPS certification for Bottlerocket is the roadmap, but, at this moment, no estimate when it will be available.
- See Issue (Open): https://github.com/bottlerocket-os/bottlerocket/issues/1667

### Does Bottlerocket have integration with AWS Inspector?

- Yes. Bottlerocket is supported by AWS inspector in commercial regions (2022-09-29).
- Inspector leverages the AWS System Manager (SSM) agent to scan for vulnerabilities. The SSM agent runs within the control container, so you need to make sure it is enabled in your hosts.

### Is OS host logs available? Does it have integration with CloudWatch Log?

- Yes. You can use `logdog` through the admin container to obtain an archive of log files from your Bottlerocket host. This will write an archive of the logs to `/var/log/support/bottlerocket-logs.tar.gz`. This archive is accessible from host containers at `/.bottlerocket/support`. You can use SSH to retrieve the file.
- No. There is no current plan to add a logging agent to the host OS.
    - Issue (Open) https://github.com/bottlerocket-os/bottlerocket/issues/850
    - Comments from Maintainers:
        > We have no current plans to add a logging agent to the host OS.

        > When talking with many EKS customers, we found that a common pattern is to use Kubernetes' facilities for log streaming, even for system level logs. Another method is to use Fluent Bit as covered in this blog post. These are our suggested methods for customers to get both container logs as well as other logs off the box.
    - CloudWatch supports collecting logs from Bottlerocket nodes (not host). There are multiple options to collect logs from Bottlerocket nodes. For example, you can use CloudWatch Container Insights or Fluent Bit with OpenSearch.

### Watch for admin container launches

- Bottlerocket has an Admin container (an Amazon Linux container image) , disabled by default, that runs outside of the orchestrator in a separate instance of containerd.
- (A) Enabling (launching) an admin container:
    - To enable the admin container:
        1. You can change the setting in user data when starting Bottlerocket, for example EC2 instance user data:
            ```
            [settings.host-containers.admin]
            enabled = true
             ```
        2. If Bottlerocket is already running, you can enable the admin container from the default control container like this:
            ```
            enable-admin-container
            # Or you can start an interactive session immediately like this:
            enter-admin-container
            ```
    - Potential solutions:
        1. For (1),
            1. Could be communicated as a DONT in sample TOML config.
            1. Use `ssm send-command` to check `apiclient -u /settings` and enforce `settings.host-containers.admin.enabled = false` (see example of using ssm send-command)
        2. For (2),
            1. Session Manager log can capture activities of the two commands in (2), and also the activities in after entering the admin container. Tested and confirmed.
- (B) Connecting to admin container:
    - You can connect to the admin container:
        1. from the default control container using:
            ```
            apiclient exec admin bash
            # OR
            enter-admin-container
            ```
        2. log in as ec2-user using your EC2-registered SSH key (e.g. using EC2 instance connect). Outside of AWS, you can pass in your own SSH keys, by populating the admin container's user-data with a base64-encoded JSON block. If user-data is populated then Bottlerocket will not fetch from IMDS at all, but if user-data is not set then Bottlerocket will continue to use the keys from IMDS.
    - Possible solutions:
        1. For (1),
            1. Session Manager log can capture activity of (1), and also the activities in after entering the admin container.
        2. For (2),
            1. We could use `ssm send-command` to check if additional key specified in `settings.host-containers.admin.user-data` (see https://aws.amazon.com/blogs/apn/getting-started-with-bottlerocket-and-certified-aws-partners/)

## DO's and DONT's via the TOML config

- For details of all settings, see https://github.com/bottlerocket-os/bottlerocket/#description-of-settings.
- DO's
    ```
    [settings.metrics]
    send-metrics = false
    # By default, Bottlerocket sends anonymous metrics when it boots, and once every six hours.
    # This can be disabled by setting send-metrics to false.

    [settings.kernel]
    lockdown = "integrity"
    # This limits an attacker's ability to overwrite the kernel's memory or modify its code.
    # It also can prevent an attacker from loading unsigned kernel modules.
    # Ref: https://aws.amazon.com/blogs/opensource/security-features-of-bottlerocket-an-open-source-linux-based-operating-system/

    [settings.host-containers.admin]
    enabled = false
    # Admin container is disabled by default. Keep it disabled until you really need it.
    # You can enable it directly with API in the control container of the instance.

    superpowered = false
    # Whether the admin container has high levels of access to the Bottlerocket host.
    # Keep it disabled.

    [settings.host-containers.control.enabled]
    enabled = true
    # Control container is enabled by default. Keep it enabled.
    # Control container runs the SSM agent (needed for Session Manager and Inspector).

    superpowered = false
    # Whether the control container has high levels of access to the Bottlerocket host.
    # Keep it disabled.
    ```
- DONT's
    - `settings.aws.credentials`: The base64 encoded content to use for AWS credentials (e.g. base64 -w0 ~/.aws/credentials).
    - `settings.host-containers.admin.source`: The URI of the admin container.
    - `settings.network.hostname`: The desired hostname of the system.
        - Important note for all Kubernetes variants: Changing this setting at runtime (not via user data) can cause issues with kubelet registration, as hostname is closely tied to the identity of the system for both registration and certificates/authorization purposes. Most users don't need to change this setting as the following defaults work for the majority of use cases. If this setting isn't set we attempt to use DNS reverse lookup for the hostname. If the lookup is unsuccessful, the IP of the node is used.


---
## Bottlerocket AMIs and Containers

The Bottlerocket image is vended through an update repository protected with **The Update Framework (TUF)**. TUF also provides the mechanism Bottlerocket uses for doing secure, in-place upgrades of the operating system.
    - Embedded within each Bottlerocket image is a **root.json** file that begins the chain of trust in that it lists the keys that Bottlerocket will trust. This file is signed by multiple keys to hinder an attacker's ability to replace it with a different version.
    - The TUF repository also includes a **targets.json** (also signed) file, which lists all the available target files in the repository and their hashes. Any file listed in the manifest is considered a TUF target and can only be downloaded from the TUF repository, thereby preventing Bottlerocket from downloading untrusted data, including untrusted images. This helps ensure the ongoing integrity of the software supply chain for Bottlerocket.

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
    - Instance state remains Running (at least it's showing Running after refresh the console).
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

---
### Crowdstrike support

Bottlerocket is now supported starting from Falco 0.34, see [release notes](https://github.com/falcosecurity/falco/releases/tag/0.34.0), [Ref-2](https://github.com/falcosecurity/libs/issues/706#issuecomment-1424154111), and also current [supported drivers](https://download.falco.org/driver/site/index.html?lib=4.0.0%2Bdriver&target=bottlerocket&arch=all&kind=all).
