#!/bin/bash
# https://github.com/NetSPI/aws_consoler/
# A utility to convert your AWS CLI credentials into AWS console access.

git clone git@github.com:NetSPI/aws_consoler.git
cd aws_consoler

# TODO - update the python version in setup.py

mkvirtualenv aws_consoler

make install
