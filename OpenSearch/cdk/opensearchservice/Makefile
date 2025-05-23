export AWS_DEFAULT_REGION ?= ap-southeast-2
export CDK_DEFAULT_REGION ?= ap-southeast-2
export ENV_STAGE ?= dev

APP_NAME=$(shell grep -m 1 AppName environment/$(ENV_STAGE).yml | cut -c 10-)

install-cdk:
	npm install -g aws-cdk
	python3 -m pip install -U pip
	pip3 install -r requirements.txt

synth:
	cdk synth $(APP_NAME)-OpenSearch -c env=$(ENV_STAGE)

diff:
	cdk diff $(APP_NAME)-OpenSearch -c env=$(ENV_STAGE)

deploy:
	cdk deploy $(APP_NAME)-OpenSearch -c env=$(ENV_STAGE) $(APP_NAME) --require-approval never

destroy:
	cdk destroy $(APP_NAME)-OpenSearch -f -c env=$(ENV_STAGE)

test-cdk:
	pip3 install -r requirements-dev.txt && \
	python3 -m pytest .

test-code:
	python3 tests/test_guardrail.py

pre-commit: format-python lint-python lint-yaml

format-python:
	black **.py */**.py

lint-python:
	pip3 install flake8
	flake8 **.py */**.py

lint-yaml:
	yamllint -c .github/linters/.yaml-lint.yml -f parsable .

clean:
	rm -rf cdk.out __pycache__
