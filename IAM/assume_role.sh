#!/bin/bash

aws sts assume-role --role-arn "arn:aws:iam::123456789012:role/DEV-01" --role-session-name "K2-DEV-01"
