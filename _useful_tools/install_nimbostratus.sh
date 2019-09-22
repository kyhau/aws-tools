#!/bin/bash
# https://github.com/andresriancho/nimbostratus

git clone git@github.com:andresriancho/nimbostratus.git
cd nimbostratus

mkvirtualenv nimbostratus -p python2.7
pip install -r requirements.txt
