#!/bin/bash

email_address=todo

aws sns subscribe --topic-arn arn:aws:sns:us-west-2:177427601217:ecs-optimized-amazon-ami-update --protocol email --notification-endpoint "${email_address}"
