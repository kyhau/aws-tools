.PHONY: lint install yamllint cfn-lint clean

install:
	pip install -r requirements-ci.txt

yamllint:
	yamllint -c ./.github/linters/.yaml-lint.yaml -f parsable --format standard .github/

cfn-lint:
	cfn-lint --config-file .github/linters/.cfnlintrc

lint: install yamllint cfn-lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
