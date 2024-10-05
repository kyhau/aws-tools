export ENV ?= dev

ROOT_PATH := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../)
ENV_FILE := $(ROOT_PATH)/environment/$(ENV).yaml

export AWS_REGION=$(shell grep AWS_REGION $(ENV_FILE) | awk -F ': ' '{print($$2)}')
export DOMAIN_NAME=$(shell grep DOMAIN_NAME $(ENV_FILE) | awk -F ': ' '{print($$2)}')
export DOMAIN_OWNER=$(shell grep AWS_ACCOUNT $(ENV_FILE) | awk -F ': ' '{gsub(/"/, "", $$2); print($$2)}')
export TARGET_REPO_NAME=$(shell grep INTERNAL_SHARED_REPO $(ENV_FILE) | awk -F ': ' '{print($$2)}')

test-repo-exist:
	aws codeartifact describe-repository --domain $(DOMAIN_NAME) --domain-owner $(DOMAIN_OWNER) --repository $(TARGET_REPO_NAME) --region $(AWS_REGION)

test-generic:
	cd generic && ./test_generic_pkg_publish_download.sh

test-nuget:
	cd nuget && ./test_nuget_method_2.sh

test-python:
	cd python && ./test_twine_publish_pip_download.sh

pre-commit: test-repo-exist test-generic test-nuget test-python
