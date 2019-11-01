# Quick Start Linux utilities
Quick Start Linux utilities provide a simple and easy way to automate the installation of AWS CloudFormation tools
across common Linux distributions.

Note that AWS conveniently provides a Linux distribution called Amazon Linux, which has this utility built-in.

Git repo: https://github.com/aws-quickstart/quickstart-linux-utilities

For details, see https://aws.amazon.com/blogs/infrastructure-and-automation/introduction-to-quickstart-linux-utilities/


```
UserData: !Base64
  Fn::Sub:
    - |
      #!/bin/bash -x
      until git clone https://github.com/aws-quickstart/quickstart-linux-utilities.git; do echo "Retrying"; done
      cd /quickstart-linux-utilities
      source quickstart-cfn-tools.source
      qs_update-os || qs_err
      qs_bootstrap_pip || qs_err
      qs_aws-cfn-bootstrap || qs_err
```