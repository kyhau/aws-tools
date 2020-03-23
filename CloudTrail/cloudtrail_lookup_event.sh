#!/bin/bash

aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue="$@" \
  --query 'Events[].{username:Username,time:EventTime,event:EventName,eventid:EventId,resource:(Resources[0].ResourceName)}' \
  --output table --region ap-southeast-2
