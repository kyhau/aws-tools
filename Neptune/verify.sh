#!/bin/bash

loadId="4169b07e-f123-6222-1d2f-123456789012"

curl -G 'https://my-neptune-database.xxxxxx.us-east-1.neptune.amazonaws.com:8182/loader/${loadId}'
