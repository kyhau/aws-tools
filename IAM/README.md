# IAM

- AWS console does not support switch roles transitively (double role switching).
    > When you switch roles in the AWS Management Console, the console always uses your original credentials to authorize the switch. This applies whether you sign in as an IAM user, as a SAML-federated role, or as a web-identity federated role. For example, if you switch to RoleA, it uses your original user or federated role credentials to determine if you are allowed to assume RoleA. If you then try to switch to RoleB while you are using RoleA, your original user or federated role credentials are used to authorize your attempt. The credentials for RoleA are not used for this action.
    - See https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_permissions-to-switch.html
    - See https://stackoverflow.com/questions/60932053/aws-console-switch-role-transitively-twice-in-a-row

- [Refining Permissions Using Service Last Accessed Data](
  https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html)
 
