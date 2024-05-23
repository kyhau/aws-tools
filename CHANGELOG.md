# Changelog

All notable changes to this project will be documented in this file.

## 2024-05-23

### Added

   * Added Health/health_org_helper.py, that exports affected resources of an AWS Health event for accounts in an organization.

## 2024-03-26

### Changed

   * Updated get_latest_ami.py to support eks k8s v1.29 and AL2023

## 2023-11-22

### Changed

   * Updated CloudFormation/list_stacks.py to default the stack name search case insensitive.

## 2023-11-11

### Added

   * Added .github/workflows/secrets-scan.yml

## 2023-11-03

### Added

   * Added IAM/account_id_from_access_key.py

## 2023-10-25

### Changed

   * Updated AWS-Public/aws-public-ip-address-ranges.py to support checking if a given IP is within AWS public IP ranges.

## 2023-07-31

### Added

   * Added _Others/fault-tolerance-analyser/install-fault-tolerance-analyser.sh

## 2023-07-07

### Changed

   * Updated scripts in CodeArtifact/demo/ for CodeArtifact demo

## 2023-05-16

### Added

   * Added Config/list_all_aws_config_resource_types.sh
   * Added Config/query_configservice_aggregate.py
   * Added predefined SQL files to be used for aggregater query in Config/sql_files/aggregate/
       - list_count_eks_cluster_of_all_accounts.sql
       - list_resource_types_of_all_accounts.sql
       - resources_counts_grouped_by_account_id.sql

### Changed

   * Updated Config/README.md
   * Updated .aliases

## 2023-05-03

### Added

   * Added ECR/test-ecr-external-image-clone.sh
   * Added ECR/test-ecr-pull-through-cache.sh

## 2023-04-17

### Changed

   * Updated AMI/get_latest_amis.py to support AL2023 #353
   * Updated AMI/get_latest_amis.py to support K8S_VERSIONS 1.26 #352

## 2023-02-28

### Changed

   * Updated .aliases to add aws-ecs-list-task-definitions-inactive #324

## 2023-02-23

### Changed

   * Updated get_latest_ami.py to support eks k8s v1.25 #318

## 2023-02-15

### Added

   * Added .github/workflows/dependabot-auto-approve-merge.yml #307
   * Added EKS/get_eks_oidc_thumbprint.sh #304

## 2023-01-30

### Added

   * Added scheduled scaling cfn templates for ECS and ASG #294

## 2023-01-23

### Updated

   * Updated .aliases to add alias aws-ami-find-by-amiid #289

## 2023-12-22

### Added

   *  Added/updated CloudFront templates to support cname #271

## 2022-12-21

### Added

   * Added CloudFormation [template](CloudFront-S3/cfn/CloudFront-S3-WebDistribution-OAC-SameS3MultiBehaviors.template.yaml) for creating CloudFront with an Amazon S3 bucket as the origin and OAC.

## 2022-12-13

### Changed

   * Use `InquirerPy` instead of `PyInquirer` for CLI selector.

## 2022-11-10

### Added

   * Support Python 3.11 in build and tests.

### Changed

   * Replaced `m2r2` with `pypandoc`.
   * Replaced `set-output` in workflow.

## 2022-11-01

   * Added [shield_attack_event_ips.py](./WAF-FirewallManager-Shield/shield_attack_event_ips.py) - A helper script that print details of the attack(s) of the given attack ID or resource ARN, or check if the top 5 contributor IPs of a shield attack are in give IP ranges.

## 2022-10-12

### Added

   * Added [AuroraServerless-v2-postgresql.template.yaml](./RDS/cfn/AuroraServerless-v2-postgresql.template.yaml) - CloudFormation template for Aurora Serverless v2 PostgreSQL database cluster

## 2022-10-04

### Changed

   * Updated [AMI/get_latest_amis.py](AMI/get_latest_amis.py) to support ECS and EKS optimized Windows Servers AMI search.

## 2022-09-22

### Added

   * Added [MLTA.md](./MLTA.md) - How does Amazon Managed Service for Prometheus relate to Amazon CloudWatch? Which one should I use?

### Changed

   * Updated EC2 notes - On-Demand Instance vCPUs limits
   * Updated EC2 notes - Encryption in transit
   * Updated EC2 notes - Amazon Linux 2 amazon-linux-extras repository
   * Updated Security note - mTLS notes - Mutual Transport Layer Security (mutual TLS or mTLS) authentication

### Removed

   * Removed IAM/set_aws_config.py.

## 2022-08-29

### Changed

   * Updated list_resources_with_configservice.py to add option `--ls` and `resource-type`.
   * Updated _common/helper/selector.py to support custom message.

## 2022-08-27

