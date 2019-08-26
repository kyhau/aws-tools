#!/usr/bin/env bash

#curl -H "Origin: http://example.com" --head https://fondservice.biarrinetworks.com/api/projects?projectid=6b1bdac4-69fb-478a-b101-15ff8ea91818

#curl -H "Origin: http://example.com" \
#  -H "Access-Control-Request-Method: GET" \
#  -H "Access-Control-Request-Headers: X-Requested-With" \
#  -X GET --verbose \
#  https://fondservice.biarrinetworks.com/api/projects?projectid=6b1bdac4-69fb-478a-b101-15ff8ea91818

curl -H "Origin: http://example.com" \
-H "Access-Control-Request-Method: GET" \
-H "Access-Control-Request-Headers: Origin, Accept, Content-Type" \
--X OPTIONS --verbose \
https://fondservice.biarrinetworks.com/api