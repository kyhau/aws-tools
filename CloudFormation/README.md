# CloudFormation (CFN) Notes

- [Useful CLIs, Libs and Tools](#useful-clis-libs-and-tools)
- [Useful templates](#useful-templates)
- [CFN Customer Resource Provider Plugins](#cfn-custom-resource-provider-plugins-and-custom-resources)
- [CFN Extensions](#cfn-extensions)
- [CFN Marcos](#cfn-marcos)
- [CFN Syntax](#cfn-syntax)

---
## Useful CLIs, Libs and Tools

- `cfn`: CloudFormation CLI. [aws-cloudformation/aws-cloudformation-cli](https://github.com/aws-cloudformation/cloudformation-cli)

- `cfn-flip`: converts CloudFormation templates between JSON and YAML formats. [awslabs/aws-cfn-template-flip](https://github.com/awslabs/aws-cfn-template-flip)

- `cfn-format`: reads in an existing CloudFormation template and outputs a cleanly-formatted, easy-to-read copy of the same template adhering to standards as used in AWS documentation. [awslabs/aws-cloudformation-template-formatter](https://github.com/awslabs/aws-cloudformation-template-formatter)

- `cfn-guard`: provides developers a general purpose domain-specific language (DSL) to express policy-as-code and then validate their JSON- and YAML-formatted data against that code. [aws-cloudformation/cloudformation-guard](https://github.com/aws-cloudformation/cloudformation-guard)

- `cfn-lint`: validates CloudFormation yaml/json templates against the CloudFormation spec and additional checks. [aws-cloudformation/cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint)
  - Blog post - [CloudFormation Linter (cfn-lint) v1](https://aws.amazon.com/blogs/devops/aws-cloudformation-linter-v1/), AWS, 2024-06-19

- `cfn_nag`: looks for patterns in CloudFormation templates that may indicate insecure infrastructure. [stelligent/cfn_nag](https://github.com/stelligent/cfn_nag)

- `cfn-policy-validator`: A command line tool that takes a CloudFormation template, parses the IAM policies attached to IAM roles, users, groups, and resources then runs them through IAM Access Analyzer validation checks. [aws-cloudformation-iam-policy-validator](https://github.com/awslabs/aws-cloudformation-iam-policy-validator)

- `cfn-skeleton`: consumes the published CloudFormation specification and generates skeleton CloudFormation templates with mandatory and optional parameters of chosen resource types pre-filled with placeholder values. [cfn-skeleton](https://github.com/awslabs/aws-cloudformation-template-builder)

- `rain`: a CLI tool for working with CloudFormation templates and stacks. [aws-cloudformation/rain](https://github.com/aws-cloudformation/rain)

- `sceptre`: manages the creation, update and deletion of stacks while providing meta commands which allow users to retrieve information about their stacks. [sceptre](https://sceptre.cloudreach.com/)

- `taskcat`: tests CloudFormation templates. It deploys your CloudFormation template in multiple AWS Regions and generates a report with a pass/fail grade for each region. taskcat is implemented as a Python class that you import, instantiate, and run. [aws-quickstart/taskcat](https://github.com/aws-quickstart/taskcat)

- [CloudFormer](https://aws.amazon.com/blogs/devops/building-aws-cloudformation-templates-using-cloudformer/)
 (beta): creates CloudFormation templates from existing AWS resources.

- [CloudMapper](https://github.com/duo-labs/cloudmapper): analyzes AWS environments, supports auditing for security issues. [duo-labs/cloudmapper](https://github.com/duo-labs/cloudmapper)

- [Former2]((https://github.com/iann0036/former2)): generates CloudFormation / Terraform / Troposphere templates from existing AWS resources. [iann0036/former2](https://github.com/iann0036/former2)

- CloudFormation Region parity: handles Region parity with IaC. [aws-samples/aws-cloudformation-region-parity](https://github.com/aws-samples/aws-cloudformation-region-parity)


---
## Useful Templates

- AWS predefined CloudWatch metric filters and alarms
  ([CloudWatch_Alarms_for_CloudTrail_API_Activity.zip](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/samples/CloudWatch_Alarms_for_CloudTrail_API_Activity.zip)). See also [User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/use-cloudformation-template-to-create-cloudwatch-alarms.html).

- CloudFormation Resources and Projects: [aws-cloudformation/awesome-cloudformation](https://github.com/aws-cloudformation/awesome-cloudformation)


---
## CFN Extensions

- In order to use a public third-party extension in your template, you must first activate the extension for the account and region where we need to use it.
   - You may want to keep track of source account IDs, environment levels for data tracking, labelling, alarm severities and retention purposes etc.

---
## CFN Custom Resource Provider Plugins and Custom Resources

- CloudFormation Resource Provider Python Plugin - [aws-cloudformation/cloudformation-cli-python-plugin](https://github.com/aws-cloudformation/cloudformation-cli-python-plugin)

- `AWSUtility::CloudFormation::CommandRunner`: this resource allows users to run Bash commands in any CloudFormation stack. [aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner](https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner)


---
## CFN Hooks

- `Generic::SecretsProtection::Hook`: protects against accidental secrets exposure by observing every property of every AWS resource type.
  [iann0036/cfn-hook](https://github.com/iann0036/cfn-hooks/tree/main/Generic-SecretsProtection-Hook)


---
## CFN Marcos

- [aws-cloudformation/aws-cloudformation-macros](https://github.com/aws-cloudformation/aws-cloudformation-macros): examples of AWS CloudFormation macros.


---
## CFN Syntax

- [Understanding CloudFormation !Sub Syntax](https://www.fischco.org/technica/2017/cloud-formation-sub/)

- [How do I use the Fn::Sub function in AWS CloudFormation with Fn::FindInMap, Fn::ImportValue, or other supported functions?](https://repost.aws/knowledge-center/cloudformation-fn-sub-function)

- Passing value to UserData to set EC2 env variable https://stackoverflow.com/questions/54858072/aws-cloudformation-userdata-ec2-environment-variable
    ```
    UserData:
      Fn::Base64: !Sub |
        #!/bin/bash
        sudo yum install -y https://s3.${AWS::Region}.amazonaws.com/amazon-ssm-${AWS::Region}/latest/linux_amd64/amazon-ssm-agent.rpm
    ```

- Example: optional item in a list
    ```
    Parameters:
      TargetRole:
        Type: String
      TargetRole2:
        Type: String
        Default: ""

    Conditions:
      HasTargetRole2: !Not [!Equals [!Ref TargetRole2, ""]]

    Resources:
      CIDeployRole:
        Type: AWS::IAM::Role
        Properties:
          AssumeRolePolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action: sts:AssumeRole
                Effect: Allow
                Principal:
                  AWS:
                    - !Ref TargetRole
                    - !If
                      - HasTargetRole2
                      - !Ref TargetRole2
                      - !Ref AWS::NoValue
    ```