### Changed

   * Updated workflow build-test-common-helper.yaml (76767c2 from @kyhau)
   * Updated requirements.txt (76767c2 from @kyhau)
   * Updated requirements-cli.txt (76767c2 from @kyhau)
   * Updated CloudFront notes - OAC (#175) (76767c2 from @kyhau)

## 2022-08-24

### Changed

   * Updated AMI/get_latest_amis.py (#173) (5974998 from @kyhau)

## 2022-08-19

### Fixed

   * Fix bug in AMI/get_latest_amis.py (#171) (9003626 from @kyhau)

## 2022-08-18

### Added

   * Added [AWS CLI README](./awscli/README.md) (6c3f713 from @kyhau)

## 2022-08-11

### Added

   * Added [Graviton.md](Graviton.md) (#167) (b4c836a from @kyhau)

## 2022-07-31

### Changed

   * Updated ECS-vs-EKS.md (#162) (b97f372 from @kyhau)

### Removed

   * Delete nano.save (#163) (238119e from @kyhau)

## 2022-07-30

### Added

   * Added short summary of ECS v EKS (#158) (75139eb from @kyhau)

## 2022-07-29

### Added

   * Added PR template (#156) (13dafb2 from @kyhau)

### Changed

   * Updated AMI/get_latest_amis.py (994ba26 from @kyhau)

## 2022-07-27

### Changed

   * Updated .aliases npm (#153) (ce9482a from @kyhau)

## 2022-07-14

### Changed

   * Updated LoadTesting (#146) (fc99db4 from @kyhau)

## 2022-07-12

### Changed

   * updatecanonical (#143) (d3eb339 from @kyhau)

## 2022-06-21

### Changed

   * Updated Security.md (b2af732 from @kyhau)

## 2022-06-17

### Changed

   * Updated dependabot.yml (0145c73 from @kyhau)

## 2022-06-15

### Changed

   * Updated cdk8s/install-cdk8s-cli.sh (18d6954 from @kyhau)
   * Updated EKS/install_eks_aws_iam_authenticator.sh (#130) (b7b6115 from @kyhau)

## 2022-05-31

### Changed

   * Updated CDK/install-cdk-v2.sh (5fc3457 from @kyhau)

## 2022-05-30

### Changed

   * Updated Dockerfile.base (9e50d40 from @kyhau)

## 2022-05-26

### Changed

   * Updated Encryption.md (ba37309 from @kyhau)

## 2022-05-21

### Changed

   * Enable Snyk (23a830c from @kyhau)

## 2022-05-17

### Changed

   * Updated .aliases (088663e from @kyhau)

## 2022-05-09

### Changed

   * Updated EKS/install_eksctl.sh (16d9b46 from @kyhau)

## 2022-05-06

### Changed

   * Updated .aliases (7eb6797 from @kyhau)

## 2022-05-05

### Changed

   * Updated Athena CFN templates (f007ccf from @kyhau)
   * Updated CDK/install-cdk-v2.sh (e8c869d from @kyhau)

## 2022-04-23

### Changed

   * Updated AMI/get_latest_amis.py (0d88c5a from @kyhau)

## 2022-03-31

### Added

   * Added get_layer_code_packages.py (dd84cf2 from @kyhau)

## 2022-03-28

### Added

   * Added Bottlerocket README (36ec5a9 from @kyhau)

## 2022-03-26

### Added

   * Added cdk-import install script (44f5763 from @kyhau)

## 2022-03-25

### Added

   * Added APIGateway/list_domains.py (3064541 from @kyhau)

## 2022-03-20

### Added

   * Added setup_oidc_github/ (b21a0c1 from @kyhau)

## 2022-02-20

### Added

   * Add diagram links of k8s and kinesis (#125) (ad1becd from @kyhau)

## 2022-02-19

### Removed

   * Delete CloudFormer.md (236cd3b from @kyhau)

## 2022-02-18

### Changed

   * Updated git-secrets install script (e4b4927 from @kyhau)
   * Updated Useful-tools/git_secrets/install_git_secrets.sh (244b380 from @kyhau)
   * Find Windows images size >= 1 GB referenced in current clusters in all specified aws accounts (#124) (0e2b953 from @kyhau)
   * test-oidc (#123) (290b96f from @kyhau)

## 2022-02-01

### Added

   * Added script to install Step Functions Local (#120) (c7b4c24 from @kyhau)

## 2022-01-28

### Changed

   * Updated codeartifact demo scripts (64d1384 from @kyhau)

## 2022-01-27

### Changed

   * Updated CodeArtifact/demo_using_python/02_list_repo_packages.sh (dbec4b2 from @kyhau)
   * Updated CodeArtifact demo scripts (05a0bb5 from @kyhau)

## 2022-01-25

### Added

   * Added CodeArtifact/cfn/ (9440258 from @kyhau)

## 2022-01-24

### Added

   * Added list_ecr_repos.py (#117) (200eb1f from @kyhau)

## 2022-01-21

### Added

   * Added EKS/basic-eks.yaml (be52f9c from @kyhau)

### Changed

   * Renamed cloudformation to cfn (#114) (46d377e from @kyhau)

## 2022-01-18

### Added

   * Added list_open_id_providers.py for EKS clusters (#113) (c5a2e06 from @kyhau)

## 2022-01-15

### Changed

   * Updated cdk8s installation script (a14db17 from @kyhau)

## 2022-01-11

### Added

   * Added Lambda/get_lambda_code_package.py (#112) (5ac9832 from @kyhau)

### Removed

   * Removed CDK/install-cdk-v1.sh (71dda0c from @kyhau)

## 2022-01-02

### Changed

   * Updated S3/list_s3_buckets.py to use fire instead of click (000ae5b from @kyhau)

## 2021-12-15

### Changed

   * Updated .aliases (511ab66 from @kyhau)

## 2021-12-04

### Changed

   * Updated CDK V2 installation script (a6b1bc7 from @kyhau)

## 2021-11-25

### Added

   * Added _common/helper/selector (9206d47 from @kyhau)

### Changed

   * Renamed _common/helper/date_time (836e173 from @kyhau)

### Removed

   * Delete Install-saml2aws.ps1 (2eafcda from @kyhau)

## 2021-11-19

### Added

   * Added _multi_services/aws-public-account-ids.py (8a8058b from @kyhau)

### Changed

   * Updated install awscli v2 scripts (#110) (337cc9c from @kyhau)

## 2021-11-16

### Added

   * Added _multi_services/aws-public-ip-address-ranges.py (#109) (2510979 from @kyhau)

## 2021-11-15

### Added

   * Added loggroups command (#108) (d1e8d09 from @kyhau)

## 2021-11-03

### Added

   * Added .github/linters/.cfnlintrc (a8f38c8 from @kyhau)

## 2021-11-02

### Changed

   * Updated ELB/list_elb.py (d3f0a6f from @kyhau)
   * Updated _multi_services/databases_status_check.py (fa14aa8 from @kyhau)
   * Renamed file (4a2b7a3 from @kyhau)
   * Updated .aliases (35b78cc from @kyhau)

## 2021-10-29

### Changed

   * Updated install sam-cli and sam-cli-beta-cdk scripts (#105) (518ace9 from @kyhau)

## 2021-10-15

### Added

   * Added ecs-fargate-with-ecs-cli (cd21cfd from @kyhau)
   * Added install_ecs_cli.sh (0aadd45 from @kyhau)

## 2021-10-14

### Changed

   * Updated requirements (cc8e255 from @kyhau)

## 2021-10-13

### Changed

   * Updated cdk8s-cli install scripts (b7143aa from @kyhau)

## 2021-10-11

### Changed

   * AWSCLI/Install-awscli-v2.ps1 (0c522b3 from @kyhau)
   * Updated Install-AWS-Tools.ps1 (8bbc433 from @kyhau)

## 2021-10-08

### Changed

   * Updated EKS/install_eksctl.sh (02f9626 from @kyhau)

## 2021-10-07

### Added

   * Added _multi_services/aws-public-ip-address-ranges.py (#99) (c8510d5 from @kyhau)

## 2021-10-02

### Added

   * Added codeql-analysis.yml (e5ea456 from @kyhau)

### Changed

   * Updated .aliases (55733ac from @kyhau)
   * Moved k8s scripts to other repo (06fe481 from @kyhau)

## 2021-09-29

### Added

   * Added k8s tool installation scripts (78b193d from @kyhau)

## 2021-09-22

### Changed

   * Updated install eks tool scripts (aa81c45 from @kyhau)

## 2021-09-04

### Added

   * Added APIGateway/cloudformation/private-api-backend.yaml (db30273 from @kyhau)

### Fixed

   * Fixed cfnlint warnings (79bc60e from @kyhau)

## 2021-09-01

### Added

   * Updated create_iam_user_github_key_rotation (91b3002 from @kyhau)

## 2021-08-28

### Added

   * Added put_cloudwatch_dashboard (c6f1396 from @kyhau)

## 2021-08-06

### Added

   * Added cognito_admin_initiate_auth_with_oauth2_hash.py (fbe728c from @kyhau)

### Changed

   * Updated help page (e7f5102 from @kyhau)

## 2021-07-13

### Added

   * Added manage-scps (bba86e2 from @kyhau)
   * Added a helper tool to support managing security hub standards controls (d73b542 from @kyhau)

## 2021-07-12

### Added

   * Added manage-stack-set-instance script (#91) (3aeb70f from @kyhau)

## 2021-07-09

### Changed

   * Updated install-sam-beta-cdk.sh (7a2cd2c from @kyhau)

## 2021-06-29

### Added

   * Added Organizations/list_policies.py (6b14757 from @kyhau)

## 2021-06-24

### Added

   * Added list_securityhub_standard_controls.py (0d827a2 from @kyhau)

### Changed

   * Updated list_securityhub_standard_controls.py (74fde10 from @kyhau)
   * Updated list_securityhub_standard_controls.py (ba9e705 from @kyhau)
   * Updated to support --detailed mode (ba9e705 from @kyhau)

## 2021-06-22

### Changed

   * Changed /mnt/c to /c (ef3bbab from @kyhau)

## 2021-06-12

### Changed

   * Updated installation command of cdk-assume-role-credential-plugin (77cb378 from @kyhau)

## 2021-06-06

### Added

   * Added create_ssm_parameters.py (c5f828d from @kyhau)

### Changed

   * Updated install-aws-session-manager-plugin-ubuntu.sh and .aliases (4eceb73 from @kyhau)

## 2021-06-05

### Changed

   * Updated Lambda Runtime (4ab7d67 from @kyhau)

## 2021-05-26

### Changed

   * Updated list_security_groups.py to handle "InvalidGroup.NotFound" (087df9d from @kyhau)

## 2021-05-22

### Added

   * Added capacity_checker.md (7e32515 from @kyhau)

## 2021-05-19

### Added

   * Added install-cfn-guard.sh, removed install_ecs_cli_v2.sh (0cd3889 from @kyhau)

## 2021-05-17

### Changed

   * Updated .aliases (555c0b5 from @kyhau)

## 2021-05-15

### Added

   * Added sam-beta-cdk installation script (36ea991 from @kyhau)
   * Added CloudShell init scripts (2e1c2e9 from @kyhau)

### Changed

   * Renamed CDK installation scripts (d0d98a4 from @kyhau)

## 2021-05-12

### Added

   * Added install_ecs_exec.sh (9eddd9a from @kyhau)

## 2021-05-11

### Changed

   * Merge remote-tracking branch 'origin/master' (d2dfd1e from @kyhau)

## 2021-05-10

### Added

   * Added CloudWatch-Synthetics.md (a9ca703 from @kyhau)

## 2021-05-09

### Changed

   * Updated requirements files (f775249 from @kyhau)

### Fixed

   * Fixed cfn-lint errors (b99df8d from @kyhau)

## 2021-05-08

### Added

   * Added install_cdk_v2.sh (551e4bd from @kyhau)
   * Updated create_key_pair.sh (fc04997 from @kyhau)

### Changed

   * Updated requirements-cli.txt (cbc3e8c from @kyhau)

## 2021-05-07

### Changed

   * Updated list_ec2_instances.py (40d45d1 from @kyhau)

## 2021-05-05

### Changed

   * Updated .aliases (11d09c4 from @kyhau)

## 2021-05-04

### Added

   * Added install_awscii_cli.sh (2d16018 from @kyhau)

### Changed

   * Updated .aliases (f4f77f7 from @kyhau)
   * Updated .aliases (05309c5 from @kyhau)
   * Updated .aliases (cc8b547 from @kyhau)

## 2021-03-03

### Added

   * Added update_rest_api_stage_settings.sh (a6cedaa from @kyhau)

## 2021-03-02

### Added

   * Added sample default value (3c44a8d from @kyhau)

## 2021-02-22

### Changed

   * Updated .aliases and rename a file (0882020 from @kyhau)

## 2021-02-18

### Added

   * Added fields to list_rds_* (c778950 from @kyhau)
   * Added list_rds_clusters and list_rds_cluster_endpoints (5fba7a6 from @kyhau)

## 2021-02-17

### Changed

   * Updated .aliases (ef28534 from @kyhau)
   * Updated .aliases (d28d582 from @kyhau)
   * Updated .aliases (7e85275 from @kyhau)

## 2021-02-16

### Changed

   * Merge remote-tracking branch 'origin/master' (2debd49 from @kyhau)
   * Updated RDS Aurora templates (ea0cdf8 from @kyhau)
   * Updated install_cdk.sh (f0621c0 from @kyhau)

## 2021-02-15

### Added

   * Added list_api_gateways.py, list_lambda_*.py (73eb579 from @kyhau)

## 2021-02-14

### Changed

   * Updated CloudWatch/send_cloudwatch_log_event.py (051d299 from @kyhau)

## 2021-02-13

### Changed

   * Updated cloudwatch_logs_insights_run_query.py (e9d0e8e from @kyhau)
   * Updated CloudWatch/CloudWatch-LogsInsights/cloudwatch_logs_insights_run_query.py to take queryString instead of queryFile (e9d0e8e from @kyhau)

## 2021-02-12

### Added

   * Added list_elb.py (c740e81 from @kyhau)
   * Added xray_sampling_rule.py (d70519c from @kyhau)

### Changed

   * convert the query time from local to utc (9cbc7ab from @kyhau)
   * Renamed files (6ccec19 from @kyhau)

## 2021-02-09

### Added

   * Added image X-Ray/xray-sqs-to-lambda/x-ray-sqs-to-lambda-to-others.png (5d5c904 from @kyhau)

## 2021-02-08

### Added

   * Added an x-ray sqs-to-lambda workaround example (ts) (66e922c from @kyhau)

## 2021-02-05

### Changed

   * Updated x-ray notes (a3bcbb1 from @kyhau)

## 2021-01-22

### Added

   * Added CloudWatchAlarms-SnsNotification-ForSfn.template.yaml (1b4effb from @kyhau)

### Changed

   * Updated CloudWatchAlarms-SnsNotification-ForApigw.template.yaml (e470984 from @kyhau)
   * Updated CloudWatchAlarms-SnsNotification-ForApigw.template.yaml (e470984 from @kyhau)

## 2020-12-16

### Changed

   * Updated list_cloudtrail_security_event_names.py (d9fb6a8 from @kyhau)

## 2020-12-14

### Added

   * Added list_cloudtrail_security_event_names.py (b71e181 from @kyhau)

## 2020-12-12

### Added

   * Added a lambda function for testing private API gateway (f8d752c from @kyhau)

## 2020-12-11

### Added

   * Added API-Mock-Simple-Private (389ed51 from @kyhau)

## 2020-12-06

### Added

   * Added Apigw-LambdaProxy (548b3ca from @kyhau)
   * Added API-Mock-Simple (0d02f04 from @kyhau)

### Changed

   * Updated deploy.sh (57db6cc from @kyhau)
   * Renamed folder (d3cfaf2 from @kyhau)
   * Updated API-SFN-Lambda (f389278 from @kyhau)
   * Updated ApiGateway-CloudWatchLogs.template.yaml and deploy.sh (9e0bfe7 from @kyhau)
   * Updated test_api.sh (9014cc8 from @kyhau)

## 2020-12-04

### Added

   * Added API-SFN-Lambda (eb9359f from @kyhau)
   * Added API-Mock (c0dc7da from @kyhau)

### Changed

   * Updated API-CanaryDeployment (419afc3 from @kyhau)

## 2020-11-19

### Added

   * Added scripts to like emr, fsx, firehose, storage gateways in multi accounts (26163cc from @kyhau)
   * Added scripts to like emr, fsx, firehose, storage gateways in multi accounts (26163cc from @kyhau)

## 2020-11-17

### Added

   * Added init versions (94da286 from @kyhau)
   * Added file from reko repo (94da286 from @kyhau)

### Changed

   * Demo for canary deployment - apig, sfn, lambda (#67) (2812a26 from @kyhau)
   * Minor updates (#66) (94da286 from @kyhau)
   * Updated rekognition.py (94da286 from @kyhau)

## 2020-11-09

### Fixed

   * Fixed vpc_flow_logs.py (c614a57 from @kyhau)

### Removed

   * Removed print lines (e187968 from @kyhau)

## 2020-11-05

### Changed

   * Updated file_io.py (59d9da0 from @kyhau)

## 2020-11-03

### Changed

   * Updated cloudtrail_lookup_events.py to decode json string in "CloudTrailEvent" attribute (optionally) (ef906f8 from @kyhau)

## 2020-11-02

### Added

   * Added StepFunctions/README.md (ae16d21 from @kyhau)

## 2020-10-31

### Changed

   * Updated .aliases (fe915df from @kyhau)

## 2020-10-28

### Added

   * Updated available_ip_address_count.sh (faa8764 from @kyhau)

### Fixed

   * Fixed start/end times in cloudtrail_lookup_events.py (#65) (9784868 from @kyhau)
   * Fixed cloudtrail_lookup_events.py where startt/end times passing to cloudtrail api shall be in utc (9784868 from @kyhau)

### Removed

   * Removed unused import (9784868 from @kyhau)

## 2020-10-27

### Changed

   * Updated list_workspaces_details.py (e023fbd from @kyhau)

## 2020-10-21

### Changed

   * Updated install_nodejs.sh (fd0d6cb from @kyhau)

## 2020-10-18

### Added

   * Added capacity_checker.py to check capacity of scalable aws resources (#62) (d586bf1 from @kyhau)
   * Added few scripts to add owner permissions to a set of QuickSight Analyses/Dashboards/DataSets (d586bf1 from @kyhau)
   * Added capacity_checker.py to check capacity of scalable aws resources (d586bf1 from @kyhau)

### Changed

   * Refactored code into new repo (62ce534 from @kyhau)

## 2020-10-17

### Changed

   * CDK for deploying lambda and event role to set CW loggroups retention (#61) (f758bc0 from @kyhau)

## 2020-10-07

### Added

   * Added few scripts to add owner permissions to a set of QuickSight Analyses/Dashboards/DataSets (#60) (a3b0541 from @kyhau)

## 2020-09-30

### Changed

   * Updated install_saml2aws.sh (0a19470 from @kyhau)

## 2020-09-29

### Changed

   * Updated .aliases (8f22994 from @kyhau)

## 2020-09-28

### Changed

   * Updated install_copilot_cli.sh (f55b3b1 from @kyhau)

## 2020-09-19

### Added

   * Added list_resolver_endpoints_and_ips.py (6c1be23 from @kyhau)
   * Added unhealth-workspaces-cloudwatch-alarms.yaml (aa0b881 from @kyhau)

## 2020-09-16

### Changed

   * Updated state machine and lambda templates (59ced33 from @kyhau)

## 2020-09-07

### Added

   * Added pub-lambda-invokes-pri-lambda-cross-account (#56) (5842d0d from @kyhau)

## 2020-09-06

### Added

   * Added install_aws_tools_kyhau.sh (3c67430 from @kyhau)

### Changed

   * Updated AppMesh notes (9bc990e from @kyhau)

## 2020-09-01

### Changed

   * Updated .aliases (b7a01a3 from @kyhau)
   * Updated requirements (4d14b58 from @kyhau)

## 2020-08-31

### Added

   * Added workspace_restore_rebuild.py (acf0051 from @kyhau)

### Changed

   * Updated list_workspaces_details.py to support lookup one workspace by id (78ffea9 from @kyhau)
   * Updated list_workspaces_details (d3b8784 from @kyhau)

## 2020-08-30

### Changed

   * Updated .travis and github action config (6de935f from @kyhau)
   * Renamed arki_common to helper (94c7b9c from @kyhau)
   * Renamed arki_common to helper (e098300 from @kyhau)

## 2020-08-29

### Changed

   * Cleaned up CF templates (641e702 from @kyhau)
   * Cleaned up CF templates (1f0c1a6 from @kyhau)
   * Cleaned up CF templates (ec87eeb from @kyhau)

## 2020-08-28

### Changed

   * Cleaned up CF templates (73c9661 from @kyhau)

## 2020-08-27

### Added

   * Added .cfnlintrc (2dfdbde from @kyhau)

### Changed

   * Moved files (6048ed3 from @kyhau)

## 2020-08-24

### Added

   * Updated EC2-VPC/available_ip_address_count.py (9562826 from @kyhau)

### Changed

   * Updated install_cdk_patterns.sh (039edf8 from @kyhau)
   * Moved file (2a711b9 from @kyhau)

## 2020-08-23

### Changed

   * Cleaned up install_nodejs.sh and install_npx.sh (e14ef5e from @kyhau)
   * Moved check_aws_api (70841ff from @kyhau)

## 2020-08-22

### Added

   * Added CloudFormation/cloudformation_to_dot_to_image.py (55df013 from @kyhau)

## 2020-08-21

### Added

   * Added Amplify/install_amplify_cli.sh (f09c62f from @kyhau)
   * Added CloudFront-S3-WebDistribution-OAI-SameS3MultiBehaviors.template.yaml (c7a9e0f from @kyhau)

## 2020-08-19

### Changed

   * Updated install_eksctl.sh (1136980 from @kyhau)
   * Updated file_io.py (95e0552 from @kyhau)
   * Updated list_workspaces_connections.py (9a0100f from @kyhau)

## 2020-08-18

### Added

   * Added cloudwatch log snippet (2c98c19 from @kyhau)

## 2020-08-17

### Changed

   * Updated copilot-cli notes (f1c8652 from @kyhau)

## 2020-08-15

### Added

   * Added alias aws-iam-list-aws-managed-policies-to-files='python /mnt/c/Workspaces/github/arki/IAM/list_aws_managaed_policies_to_files.sh' (f540186 from @kyhau)

## 2020-08-13

### Added

   * Added simple script to retrieve some network services data (1b1d866 from @kyhau)

### Changed

   * Moved folders (f199b85 from @kyhau)

## 2020-08-12

### Changed

   * Updated lambda notes (06933ea from @kyhau)
   * Updated requirements-cli.txt (39dfd33 from @kyhau)

### Removed

   * Removed CDK/url-shortener (3ec735c from @kyhau)

## 2020-08-07

### Changed

   * Updated install_cdk.sh (9edefbe from @kyhau)

## 2020-08-05

### Changed

   * Updated CloudWatchInsights query files (f3c58d5 from @kyhau)
   * Updated cloudtrail_lookup_events.py to dump json instead of yaml. (842eefe from @kyhau)

## 2020-08-04

### Changed

   * Updated EC2-VPC/vpc_flow_logs.py (37d5160 from @kyhau)

## 2020-08-03

### Added

   * Added vpc_flow_logs.py (3a227cf from @kyhau)

### Changed

   * Updated CloudWatch/CloudWatch-LogsInsights/cloudwatch_logs_insights_run_query.py (141da75 from @kyhau)
   * Updated CloudWatch/CloudWatch-LogsInsights/cloudwatch_logs_insights_list_queries.py (ca5b270 from @kyhau)
   * Set theme jekyll-theme-tactile (e6ccd39 from @kyhau)
   * Set theme jekyll-theme-modernist (c712b0e from @kyhau)
   * Set theme jekyll-theme-modernist (a7902ff from @kyhau)

### Removed

   * Delete _config.yml (123b2c7 from @kyhau)

## 2020-08-02

### Changed

   * Set theme jekyll-theme-minimal (eb18513 from @kyhau)

## 2020-08-01

### Removed

   * Removed some base files, use vscode snippets instead (a1574f9 from @kyhau)

## 2020-07-30

### Changed

   * Updated requirements-cli.txt (fd9f801 from @kyhau)
   * Moved folder (b3a08cc from @kyhau)

## 2020-07-29

### Added

   * Updated create_key_pair.sh (527c83d from @kyhau)
   * Added ssh-through-session-manager.sh (1bf9614 from @kyhau)
   * Added create_key_pair.sh (1bf9614 from @kyhau)

## 2020-07-27

### Added

   * Added ECR/list_used_images_having_critical_or_high_severity_findings.py (2ec6b81 from @kyhau)

## 2020-07-25

### Added

   * Added ec2_get_console_screenshot.py (0fc8bac from @kyhau)

### Changed

   * Updated networking notes (301cb99 from @kyhau)

## 2020-07-24

### Changed

   * Updated SSM/install_aws_session_manager_plugin.sh (7a9356e from @kyhau)

## 2020-07-22

### Added

   * Added kms_decrypt.py (9c9c13f from @kyhau)
   * Added get_parameter_encrypted_with_kms.py (e929c9c from @kyhau)

## 2020-07-20

### Changed

   * Updated install_cdk.sh (36b679c from @kyhau)

## 2020-07-18

### Added

   * Added alias for delete_table_items.py (6ee4fd2 from @kyhau)

## 2020-07-16

### Added

   * Added DynamoDB/delete_table_items.py (1439cc7 from @kyhau)
   * Add timer to search_dynamodb.py (fc55d09 from @kyhau)

## 2020-07-15

### Added

   * Added simple script to install copilot-cli (0ffcee2 from @kyhau)

### Changed

   * Updated S3 templates (5a6118b from @kyhau)
   * Updated requirements (839e38f from @kyhau)

## 2020-07-14

### Added

   * Added sample chalice templates (cb815b1 from @kyhau)
   * Added list_regions.sh (220d4d9 from @kyhau)

### Changed

   * Updated S3 templates (e9bbe33 from @kyhau)
   * Updated Cognito templates (612870f from @kyhau)

## 2020-07-13

### Added

   * Added CloudFront-S3-WebDistribution-OAI.template.yaml (d76a707 from @kyhau)

## 2020-07-12

### Added

   * Added install-aws-api-gateway-developer-portal.sh (c4a9b78 from @kyhau)
   * Added saml-cli installation scripts (e9aa404 from @kyhau)
   * Added install_homebrew.sh (4bc1dee from @kyhau)

### Changed

   * Updated 2 simple s3 templates (cce2467 from @kyhau)
   * Updated file_io.py (cbaad6b from @kyhau)

## 2020-07-08

### Added

   * Updated file_io.py, added create_stack_set_*.sh (63beb03 from @kyhau)

## 2020-07-07

### Added

   * Added Useful-tools/load_testing/README.md (1b952a6 from @kyhau)

## 2020-07-06

### Added

   * Added list_resources_* (2a78e09 from @kyhau)
   * Added list_resources_* (a76c003 from @kyhau)
   * Added Route53/list_hosted_zones.py (e2cfbdd from @kyhau)
   * Added reset_pip_index.sh (04b7ac1 from @kyhau)

### Changed

   * Updated command help string in S3/list_s3_buckets.py (cccf84e from @kyhau)

## 2020-07-05

### Changed

   * Updated list_s3_buckets.py (edc6a0a from @kyhau)

## 2020-07-04

### Changed

   * Updated list_tags.py (256d577 from @kyhau)
   * Updated list_tags.py (7b6cb76 from @kyhau)
   * Refactored arki_common(#47) (a3c0200 from @kyhau)

## 2020-07-03

### Added

   * Added list_vpcs.py (28a9d3a from @kyhau)

## 2020-06-28

### Added

   * Added Inspector/inspector_helper.py (55831f7 from @kyhau)

## 2020-06-26

### Added

   * Added sample Athena sql files for TrustedAdvisor (06b9c38 from @kyhau)

### Changed

   * Minor refactoring TrustedAdvisor/trusted_advisor_check_result.py (c30313b from @kyhau)
   * Updated ACM/list_certificates.py (cab073d from @kyhau)

## 2020-06-18

### Added

   * Added 06_create_external_repository_connection.sh (b27a0d8 from @kyhau)
   * Added CodeArtifact demo scripts (4272b47 from @kyhau)

### Changed

   * Updated install_cdk.sh (e01c1af from @kyhau)

## 2020-06-17

### Added

   * Added README.md (579a5e2 from @kyhau)
   * Added CodeArtifact files (51ed202 from @kyhau)

## 2020-06-14

### Changed

   * Updated list_ips_used.py (669c0c8 from @kyhau)

## 2020-06-13

### Changed

   * Updated aws_login.py (c68b748 from @kyhau)

## 2020-06-12

### Changed

   * Updated athena_query_execution.py (#44) (aba62b3 from @kyhau)

### Fixed

   * Minor fix in Athena/write_json_to_s3_import_to_athena.py (6b4f76d from @kyhau)

## 2020-06-11

### Added

   * Added README.md (85c9701 from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (932dd52 from @kyhau)
   * Updated .aliases (57bd859 from @kyhau)
   * Refactored lambda_permissions_for_apig.py (4c4932c from @kyhau)

## 2020-06-08

### Changed

   * Supported multiple keywords (93f88ee from @kyhau)
   * Minor refactoring on aws_login.py (e519286 from @kyhau)
   * Refactored _base_file_templates (d8b2023 from @kyhau)
   * Updated aws_login.py help page (d06af09 from @kyhau)

## 2020-06-07

### Changed

   * Refactored search_dynamodb.py (94936eb from @kyhau)
   * Updated _base_file_templates (9714ecc from @kyhau)
   * Refactored deploy_apig_v2.py and make it a standalone script (011539d from @kyhau)
   * Refactored deploy_apig.py and make it a standalone script (3ff4a4c from @kyhau)

### Removed

   * Removed dependency to typer (25ad4f8 from @kyhau)

## 2020-06-06

### Added

   * Added README.md (c3e0771 from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (d0e361e from @kyhau)
   * Updated write_json_to_s3_import_to_athena.py (3b26749 from @kyhau)

## 2020-06-05

### Added

   * Added some simple helper scripts (#42) (9f67913 from @kyhau)
   * Added Security/list_tags.py (9f67913 from @kyhau)
   * Added RDS/database_status_check.py (9f67913 from @kyhau)
   * Added TrustedAdvisor/trusted_advisor_check_result.py (9f67913 from @kyhau)

## 2020-06-03

### Changed

   * Updated TrustedAdvisor/READNE.md (1fd0008 from @kyhau)

## 2020-06-02

### Changed

   * Updated lambda_deploy.py (e6e9b6c from @kyhau)

## 2020-05-29

### Changed

   * Minor update on lambda templates (6c72256 from @kyhau)
   * Updated S3 CF templates (57d8ce7 from @kyhau)
   * Updated S3 sample templates with the LifecycleConfiguration support (76ce390 from @kyhau)

## 2020-05-28

### Added

   * Added MSK/mskconfig.properties (9c4661f from @kyhau)

## 2020-05-26

### Added

   * Added SSM/ssm_parameters_list.sh (#41) (efb41af from @kyhau)

## 2020-05-22

### Added

   * Added packet_loss_testing.sh (0d5dc7b from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (83fded0 from @kyhau)
   * Updated install_network_utilities.sh (b1e844c from @kyhau)

## 2020-05-21

### Added

   * Added install_network_utilities.sh (587b2d6 from @kyhau)

### Removed

   * Removed MSK/requirements.txt (e7e2957 from @kyhau)

## 2020-05-20

### Added

   * Added active-active-multi-cluster-replication notes (8d594f0 from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (10ecf15 from @kyhau)
   * Updated requirements.txt (129a383 from @kyhau)
   * Updated requirements.txt (09bbabb from @kyhau)

## 2020-05-18

### Added

   * Added streaming/cross-cluster-replication.md (ac8231a from @kyhau)

## 2020-05-17

### Added

   * Added RDS/rds-iam-connect.sh (6cd1961 from @kyhau)

## 2020-05-16

### Added

   * Added Useful-tools/load_testing/requirements.txt (a175dc8 from @kyhau)

### Changed

   * Updated check_UserData.py (da8b5c7 from @kyhau)
   * Moved files (5bd07be from @kyhau)

## 2020-05-15

### Changed

   * Refactored MSK scripts (2c29659 from @kyhau)
   * Updated requirements (be6d266 from @kyhau)
   * Updated awscli-v2 install scripts (d23e608 from @kyhau)

## 2020-05-14

### Added

   * Added cdk8s/install_cdk8s.sh (6b16180 from @kyhau)

### Changed

   * Updated saml2aws version (d485e45 from @kyhau)
   * Updated requirements (dac3397 from @kyhau)

## 2020-05-10

### Added

   * Added a simple template for quick scripting (619b3f8 from @kyhau)

## 2020-05-08

### Added

   * Added Useful-tools/install_dotnet.sh (37543da from @kyhau)

### Changed

   * Tried typer (d98a4c0 from @kyhau)
   * Updated simple_with_args.sh (867186a from @kyhau)

## 2020-05-06

### Added

   * Added get_latest_*_ami*.py (64209a6 from @kyhau)

### Changed

   * Updated requirements-cli.txt (470da07 from @kyhau)

## 2020-05-05

### Added

   * Added find_subnet_for_ip.py (63f0a70 from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (721efe2 from @kyhau)

## 2020-05-04

### Added

   * Added MSK/create_topics.py (f8405a8 from @kyhau)

## 2020-05-03

### Added

   * Updated 01_create_msk_cluster.sh (a078ffc from @kyhau)
   * Added 04_setup_prometheus_on_client_amzn2.sh (a9b392b from @kyhau)
   * Updated 01_create_msk_cluster.sh (546f44c from @kyhau)
   * Added 01_create_msk_cluster.py (ee48483 from @kyhau)
   * Added 2 templates for quick scripting (4ce5fed from @kyhau)
   * Added MSK/msk_list_nodes.py (756c575 from @kyhau)
   * Updated 01_create_msk_cluster.sh (e67b9b0 from @kyhau)
   * Updated 02_create_kafka_topic_and_client_properties_on_client_amzn2.sh (4d95788 from @kyhau)
   * Added 03_setup_burrow_on_client_machine.sh (7d04eeb from @kyhau)
   * Updated 02_create_kafka_topic_and_client_properties_at_client_machine.sh (d945d6c from @kyhau)

### Changed

   * Updated 03_setup_burrow_on_client_amzn2.sh (b328fd1 from @kyhau)
   * Updated 03_setup_burrow_on_client_machine.sh (eb7c297 from @kyhau)
   * Test scripts for testing MSK (0e6266f from @kyhau)

## 2020-05-02

### Added

   * Added some util scripts for MSK (c67101b from @kyhau)
   * Added find_ips_in_security_groups.sh (0b1930e from @kyhau)

### Changed

   * Updated .aliases (f27f659 from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/pip-approx-eq-20.1' (be79ec2 from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/coverage-approx-eq-5.1' (daf5839 from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/mock-approx-eq-4.0' (7bcef3a from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/pytest-approx-eq-5.4' (9a1dc42 from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/tox-approx-eq-3.14' (78ac70b from @kyhau)

## 2020-05-01

### Added

   * Added available_ip_address_count.py (98541cc from @kyhau)
   * Added list_vpn_connections.py (0120227 from @kyhau)
   * Added list_security_groups.py (30c6f20 from @kyhau)

### Changed

   * Updated .aliases (312b91d from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/wheel-approx-eq-0.34' into dependabot/pip/_common/virtualenv-approx-eq-20.0 (a0cac9c from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/pytest-cov-approx-eq-2.8' into dependabot/pip/_common/virtualenv-approx-eq-20.0 (d1cf5b1 from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/pytest-mock-approx-eq-3.1' into dependabot/pip/_common/virtualenv-approx-eq-20.0 (02ed4c0 from @kyhau)
   * Merge remote-tracking branch 'origin/dependabot/pip/_common/logilab-common-approx-eq-1.6' into dependabot/pip/_common/virtualenv-approx-eq-20.0 (70ec93b from @kyhau)

## 2020-04-30

### Changed

   * Updated Useful-tools/aws-multi-account-viewer/03-build-frontend.sh (1203f23 from @kyhau)

## 2020-04-29

### Changed

   * Updated EC2-VPC/list_ips_used.py (adad17f from @kyhau)

## 2020-04-28

### Fixed

   * Fixed output file path in Config/query_configservice.py (0f12134 from @kyhau)

## 2020-04-24

### Changed

   * Updated vpc_endpoints and vpc_endpoint_services scripts (a0f5ca7 from @kyhau)
   * Updated saml2aws version (2a1af8c from @kyhau)

## 2020-04-23

### Added

   * Added list_workspaces_connections.py and updated .aliases (89aea63 from @kyhau)

## 2020-04-21

### Changed

   * Updated notes (27a40d7 from @kyhau)

## 2020-04-18

### Changed

   * Updated SecurityHub scripts (4e524a7 from @kyhau)

## 2020-04-09

### Added

   * Added cloudwatch_logs_insights_run_query.py and cloudwatch_logs_insights_list_queries.py (37c9386 from @kyhau)

### Changed

   * Updated install_cdk.sh (9f78099 from @kyhau)
   * Updated InstallGitSecrets.ps1 and Install-AWSSessionManagerPlugin.ps1 (939a7a0 from @kyhau)

## 2020-04-06

### Changed

   * Minor update on lambda_deploy.py to support enabling x-ray (baf0d80 from @kyhau)
   * Minor update on lambda_deploy.py to support enabling x-ray (b1cb1a8 from @kyhau)
   * Minor update on apig_deploy.py to support enabling x-ray (5640857 from @kyhau)

## 2020-04-03

### Added

   * Added athena_query_execution.py (25d6f44 from @kyhau)

### Changed

   * Updated .travis.yml and _common/tox.ini (441d89b from @kyhau)
   * Minor refactoring (#26) (10e6ee0 from @kyhau)

## 2020-04-02

### Added

   * Added CloudTrail/cloudtrail_lookup_events.py (4997b11 from @kyhau)

## 2020-03-29

### Added

   * Added Neptune/import.sh and Neptune/verify.sh (623ff95 from @kyhau)

## 2020-03-23

### Added

   * Added simple script CloudTrail/cloudtrail_lookup_event.sh (6ef335f from @kyhau)

## 2020-03-20

### Added

   * Added GuardDuty/list_findings.py (1d5c412 from @kyhau)

## 2020-03-12

### Changed

   * Renamed file extensions (fbb5271 from @kyhau)
   * Updated sample values in search_inventory.py (9807bb6 from @kyhau)
   * Minor update to custom-ec2processes-document-association.yaml to support keyword with space (b80e1a3 from @kyhau)

## 2020-03-11

### Added

   * Added saml2aws/Troubleshooting.md (7f11403 from @kyhau)

### Changed

   * Updated SSM/CustomInventory/custom-ec2processes-document-association.yaml (a377f00 from @kyhau)
   * Updated ssm agent installation script (ac3039f from @kyhau)

### Fixed

   * Minor fix in search_inventory.py (2369258 from @kyhau)

## 2020-03-07

### Added

   * Added update_stack_with_same_parameters.py (e0d25d5 from @kyhau)

## 2020-03-06

### Changed

   * Sample templates for patching (e60021b from @kyhau)

## 2020-03-04

### Changed

   * Updated the default values in custom-ec2processes-document-association.yaml (443d6a0 from @kyhau)
   * Minor updates (94f5da5 from @kyhau)

## 2020-03-03

### Changed

   * Updated get_inventory.py (faster) (752ccfb from @kyhau)
   * Updated get_inventory.sh (81d688b from @kyhau)

### Removed

   * Removed old file (4eca547 from @kyhau)

## 2020-03-02

### Changed

   * Simple scripts for retrieving inventory for a given "inventory type" (1c4423c from @kyhau)

## 2020-02-27

### Changed

   * Sample templates from AWS TechShift Modernize workshop (34d5393 from @kyhau)

## 2020-02-26

### Changed

   * Updated requirements.txt (b9342ab from @kyhau)
   * Updated requirements.txt (6612992 from @kyhau)

## 2020-02-25

### Changed

   * Updated list_ec2_instances.py (ac4abfa from @kyhau)

## 2020-02-24

### Changed

   * Updated .alias and requirements.txt (d56d1fc from @kyhau)

## 2020-02-20

### Added

   * Added install_ssm_agent.*sh scripts (fc4944f from @kyhau)

## 2020-02-18

### Added

   * Added custom-ec2processes-document-association.yaml (e165c46 from @kyhau)

## 2020-02-12

### Changed

   * Updated .alias (e679198 from @kyhau)
   * Updated .alias (aa38b57 from @kyhau)

## 2020-02-07

### Added

   * Added saml2aws/Install-saml2aws.ps1 (29a59e9 from @kyhau)

## 2020-02-05

### Changed

   * Updated RDS/RDS-PostgresSQL.template.yaml (f7296aa from @kyhau)
   * Updated RDS/list_rds_instances.py (9406b7b from @kyhau)

## 2020-02-04

### Added

   * Added list_ec2_unreachable.py (eff7dc4 from @kyhau)

### Changed

   * Minor cleaned up on list_ec2_instances.py (95ab6f3 from @kyhau)
   * Updated EC2-VPC/list_ec2_unreachable.py (146f938 from @kyhau)
   * Updated RDS/Import-AWS-RDS-CA.ps1 (a5ea2f6 from @kyhau)
   * Updated API/check_aws_apis.py to support checking results on top of status code (51ca40a from @kyhau)

## 2020-02-03

### Added

   * Added Userful-tools/install_serverless.sh (55c561d from @kyhau)
   * Added  EC2-VPC/list_ec2_apps_from_inventory.py (659669c from @kyhau)

### Changed

   * Updated .aliases (0076762 from @kyhau)
   * Updated saml2aws/install_saml2aws.sh (f553636 from @kyhau)
   * Updated RDS/list_ec2_db_instances.py to include subnet name (c46a761 from @kyhau)

## 2020-01-25

### Changed

   * Updated .aliases (270532a from @kyhau)

## 2020-01-23

### Added

   * Added API/check_aws_apis.py (eb4738f from @kyhau)

### Changed

   * Updated  API/check_aws_apis.py (8e7db38 from @kyhau)
   * Updated .aliases (b6cdcca from @kyhau)
   * Updated  API/check_aws_apis.py (3bb00cc from @kyhau)

## 2020-01-22

### Changed

   * Updated list_rds_instances.py (bd68d8e from @kyhau)

## 2020-01-21

### Changed

   * Updated list_ec2_db_instances.py (f1b7580 from @kyhau)
   * Updated list_ec2_db_instances.py (d3615bc from @kyhau)

## 2020-01-20

### Added

   * Added RDS/list_ec2_db_instances.py (e375856 from @kyhau)

### Changed

   * Updated list_rds_instances.py to include printing SingleAZ/MultiAZ (d62464a from @kyhau)

## 2020-01-17

### Changed

   * Updated RDS/list_rds_instances.py (5b4521f from @kyhau)

## 2020-01-16

### Added

   * Added RDS/list_rds_instances.py (e24199a from @kyhau)
   * Added ACM/list_certificates.py (fd361df from @kyhau)
   * Added RDS/Import-AWS-RDS_CA.sh (fcc7df9 from @kyhau)

### Changed

   * Updated list_certificates.py (5b59dcd from @kyhau)
   * Renamed folder from SSO to AWSCLI (d5ec787 from @kyhau)

## 2020-01-15

### Added

   * Added list_ec2_instances.py (311e696 from @kyhau)

### Changed

   * Updated .alias (c2a524a from @kyhau)
   * Updated notes (f93d63e from @kyhau)

## 2020-01-05

### Changed

   * Updated READMD.md (f9854b7 from @kyhau)

## 2019-12-20

### Added

   * Added search_cloudwatch_rds_metrics.sh (0f466ac from @kyhau)
   * Added install_ecs_cli_v2.sh (7a9b244 from @kyhau)

## 2019-12-19

### Changed

   * Updated aws_login.py (b7bc954 from @kyhau)
   * Updated aws_login.py (997405f from @kyhau)
   * Updated aws_login.py (b2d67c8 from @kyhau)
   * Updated aws_login.py (7337ab2 from @kyhau)
   * Updated aws_login.py (e6ae429 from @kyhau)

## 2019-12-18

### Added

   * Added S3/Troubleshoot.md (94d97a3 from @kyhau)

### Changed

   * Updated saml2aws/aws_login.py (44c38ea from @kyhau)

## 2019-12-17

### Changed

   * Updated SSO/install_awscli_v2.sh (f03ff60 from @kyhau)

## 2019-12-13

### Added

   * Added README.md (dec3c6c from @kyhau)

### Changed

   * Updated list_iam_users.py (e805814 from @kyhau)

## 2019-12-12

### Added

   * Minor update on .sh to support additional arguments (e.g. profile) (a2a9572 from @kyhau)

## 2019-12-09

### Changed

   * Updated ls-common-port.md (1c0677b from @kyhau)

## 2019-12-05

### Changed

   * Updated install_eks_metrics_server.sh (30c17b9 from @kyhau)
   * Minor queries cleanup (06e668a from @kyhau)
   * Minor queries cleanup (571034d from @kyhau)
   * Updated ec2 cloudwatch insights queries (06bda74 from @kyhau)

## 2019-12-02

### Changed

   * Updated CloudWatch Logs Insights queries (32b0247 from @kyhau)

## 2019-11-29

### Changed

   * Updated CloudWatch Logs Insights queries (5e5d7f3 from @kyhau)
   * Updated CloudWatch Logs Insights queries (2e457d3 from @kyhau)
   * Updated CloudWatch Logs Insights queries (77cfcb1 from @kyhau)
   * Updated CloudWatch Logs Insights queries (0018df1 from @kyhau)
   * Updated .aliases (50f9ea4 from @kyhau)

## 2019-11-27

### Changed

   * Updated install_saml2aws.sh (4cc975a from @kyhau)

## 2019-11-26

### Added

   * Added simple.ps1 (86a14d2 from @kyhau)

## 2019-11-24

### Changed

   * Updated requirements.txt (f17d1bd from @kyhau)

## 2019-11-22

### Added

   * Added Install-AWSSessionManager.ps1 and Install-AWSTools.ps1 (3081523 from @kyhau)

## 2019-11-21

### Added

   * Addded MaxInstanceLifetime to the template for ECS autoscaling (95a5dd8 from @kyhau)

## 2019-11-12

### Added

   * Added install_awscli_v2.sh (7665379 from @kyhau)

## 2019-11-10

### Changed

   * Updated ECR templates (8159ba8 from @kyhau)

## 2019-11-07

### Added

   * Added sns_subscribe scripts (3412d1d from @kyhau)

### Changed

   * Updated saml2aws version (2774d88 from @kyhau)
   * Udpated aliases (b1078f9 from @kyhau)

## 2019-11-06

### Added

   * Added as simple cdk example of a bucket with kms (6355d79 from @kyhau)
   * Added s3_size.sh (36bbfec from @kyhau)
   * Added EKS setup scripts (#24) (6a94453 from @kyhau)

### Changed

   * Updated SessionManager.md (a74364a from @kyhau)
   * Updated .gitignore (7c0001b from @kyhau)

## 2019-11-05

### Added

   * Added ContainerInsights notes (b4b6f70 from @kyhau)
   * Added sar example (8440eb2 from @kyhau)
   * Added README.md of Lambda layers (#23) (5bc39c9 from @kyhau)
   * Added sam scripts (#22) (1ef9ae0 from @kyhau)

### Changed

   * Minor file reorganisation and cleanup (58907ec from @kyhau)
   * Renamed folder (bb000da from @kyhau)

## 2019-11-04

### Added

   * Added available_ip_address_count.sh (e0a2f90 from @kyhau)
   * Added github-based-sam-codepipeline-cd (#20) (9d191c0 from @kyhau)

### Changed

   * Updated .aliases (cb3da5b from @kyhau)
   * Updated InsightsQueries.md (8ae3102 from @kyhau)
   * Updated list_ips_used.py to handle AuthFailure (#21) (dabed44 from @kyhau)
   * Renamed files (3001d2e from @kyhau)

## 2019-11-01

### Added

   * Added Quickstart-linux-utilities-in-UserData.md (9b8d837 from @kyhau)

### Changed

   * Renamed folders (cd35521 from @kyhau)

## 2019-10-31

### Changed

   * Updated READMD.md (c128504 from @kyhau)
   * Updated requirements.txt (59d0ed2 from @kyhau)

### Fixed

   * Fixed .aliases (869f705 from @kyhau)
   * Updated .aliases and minor fix on cognito.py (22038c3 from @kyhau)

## 2019-10-30

### Changed

   * Renamed .aliases (2760125 from @kyhau)

## 2019-10-29

### Added

   * Added loggroup_put_retention_policy.sh (8b084df from @kyhau)
   * Added setup scripts for Multi-account-viewer (#19) (855d20b from @kyhau)
   * Added sample inspector related functions (7961ec6 from @kyhau)

### Fixed

   * Fixed 03-build-frontend.sh (8a2575a from @kyhau)

## 2019-10-28

### Changed

   * Auto stash before merge of "master" and "origin/master" (65dc5f0 from @kyhau)
   * Updated aliases (1dd9e01 from @kyhau)
   * Updated install_cdk.sh (c7673a9 from @kyhau)

## 2019-10-27

### Added

   * Added installation script for bash_my_aws (#18) (2fc4a85 from @kyhau)
   * Added some general VPC Endpoints templates (#17) (43f1e68 from @kyhau)

### Changed

   * Renamed templates (40fbd36 from @kyhau)

## 2019-10-25

### Changed

   * Updated url-shortener demo code (b1d5f04 from @kyhau)

## 2019-10-24

### Added

   * Added CDK-Group-Policies.yaml (76162f6 from @kyhau)

### Changed

   * Minor clean up on cdk demo code (5b4bbd4 from @kyhau)

## 2019-10-23

### Added

   * Minor update on query_configservice.py, added 3 sql statement files. (#16) (08a5e92 from @kyhau)
   * Added TrustAdvisor/README.md (11add06 from @kyhau)

### Changed

   * dos2unix (166805e from @kyhau)
   * Updated requirements-cli.txt (6bb2e95 from @kyhau)

## 2019-10-22

### Added

   * Added a simple python script to query configservice (#15) (3806cf7 from @kyhau)

### Changed

   * Updated list_amis_used.py (83cfa70 from @kyhau)
   * Updated list_ips_used.py (0d560c8 from @kyhau)
   * Updated aws_login.py (d784f93 from @kyhau)

## 2019-10-21

### Added

   * Added a script to retrieve all IPs  (#14) (aca358c from @kyhau)
   * 1. Added a script list_ips_used.py (aca358c from @kyhau)
   * PrivateIpAddress, PrivateDnsName, IsPrimary, PublicIp, PublicDnsName, InstanceId, Description, AccountId, Region (aca358c from @kyhau)

### Changed

   * 2. Updated arki_common/aws.py to support reading both csv and single-line role files (aca358c from @kyhau)
   * More details (aca358c from @kyhau)
   * Given a profile or a list of role arns, retrieve all IPs currently used in the corresponding account and write them to a csv file (<account_id>_ips_used.csv). (aca358c from @kyhau)
   * Output data: (aca358c from @kyhau)
   * Description is the instance's tag Name if the IP is used by an instance; otherwise it is the ENI description. (aca358c from @kyhau)

## 2019-10-18

### Added

   * Added cloudtrail_lookup_security.sh (52c7f97 from @kyhau)

### Changed

   * Updated aws_login.py to support overriding session duration (#13) (51a0f4f from @kyhau)

## 2019-10-17

### Changed

   * Updated READMD.md (ce7bd91 from @kyhau)
   * Changed workspace path (ce9335b from @kyhau)

## 2019-10-16

### Added

   * Added git_secrets setup scripts (#12) (cb5bed1 from @kyhau)

## 2019-10-14

### Changed

   * Moved file (f990c21 from @kyhau)
   * Updated glacier_to_s3.sh (5dd8384 from @kyhau)

## 2019-10-13

### Added

   * Added a TODO (f06542b from @kyhau)

## 2019-10-11

### Changed

   * Reorganised some files (ecaae86 from @kyhau)

## 2019-10-10

### Added

   * Added glacier_to_s3.sh (8cd99fd from @kyhau)

### Changed

   * Updated aws_login.py (6990fe5 from @kyhau)
   * Renamed install_saml2aws.sh (99b05aa from @kyhau)

### Removed

   * Removed unused line (4820e1a from @kyhau)

## 2019-10-09

### Added

   * Added the init version of url-shortener files (f9a86e3 from @kyhau)

### Changed

   * url-shortener code modified from aws online tech talk (#11) (f9a86e3 from @kyhau)
   * Updated demo files (f9a86e3 from @kyhau)

## 2019-10-08

### Changed

   * Updated requirement files (d46c07c from @kyhau)
   * Updated requirement files (f36f174 from @kyhau)

## 2019-10-07

### Added

   * Added get_secret.py (e9e8840 from @kyhau)

### Changed

   * Updated requirements-cli.txt (a154b4f from @kyhau)

## 2019-10-05

### Added

   * Added PublicAccessBlockConfiguration (9abb5ab from @kyhau)
   * Added a simple script to retrieve all latest AWS managed policies and examples of CloudWatch Insights and CloudTrail queries for quick lookup (#8) (df78968 from @kyhau)
   * Added aws_managed_policies.sh (df78968 from @kyhau)
   * Added a simple script to retrieve all latest AWS managed policies and save them in individual files (df78968 from @kyhau)
   * Added InsightsQueries.md (df78968 from @kyhau)
   * Added CloudTrailQueries.md (df78968 from @kyhau)
   * Added 3 CloudFormation templates (df78968 from @kyhau)

### Changed

   * ECS event handling CF and Lambda templates (#9) (5e8cffd from @kyhau)
   * Put up a list of examples and common CloudWatch Logs Insights queries for quick lookup (df78968 from @kyhau)
   * Put up a list of examples and common CloudTrail queries for quick lookup (df78968 from @kyhau)

### Fixed

   * Fixed cross-account bucket policy and kms policy (#10) (e7ca72b from @kyhau)
   * Fixed cross-account bucket policy and kms policy (e7ca72b from @kyhau)

## 2019-10-03

### Added

   * Added saml2aws/aws_login.py (4e6e054 from @kyhau)
   * Added recreate_stack_with_same_parameters.py (a1729db from @kyhau)

### Changed

   * Minor refactoring of the reusable lambda template code (5b0bfc7 from @kyhau)
   * Updated S3 template (a1c58e7 from @kyhau)

## 2019-10-02

### Added

   * Added a simple lambda template for quick start (abaf642 from @kyhau)

### Changed

   * Sample kms policies (9ed4216 from @kyhau)
   * dos2unix (5bb7f6a from @kyhau)
   * Cross-accounts S3 bucket with KMS (#7) (e1740de from @kyhau)

## 2019-10-01

### Changed

   * Updated simple templates (b3cb884 from @kyhau)

## 2019-09-30

### Added

   * Added CloudFormer.md (933eea6 from @kyhau)
   * Added simple templates (4746725 from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (3c83e24 from @kyhau)
   * dos2unix (7239df5 from @kyhau)

## 2019-09-29

### Added

   * Added packet_sniffing_ob_ec2.sh (82db0fe from @kyhau)
   * Added get_canonical_user_id.sh (262ccc9 from @kyhau)

## 2019-09-26

### Changed

   * Updated aws_metadata (8264cb9 from @kyhau)
   * Updated aws_metadata (e104b78 from @kyhau)

## 2019-09-25

### Added

   * Added _security/README.md (8145a77 from @kyhau)

## 2019-09-24

### Added

   * Added simple lambda template (8dc4e77 from @kyhau)

### Changed

   * Renamed folder (5b25bb8 from @kyhau)

## 2019-09-23

### Changed

   * Updated the filter in change_ec2_instance_type_started_by_asg.sh (d40b9e8 from @kyhau)

## 2019-09-22

### Changed

   * Renamed folder (091474a from @kyhau)
   * Simple examples for updating policies (560a707 from @kyhau)

## 2019-09-21

### Added

   * Added whoami_filter.py (514174a from @kyhau)
   * Added change_ec2_instance_type_started_by_asg.sh (893cd1a from @kyhau)
   * Added get_latest_eks_optimized_ami.sh (363b620 from @kyhau)
   * Added list_stacks.py (2c68ac5 from @kyhau)
   * Added Step Functions templates (b6f5374 from @kyhau)

### Changed

   * Updated check_UserData.py (51c84a4 from @kyhau)
   * Updated decode_UserData.py (7a387c6 from @kyhau)
   * Updated whoami_filter_restricted.txt (a1cb540 from @kyhau)
   * Updated whoami.py and .gitignore (086e349 from @kyhau)
   * Renamed folders (81acf61 from @kyhau)

## 2019-09-19

### Added

   * Added list_stacks.py (190703e from @kyhau)
   * Added SF template (618152a from @kyhau)
   * Added change_ec2_instance_type_started_by_asg.sh (759341e from @kyhau)
   * Added AMI/get_latest_eks_optimized_ami.sh (1b6a454 from @kyhau)

### Changed

   * Merge remote-tracking branch 'origin/master' (238a595 from @kyhau)

### Removed

   * Delete whoami.json (8c1a747 from @kyhau)

## 2019-09-17

### Added

   * Added a simple example to attach ScheduledAction to a ASG (a46d2bf from @kyhau)

## 2019-09-16

### Added

   * Added list_iam_users.py (f8ecbd2 from @kyhau)
   * Added account_authorization_details.py (f8ecbd2 from @kyhau)
   * Added whoami.py (f8ecbd2 from @kyhau)

### Changed

   * Minor updates (#6) (f8ecbd2 from @kyhau)
   * Updated list_amis_used.py (f8ecbd2 from @kyhau)
   * Updated list_s3_buckets.py (f8ecbd2 from @kyhau)
   * Updated list_accounts.py (f8ecbd2 from @kyhau)

## 2019-09-14

### Added

   * Added list_all_accounts.py (be48ed0 from @kyhau)
   * Added list_s3_buckets_in_all_accounts.py (be48ed0 from @kyhau)
   * Added list_AMIs_used_in_all_accounts.py (be48ed0 from @kyhau)

### Changed

   * Minor updates (#5) (be48ed0 from @kyhau)
   * Updated requirements files (be48ed0 from @kyhau)
   * Updated assume role scripts (be48ed0 from @kyhau)

## 2019-09-12

### Changed

   * Renamed folder (869072f from @kyhau)
   * Updated install_nimbostratus.sh (30f6d56 from @kyhau)

## 2019-09-11

### Added

   * Added installation scripts for some useful tools (5f86855 from @kyhau)

## 2019-09-08

### Added

   * Added notes (#4) (f8f857f from @kyhau)
   * Added IAM/saml2aws/setup_saml2aws.sh (f8f857f from @kyhau)
   * Added install_session_manager_plugin.sh (f8f857f from @kyhau)
   * Added start_dynamodb_local_docker.sh (f8f857f from @kyhau)
   * Added SessionManager.md (f8f857f from @kyhau)
   * Added EC2InstanceConnect.md (f8f857f from @kyhau)

## 2019-09-01

### Added

   * Added local scripts (cdc574b from @kyhau)

## 2019-08-28

### Added

   * Added local scripts (8175f27 from @kyhau)

### Changed

   * Updated notes (9d89a57 from @kyhau)
   * Updated requirements (3651cd0 from @kyhau)

## 2019-08-27

### Added

   * Added some CF templates (d9ba653 from @kyhau)
   * Added start_dynamodb_local.sh (5734a8e from @kyhau)

## 2019-08-26

### Added

   * Added some local tools (#3) (24ca3c0 from @kyhau)

## 2019-03-22

### Changed

   * Minor update (d7b94ed from @kyhau)
   * Sync with base repo (3ed05e9 from @kyhau)

## 2019-02-11

### Changed

   * Updated to use toml and functools.wraps (#2) (6e28d02 from @kyhau)

## 2018-11-06

### Changed

   * Updated.gitignore (cf0ef25 from @kyhau)

## 2018-09-04

### Fixed

   * lambda_deploy: Minor fixed on retrieving the setting "aws.lambda.kmskey.arn" not existing in the ini file (d4a8850 from @kyhau)

## 2018-09-03

### Added

   * Added lambda_deploy.py (705aba7 from @kyhau)

### Changed

   * Cleanup (8650e87 from @kyhau)

## 2018-07-13

### Changed

   * Updated dynamdodb.py (5a7a6a8 from @kyhau)
   * Updated dynamdodb.py (5f9d111 from @kyhau)
   * Supported aws.profile in cognito.py (79e01d2 from @kyhau)
   * Updated cognito.list_all_users (c11a8bb from @kyhau)

## 2018-07-05

### Added

   * Added arki/aws/cognito.py (1ca492b from @kyhau)

## 2018-06-14

### Changed

   * Set up API Gateway data trace, logging level and metrics logging (d8b0e4d from @kyhau)

## 2018-06-05

### Changed

   * Separate list_task_definition and detail (bb4a943 from @kyhau)

## 2018-06-04

### Added

   * Added dockerc and dockeri (4e2d14e from @kyhau)

## 2018-06-03

### Added

   * Added aws_ecs* (ab13fbf from @kyhau)
   * Added aws_ddb (15895fd from @kyhau)
   * Added aws_lambda_permissions_to_apig - adding Lambda Permissions for API Gateway resources (3bfda1a from @kyhau)
   * Added deploy_apig (c139859 from @kyhau)

### Changed

   * Support update base ini file (0671177 from @kyhau)

## 2018-06-02

### Added

   * Added venv (d199af9 from @kyhau)
   * Added arki tool list (9fd14a1 from @kyhau)
   * Added profiles and env_variable_store (e265cab from @kyhau)

### Changed

   * Clean up (c1bbe75 from @kyhau)
