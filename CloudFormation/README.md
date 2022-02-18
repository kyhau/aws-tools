# CloudFormation Notes

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [CDN Syntax](#cfn-syntax)

---
## Useful Libs and Tools

| Description | Repo/Link |
| :--- | :--- |
| `cfn` - AWS CloudFormation CLI | [aws-cloudformation/aws-cloudformation-cli](https://github.com/aws-cloudformation/cloudformation-cli) |
| `cfn-guard` - AWS CloudFormation Guard | [aws-cloudformation/cloudformation-guard](https://github.com/aws-cloudformation/cloudformation-guard) |
| AWS CloudFormation Handling Region parity| [aws-samples/aws-cloudformation-region-parity](https://github.com/aws-samples/aws-cloudformation-region-parity) |
| `cfn-lint` - AWS CloudFormation Linter | [aws-cloudformation/cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint) |
| AWS CloudFormation Macros | [aws-cloudformation/aws-cloudformation-macros](https://github.com/aws-cloudformation/aws-cloudformation-macros) |
| AWS CloudFormation Registry (public/private extensions/modules) | [User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) |
| AWS CloudFormation Resource Provider Python Plugin | [aws-cloudformation/cloudformation-cli-python-plugin](https://github.com/aws-cloudformation/cloudformation-cli-python-plugin) |
| AWS CloudFormation Resources and Projects | [aws-cloudformation/awesome-cloudformation](https://github.com/aws-cloudformation/awesome-cloudformation) |
| AWS CloudFormation Sample Templates | [awslabs/aws-cloudformation-templates](https://github.com/awslabs/aws-cloudformation-templates) |
| AWS CloudFormation Template Flip (cfn-flip) | [awslabs/aws-cfn-template-flip](https://github.com/awslabs/aws-cfn-template-flip) |
| [AWS predefined CloudWatch metric filters and alarms](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/use-cloudformation-template-to-create-cloudwatch-alarms.html) |[CloudWatch_Alarms_for_CloudTrail_API_Activity.zip](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/samples/CloudWatch_Alarms_for_CloudTrail_API_Activity.zip)|
| AWSUtility::CloudFormation::CommandRunner | [aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner](https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-awsutilities-commandrunner) |
| CloudMapper | [duo-labs/cloudmapper](https://github.com/duo-labs/cloudmapper) |
| CloudFormer | [CloudFormer for creating templates from existing AWS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html) |
| Former2 generates CloudFormation / Terraform / Troposphere templates from existing AWS resources | [iann0036/former2](https://github.com/iann0036/former2) |

---
## Useful Articles and Blogs

- [AWS CloudFormer](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html)
 (beta) - creates AWS CloudFormation templates from existing AWS resources.

- `cfn-flip` [awslabs/aws-cfn-template-flip](https://github.com/awslabs/aws-cfn-template-flip) -
  converts AWS CloudFormation templates between JSON and YAML formats, making use of the YAML format's short function
  syntax where possible.
  - `pip install cfn_flip`

- cfn-format [awslabs/aws-cloudformation-template-formatter](https://github.com/awslabs/aws-cloudformation-template-formatter) -
  reads in an existing AWS CloudFormation template and outputs a cleanly-formatted, easy-to-read copy of the same template adhering to standards as used in AWS documentation.

- `cfn-lint` [aws-cloudformation/cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint) -
  validates CloudFormation yaml/json templates against the CloudFormation spec and additional checks.
  - `pip install cfn-lint`

- [stelligent/cfn_nag](https://github.com/stelligent/cfn_nag) -
  looks for patterns in CloudFormation templates that may indicate insecure infrastructure.

- [cfn-skeleton](https://github.com/awslabs/aws-cloudformation-template-builder) -
  consumes the published CloudFormation specification and generates skeleton CloudFormation templates with mandatory and optional parameters of chosen resource types pre-filled with placeholder values.

- [sceptre](https://sceptre.cloudreach.com/) -
  manages the creation, update and deletion of stacks while providing meta commands which allow users to retrieve
  information about their stacks.

- [aws-quickstart/taskcat](https://github.com/aws-quickstart/taskcat) -
  tests AWS CloudFormation templates. It deploys your AWS CloudFormation template in multiple AWS Regions and
  generates a report with a pass/fail grade for each region.
  taskcat is implemented as a Python class that you import, instantiate, and run.

---
## CFN Syntax

- [Understanding AWS CloudFormation !Sub Syntax](https://www.fischco.org/technica/2017/cloud-formation-sub/)

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
