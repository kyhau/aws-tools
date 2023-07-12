#!/bin/bash

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue="$@" \
  --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,resource:(Resources[0].ResourceName)}' \
  --output table --region ap-southeast-2

# Events from the past 90 days are available for lookup. To specify a time range, type the following command:
# --start-time <timestamp> --end-time <timestamp>
#
# Valid time format
# 1422317782
# 1422317782.0
# 01-27-2015
# 01-27-2015,01:16PM
# "01-27-2015, 01:16 PM"
# "01/27/2015, 13:16"
# 2015-01-27
# "2015-01-27, 01:16 PM"
