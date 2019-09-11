#!/bin/bash
# https://github.com/RhinoSecurityLabs/pacu

git clone git@github.com:RhinoSecurityLabs/pacu.git
cd pacu

mkvirtualenv pacu
pip install -r requirements.txt
