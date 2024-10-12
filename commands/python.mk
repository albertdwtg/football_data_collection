define ENV_VARIABLES
PROJECT_ID = "$(GCP_PROJECT_ID)"
PROJECT_ENV = "$(ENV)"
endef
export ENV_VARIABLES

define TEST_REQUIREMENTS
black==24.10.0
pylint==3.3.1
endef
export TEST_REQUIREMENTS

define PYLINTRC
[MASTER]
ignore=.venv_test
endef
export PYLINTRC

SHELL := /bin/bash
PYTHON_FOLDER = src
TEST_REQUIREMENTS_FILE = test_requirements.txt

deploy:
	@echo 'Start to build python code > $(ENV)'
	cd $(PYTHON_FOLDER); \
		echo "$$ENV_VARIABLES" > .env; \
		echo "Install test requirements"; \
		echo "$$TEST_REQUIREMENTS" > $(TEST_REQUIREMENTS_FILE); \
		python3 -m venv .venv_test; \
		source .venv_test/bin/activate; \
		pip install -r $(TEST_REQUIREMENTS_FILE); \
		echo "Run black checks"; \
		../.venv/bin/black . --check --exclude=.venv_test; \
		echo "Run pylint checks"; \
		echo "$$PYLINTRC" > .pylintrc; \
		../.venv/bin/pylint . ;