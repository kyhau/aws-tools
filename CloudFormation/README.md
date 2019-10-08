# Useful tools

* [AWS CloudFormer](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cloudformer.html)
 (beta) - creates AWS CloudFormation templates from existing AWS resources.

* [cfn-flip](https://github.com/awslabs/aws-cfn-template-flip) - 
  converts AWS CloudFormation templates between JSON and YAML formats, making use of the YAML format's short function
  syntax where possible.
  - `pip install cfn_flip`

* [cfn-format](https://github.com/awslabs/aws-cloudformation-template-formatter) -
  reads in an existing AWS CloudFormation template and outputs a cleanly-formatted, easy-to-read copy of the same
  template adhering to standards as used in AWS documentation.

* [cfn-lint](https://github.com/aws-cloudformation/cfn-python-lint) -
  validates CloudFormation yaml/json templates against the CloudFormation spec and additional checks. 
  - `pip install cfn-lint`

* [cfn-nag](https://github.com/stelligent/cfn_nag) -
  looks for patterns in CloudFormation templates that may indicate insecure infrastructure.

* [cfn-skeleton](https://github.com/awslabs/aws-cloudformation-template-builder) -
  consumes the published CloudFormation specification and generates skeleton CloudFormation templates with mandatory
  and optional parameters of chosen resource types pre-filled with placeholder values.

* [sceptre](https://sceptre.cloudreach.com/) -
  manages the creation, update and deletion of stacks while providing meta commands which allow users to retrieve
  information about their stacks.

* [taskcat](https://github.com/aws-quickstart/taskcat) -
  tests AWS CloudFormation templates. It deploys your AWS CloudFormation template in multiple AWS Regions and
  generates a report with a pass/fail grade for each region.
  taskcat is implemented as a Python class that you import, instantiate, and run.

