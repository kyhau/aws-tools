#!/bin/bash

# Set to fail script if any command fails.
set -e

# Define constants
SCRIPT_DIR=$(dirname $(realpath $0))

# Cleanup hack at the end
function finish {
  # Delete any tmp file
  [[ -f tmp.json ]] && rm tmp.json
  echo "Goodbye"
}
trap finish EXIT

# Define the help menu
help_menu() {
  echo "Usage:
  ${0##*/}
    --build-image                Build/test docker image.
    --build-number BUILD_NUMBER  The build number to uniquely identify the image we build. Default to 000.
  "
  exit
}

# Parse arguments
DO_BUILD=false

while [[ "$#" > 0 ]]; do case $1 in
    --build-image)       DO_BUILD=true                     ;;
    --build-number)      BUILD_NUMBER="${2}"       ; shift ;;
    -h|--help)           help_menu                         ;;
    *)                   echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

[[ ! -z "$BUILD_NUMBER" ]] || (echo "Error: BUILD_NUMBER is not provided. Aborted." && exit 1)

