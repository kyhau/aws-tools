#!/bin/bash

aws s3 ls --summarize --human-readable --recursive s3://"$@"