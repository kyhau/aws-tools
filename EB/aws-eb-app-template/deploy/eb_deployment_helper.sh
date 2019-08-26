#!/bin/bash

# Set to fail script if any command fails.
set -e

# Define constants
SCRIPT_DIR=$(dirname $(realpath $0))
APP_DIR=$(dirname ${SCRIPT_DIR})/app
PYTHON_VERSION=python3.6
APP_NAME=sample_service
DOCKER_REPO="khau/${APP_NAME}"
EB_REGION=ap-southeast-2

# Cleanup hack at the end
function finish {
  [[ -f ${APP_DIR}/Dockerrun.aws.json ]] && rm ${APP_DIR}/Dockerrun.aws.json
  cd ${SCRIPT_DIR}
  echo "goodbye"
}
trap finish EXIT

# Define the help menu
help_menu() {
  echo "Usage:
  ${0##*/}
    --build-image                Build/test docker image.
    --build-number BUILD_NUMBER  The build number to uniquely identify the image we build. Default to 000.
    --push-image                 Push a copy of the versioned Docker image (from --build-image) to Docker registry.
    --eb-config-update           Run eb command to update EB environment of EB_ENV_NAME (on After Creation).
    --eb-deploy                  Run eb command to deploy an application using Dockerrun.aws.json.
    --eb-deploy-tag DEPLOY_IMAGE_TAG
                                 Deploy the application image of the given image version. Default to current version.
    --eb-env EB_ENV_NAME         EB environment: [SampleService|SampleService-staging|SampleService-dev]
  "
  exit
}

# Parse arguments
DO_DOCKER_BUILD=false
DO_DOCKER_PUSH=false
DO_EB_DEPLOY=false
DO_EB_CONFIG_UPDATE=false
BUILD_NUMBER="000"

while [[ "$#" > 0 ]]; do case $1 in
    --build-image)       DO_DOCKER_BUILD=true                     ;;
    --build-number)      BUILD_NUMBER="${2}"              ; shift ;;
    --push-image)        DO_DOCKER_PUSH=true                      ;;
    --eb-env)            EB_ENV_NAME="${2}"               ; shift ;;
    --eb-config-update)  DO_EB_CONFIG_UPDATE=true                 ;;
    --eb-deploy)         DO_EB_DEPLOY=true                        ;;
    --eb-deploy-tag)     DEPLOY_IMAGE_TAG="${2}"          ; shift ;;
    -h|--help)           help_menu                                ;;
    *)                   echo "Invalid option: ${1}" && help_menu ;;
esac; shift; done

function missed_var_error {
  [[ ! -z "$3" ]] || (echo "CHECK_POINT: $1 $2 is not provided. Exit now." && exit 1)
}

####################################################################################################
# Prepare virtualenv for building the application image

cd ${APP_DIR}
virtualenv -p ${PYTHON_VERSION} env_container
. env_container/bin/activate
python -m pip install -e .

# Default APP_VERSION is the version in the repo
APP_VERSION=`python -c "import pkg_resources; print(pkg_resources.get_distribution('${APP_NAME}').version)"`

deactivate    # env_container

####################################################################################################
# Check arguments and environment variables

if [[ "$DO_DOCKER_BUILD" = true ]] ||  [[ "$DO_EB_DEPLOY" = true ]] ; then
  value_type="Env-variable"
  missed_var_error ${value_type} "PIP_INDEX_URL" ${PIP_INDEX_URL}

  DEV_TAG="${DOCKER_REPO}:${APP_VERSION}_BUILD${BUILD_NUMBER}"   # local image tag
  VERSION_TAG="${DOCKER_REPO}:${APP_VERSION}"                    # actual image tag to be pushed to docker registry
fi
if [[ "$DO_EB_DEPLOY" = true ]] || [[ "$DO_EB_CONFIG_UPDATE" = true ]] ; then
  missed_var_error "Argument" "EB_ENV_NAME" ${EB_ENV_NAME}

  case "$EB_ENV_NAME" in
    SampleService)         STAGE_TAG=$VERSION_TAG              ;;
    SampleService-dev)     STAGE_TAG="${DOCKER_REPO}:dev"      ;;
    SampleService-staging) STAGE_TAG="${DOCKER_REPO}:staging"  ;;
    *)                    (echo "CHECK_POINT: Invalid EB_ENV_NAME: $EB_ENV_NAME. Exit now." && exit 1) ;;
  esac

  cd ${SCRIPT_DIR}
  virtualenv -p ${PYTHON_VERSION} env_eb_update
  . env_eb_update/bin/activate
  python -m pip install -r requirements-deploy.txt
  deactivate    # env_eb_update
