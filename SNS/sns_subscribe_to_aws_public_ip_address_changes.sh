#!/bin/bash

email_address=todo

aws sns subscribe --topic-arn arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged --protocol email --notification-endpoint "${email_address}"

