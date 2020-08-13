# EC2 / VPC

- CloudWatch Agent
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent-New-Instances-CloudFormation.html
        - append_dimensions, AutoScalingGroupName
        - metrics_collected, mem_used_percent, swap_used_percent
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-common-scenarios.html
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AgentReference.html
    - https://stackoverflow.com/questions/55098841/cloudformation-output-of-cloudformation-init


- Quick Start Linux utilities
    - Quick Start Linux utilities provide a simple and easy way to automate the installation of AWS CloudFormation tools across common Linux distributions.
    - Note that AWS conveniently provides a Linux distribution called Amazon Linux, which has this utility built-in.
    - Git repo: https://github.com/aws-quickstart/quickstart-linux-utilities
    - For details, see https://aws.amazon.com/blogs/infrastructure-and-automation/introduction-to-quickstart-linux-utilities/

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


- EC2 Instance Connect
    - There is no need to install the EC2 Instance Connect CLI if users only use the console or an SSH client to connect to an instance. 

    ```
    ################################################################################
    # Install CLI
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-set-up.html#ec2-instance-connect-install-eic-CLI
    
    pip install ec2instanceconnectcli
    
    # SSH connection to an instance
    ssh <instance_id>
    ```