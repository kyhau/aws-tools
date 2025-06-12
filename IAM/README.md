# IAM

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [AWS User Federation](#aws-user-federation)
- [AWS console does not support switch roles transitively (double role switching)](#aws-console-does-not-support-switch-roles-transitively-double-role-switching)
- [Assume Role in Go v2](#assume-role-go-v2)
- [OIDC](#oidc)


---

## Useful Libs and Tools

- AWS IAM Policy Simulator - [IAM Policy Simulator Console](https://policysim.aws.amazon.com/)
- AWS Managed Policies (list/monitor) - [z0ph/aws_managed_policies](https://github.com/z0ph/aws_managed_policies/tree/master/policies)
- AWS Policy Generator - [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)
- [aws.permissions.cloud](https://aws.permissions.cloud/) - uses a variety of information gathered within the IAM Dataset and exposes that information in a clean, easy-to-read format.


## Useful Articles and Blogs
- [The many ways to obtain credentials in AWS](https://www.wiz.io/blog/the-many-ways-to-obtain-credentials-in-aws), Wiz, 2024-12-21
- [Refining Permissions Using Service Last Accessed Data](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html)


### Different ways to obtain AWS credentials

1. From AWS SDK credential providers
    1. IAM user access Key
    2. Environment variables such as `AWS_SECRET_ACCESS_KEY`
    3. From local file such as `~/.aws/credentials`
    4. From IMDS
        - EC2
            - `IMDS v1: http://169.254.169.254/latest/meta-data/iam/security-credentials/`
            - `IMDS v2 (IPv6): [fd00:ec2::254]`
        - ECS/EKS
            - Environment variables: `AWS_CONTAINER_CREDENTIALS_FULL_URI`, `AWS_CONTAINER_AUTHORIZATION_TOKEN` (e.g. CloudShell and IoT Greengrass 2.0)
        - EKS Pod Identities
            - `IP address 169.254.170.23 (or [fd00:ec2::23] for IPv6)`
            - Variable `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE` (by default set to `/var/run/secrets/pods.eks.amazonaws.com/serviceaccount/eks-pod-identity-token`) which sets an HTTP header `Authorization` to the value of that file.
        - IRSA (IAM Roles for Service Accounts)
            - Environment variables `AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN` set, which are used to make an anonymous call to `sts:AssumeRoleWithWebIdentity`.
            - By default the token file will be at `/var/run/secrets/eks.amazonaws.com/serviceaccount/token`.
2. Default Host Management Configuration - SSM (AWS Systems Manager), SSM Agent
    1. Default Host Management Configuration (DHMC)
        - Default IAM role named `AWSSystemsManagerDefaultEC2InstanceManagementRole`
        - Use `http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance`
            - The additional steps involved in getting the creds involve generating a key pair, which is stored in `/var/lib/amazon/ssm/Vault/Store/EC2RegistrationKey`. The key pair within that file can then be used without the need to access the metadata service (ie. access to that file is sufficient for obtaining credentials as if the EC2 was requesting them).
            - The SSM agent will then store these credentials in `/var/lib/amazon/ssm/credentials` or `/root/.aws/credentials`.
3. Systems Manager hybrid activation (SSM Agent)
    - for managing compute resources within an on-prem environment or other non-AWS resources.  This same technique is also used by ECS Anywhere and is part of IoT Greengrass.
    - The agent is activated using an activation code and activation id, and then creates the files `/var/lib/amazon/ssm/Vault/Store/RegistrationKey` and `/var/lib/amazon/ssm/Vault/Store/InstanceFingerprint` which are then used to obtain credentials.
4. Cognito
    -  API `GetCredentialsForIdentity` which is passed an identity ID, which is just a region and GUID value, and will return AWS session credentials.
5. Datasync
    - Within `/usr/local/aws-storage-gateway/var/` it will use the files `cert.pem` and `keypair.pem` to authenticate to AWS, and the datasync agent will then use those to potentially sync an S3 bucket and a local directory.
6. IoT
    - The API `iot:AssumeRoleWithCertificate`
7. IAM Roles Anywhere

References: [Ref-1](https://www.wiz.io/blog/the-many-ways-to-obtain-credentials-in-aws)


### AWS User Federation
- Key notes
    - So this federated session is associated to an IAM User, with Access Key and permission `sts:GetFederationToken` to start.
    - Then using the federated session to log into console even if the IAM User has no password.
    - And if the IAM User has permissions, e.g., `AttachUserPolicy` or `PutUpdatePolicy`, the federated session allows to escalate privileges from console (which is not possible when using CLI/API)
    - And federated session are only revoked when the base user's policies/permissions are detached, or an explicit deny-all IAM policy is applied.
    - And federated sessions derived from the root user cannot be contained except through an SCP.
- Protection: Create an SCP preventing the use of   `sts:GetFederationToken` for all IAM users.
- [How Adversaries Can Persist with AWS User Federation](https://www.crowdstrike.com/blog/how-adversaries-persist-with-aws-user-federation/), CrowdStrike, 2023-01-30
- [Survive Access Key Deletion with sts:GetFederationToken](https://hackingthe.cloud/aws/post_exploitation/survive_access_key_deletion_with_sts_getfederationtoken/), Nick Frichette, 2023-09

### AWS console does not support switch roles transitively (double role switching)
> When you switch roles in the AWS Management Console, the console always uses your original credentials to authorize the switch. This applies whether you sign in as an IAM user, as a SAML-federated role, or as a web-identity federated role. For example, if you switch to RoleA, it uses your original user or federated role credentials to determine if you are allowed to assume RoleA. If you then try to switch to RoleB while you are using RoleA, your original user or federated role credentials are used to authorize your attempt. The credentials for RoleA are not used for this action.

- See https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_permissions-to-switch.html
- See https://stackoverflow.com/questions/60932053/aws-console-switch-role-transitively-twice-in-a-row


---
### Assume Role go v2

- https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/credentials/stscreds
- https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/gov2/sts/AssumeRole/AssumeRolev2.go
- https://stackoverflow.com/questions/65585709/how-to-assume-role-with-the-new-aws-go-sdk-v2-for-cross-account-access
- https://flowerinthenight.com/blog/2021/04/30/authenticate-aws-sdk-golang-v2

---
### OIDC

- [Identity-provider controls for shared OIDC providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc_secure-by-default.html)
- OpenIDConnectProvider
    1. `iam:*OpenIDConnectProvider*` permissions are not required when creating an EKS cluster `CreateCluster`, which creates an OpenID Connect provider (issuer) URL for the cluster (e.g. https://oidc.eks.ap-southeast-2.amazonaws.com/id/xxx). And in CloudTrail, there are no `*OpenIDConnectProvider*` events.
    2.  After (1), the cluster has an OpenID Connect issuer URL associated with it. To use IAM roles for service accounts, an IAM OIDC provider must exist for your cluster. See [here](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html).
        - You need to run the `ekctl associate-iam-oidc-provider`,

              $ eksctl utils associate-iam-oidc-provider --cluster=development-k-test-oicd --approve --region=ap-southeast-2 --profile test-oidc

        - A Open ID Provider with the same URL as (1) is created. For this step, this role needs to have the following permissions

              iam:CreateOpenIDConnectProvider
              iam:GetOpenIDConnectProvider
              iam:TagOpenIDConnectProvider

        - CloudTrail does NOT show the events as well (e.g. CreateOpenIDConnectProvider)
        - See also [../EKS/test-oidc](../EKS/test-oidc/)

- Monitor the following on modification and creation of IAM OpenID Connect provider
    - Alert on use of unauthorised `url` and `thumbprint`
    - Alert on IAM Roles that trust an unapproved `OpenIDConnectProvider` (i.e. using associated with unapproved `url` or `thumbprint`).
    - Access Analyzer is flagging roles with OIDC provider. It can be used for alerting.
