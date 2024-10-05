export AWS_DEFAULT_REGION ?= ap-southeast-2
export CDK_DEFAULT_REGION ?= ap-southeast-2
export ENV_STAGE ?= dev

APP_NAME=$(shell grep -m 1 AppName environment/$(ENV_STAGE).yml | cut -c 10-)

install-cdk:
	npm install -g aws-cdk
	python3 -m pip install -U pip
	pip3 install -r requirements-dev.txt

synth:
	cdk synth -c env=${ENV_STAGE} --all

deploy:
	pip3 install -r requirements.txt
	cdk deploy $(APP_NAME) -c env=${ENV_STAGE} --require-approval never

destroy:
	cdk destroy $(APP_NAME) -f -c env=${ENV_STAGE}

test-cdk:
	python3 -m pytest tests/

pre-commit: format-python lint-python lint-yaml test

format-python:
	black **.py

lint-python:
	pip3 install flake8
	flake8 **.py

lint-yaml:
	yamllint -c .github/linters/.yaml-lint.yml -f parsable .

clean:
	rm -rf cdk.out **/__pycache__
