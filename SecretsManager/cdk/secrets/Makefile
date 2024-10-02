export AWS_DEFAULT_REGION ?= ap-southeast-2
export CDK_DEFAULT_REGION ?= ap-southeast-2
export ENV_STAGE ?= dev

APP_NAME=$(shell grep -m 1 AppName environment/$(ENV_STAGE).yml | cut -c 10-)

install-cdk:
	npm install -g aws-cdk
	python3 -m pip install -U pip
	pip3 install -r requirements.txt

synth:
	cdk synth $(APP_NAME)-Secrets -c env=$(ENV_STAGE)

synth-local:
	CDK_LOCAL_SYNC=true cdk synth $(APP_NAME)-Secrets -c env=$(ENV_STAGE)

diff:
	cdk diff $(APP_NAME)-Secrets -c env=$(ENV_STAGE)

deploy:
	cdk deploy $(APP_NAME)-Secrets -c env=$(ENV_STAGE) $(APP_NAME) --require-approval never

destroy:
	cdk destroy $(APP_NAME)-Secrets -f -c env=$(ENV_STAGE)

test-cdk:
	pip3 install -r requirements-dev.txt && \
	python3 -m pytest .

pre-commit: format-python lint-python lint-yaml

format-python:
	black --line-length=100 **.py */**.py

lint-python:
	pip3 install flake8
	flake8 --ignore E501,F541,W503,W605 **.py */**.py

lint-yaml:
	yamllint -c .github/linters/.yaml-lint.yml -f parsable .

clean:
	rm -rf cdk.out lib/__pycache__
