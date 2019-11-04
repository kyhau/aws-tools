#!/bin/bash
# Set to fail script if any command fails.
set -e

# build the layer from scratch
make layer-build

# package and deploy the layer with `SAM` CLI
make sam-layer-package sam-layer-deploy

# destroy the layer
make sam-layer-destroy

