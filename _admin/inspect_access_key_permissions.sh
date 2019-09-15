#!/bin/bash

access_key=
secret_key=

workon nimbostratus

nimbostratus dump-permissions --access-key=${access_key} --secret-key=${secret_key}