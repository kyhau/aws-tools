#!/bin/bash

aws ec2 describe-regions --query Regions[*].[RegionName] --output text