fi
if [[ ! -z ${DEPLOY_IMAGE_TAG} ]]; then
  VERSION_TAG=${DEPLOY_IMAGE_TAG}
  STAGE_TAG=${DEPLOY_IMAGE_TAG}
fi

####################################################################################################
# Build and test docker image

if [[ "$DO_DOCKER_BUILD" = true ]] ; then
  echo "################################################################################"
  echo "CHECK_POINT: Started building docker image for testing"

  cd ${APP_DIR}

  echo "CHECK_POINT: Build image ${DEV_TAG}"
  docker build -t ${DEV_TAG} \
    --build-arg PIP_INDEX_URL=${PIP_INDEX_URL} \
    -f Dockerfile.base .

  echo "CHECK_POINT: Start the image tests using a container"

  # Sanity check to make sure gunicorn can be called. We call it with no arguments
  # and expect to receive the error message "No application module specified"
  docker run --rm "${DEV_TAG}" pserve 2>&1 | grep "No application module specified"
  [[ $? -eq 0 ]] || (echo "CHECK_POINT: Docker image test failed. Exit now." && exit 1)

  echo "CHECK_POINT: Docker image test passed."

  docker tag ${DEV_TAG} ${VERSION_TAG}

  if [[ "$DO_DOCKER_PUSH" = true ]] ; then
    echo "CHECK_POINT: Push image ${VERSION_TAG}"
    ( docker push "${VERSION_TAG}" && send_email "${VERSION_TAG}" ) || echo "Failure: ${VERSION_TAG} push failed."
  fi

  # Cleanup dev image once we're done
  docker rmi ${DEV_TAG}
fi

####################################################################################################
# Recreate EB resources

if [[ "$DO_EB_CONFIG_UPDATE" = true ]] ; then
  echo "################################################################################"
  echo "CHECK_POINT: Started running eb config update - this may recreate some AWS resources"

  . ${SCRIPT_DIR}/env_eb_update/bin/activate
  cd ${APP_DIR}

  eb use ${EB_ENV_NAME}
  eb config --region $EB_REGION --cfg ${EB_ENV_NAME}

  deactivate    # env_eb_update
fi

####################################################################################################
# Deploy application to EC2s

if [[ "$DO_EB_DEPLOY" = true ]] ; then
  echo "################################################################################"
  echo "CHECK_POINT: Started running eb deploy - this will deploy application and update any settings within the EC2s"

  . ${SCRIPT_DIR}/env_eb_update/bin/activate
  cd ${APP_DIR}

  echo "CHECK_POINT: Pull image if it does not exist locally"
  [[ ! -z $(docker images -q ${VERSION_TAG}) ]] || docker pull ${VERSION_TAG}

  if [[ ${VERSION_TAG} != ${STAGE_TAG} ]]; then
    # Use a "stage" tag instead of a version tag

    echo "CHECK_POINT: Tag image ${VERSION_TAG} with ${STAGE_TAG}"
    docker tag ${VERSION_TAG} ${STAGE_TAG}

    echo "CHECK_POINT: Push image ${STAGE_TAG}"
    docker push ${STAGE_TAG} || echo "Failure: ${STAGE_TAG} push failed."
  fi

  export SAMPLE_SERVICE_STAGE_TAG=${STAGE_TAG}
  export SAMPLE_SERVICE_CONFIG_FILE=${SAMPLE_SERVICE_CONFIG_FILE}

  echo "CHECK_POINT: Create Dockerrun.aws.json with ${SAMPLE_SERVICE_STAGE_TAG}"
  cat Dockerrun.aws.json.template | envsubst > Dockerrun.aws.json

  time eb deploy --region $EB_REGION $EB_ENV_NAME

  # Cleanup local images
  docker rmi ${VERSION_TAG} ${STAGE_TAG}

  deactivate    # env_eb_update
fi
