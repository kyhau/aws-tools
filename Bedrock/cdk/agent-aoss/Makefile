export AWS_DEFAULT_REGION ?= ap-southeast-2
export CDK_DEFAULT_REGION ?= ap-southeast-2
export ENV_STAGE ?= dev

APP_NAME=$(shell grep -m 1 AppName environment/$(ENV_STAGE).yml | cut -c 10-)

install-cdk:
	npm install -g aws-cdk
	python3 -m pip install -U pip
	pip3 install -r cdk/requirements.txt

synth:
	cd cdk && cdk synth -c env=$(ENV_STAGE) --all

deploy:
	cd cdk && \
	pip3 install -r requirements.txt && \
	cdk deploy -c env=$(ENV_STAGE) $(APP_NAME) --require-approval never

destroy:
	cd cdk && cdk destroy -f -c env=$(ENV_STAGE) $(APP_NAME)

test-cdk:
	cd cdk && \
	pip3 install -r requirements-dev.txt && \
	python3 -m pytest .

test-code:
	python3 tests/test_bedrock.py

pre-commit: format-python lint-python lint-yaml test

format-python:
	black */**.py */**/**.py

lint-python:
	pip3 install flake8
	flake8 */**.py */**/**.py

lint-yaml:
	yamllint -c .github/linters/.yaml-lint.yml -f parsable .

clean:
	rm -rf cdk.out lib/__pycache__
