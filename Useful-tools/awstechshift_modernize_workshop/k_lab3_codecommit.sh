#!/bin/bash
# Set to fail script if any command fails.
set -e

aws codecommit create-repository --repository-name TSAGallery-SPA --region ap-southeast-1

aws codecommit create-repository --repository-name TSAGallery-API --region ap-southeast-1

