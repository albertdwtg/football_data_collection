SHELL := /bin/bash
PYTHON_FOLDER = src
TEST_REQUIREMENTS_FILE = test_requirements.txt
VENV_TEST_DIR = .venv_test

define ENV_VARIABLES
PROJECT_ID = "$(GCP_PROJECT_ID)"
PROJECT_ENV = "$(ENV)"
endef
export ENV_VARIABLES

define TEST_REQUIREMENTS
black==24.10.0
pylint==3.3.1
pytest
endef
export TEST_REQUIREMENTS

define PYLINTRC
[MASTER]
ignore=$(VENV_TEST_DIR),.venv
endef
export PYLINTRC


py-checks:
	@echo 'Start to build python code'
	set -eo pipefail; \
	cd $(PYTHON_FOLDER); \
		echo "$$ENV_VARIABLES" > .env; \
		echo "Create test requirements"; \
		echo "$$TEST_REQUIREMENTS" > $(TEST_REQUIREMENTS_FILE); \
		cat requirements.txt >> $(TEST_REQUIREMENTS_FILE); \
		python3 -m venv $(VENV_TEST_DIR); \
		source $(VENV_TEST_DIR)/bin/activate; \
		echo "Install test requirements"; \
		pip install -r $(TEST_REQUIREMENTS_FILE); \
		echo "Run black checks"; \
		$(VENV_TEST_DIR)/bin/black . --check --exclude=.venv*; \
		echo "Run pylint checks"; \
		echo "$$PYLINTRC" > .pylintrc; \
		$(VENV_TEST_DIR)/bin/pylint . ;\
		echo "Run unit tests"; \
		python3 -m pytest -q ../tests_py/*;

clean-py-files:
	echo 'Remove files generated by python code testing'
	cd $(PYTHON_FOLDER); \
		rm -f .pylintrc;\
		rm -f .env;\
		rm -f $(TEST_REQUIREMENTS_FILE);

# py-unit-tests:
# 	cd $(PYTHON_FOLDER); \
# 		echo "$$ENV_VARIABLES" > .env; \
# 		echo "Create test requirements"; \
# 		echo "$$TEST_REQUIREMENTS" > $(TEST_REQUIREMENTS_FILE); \
# 		cat requirements.txt >> $(TEST_REQUIREMENTS_FILE); \
# 		python3 -m venv $(VENV_TEST_DIR); \
# 		source $(VENV_TEST_DIR)/bin/activate; \
# 		echo "Install test requirements"; \
# 		pip install -r $(TEST_REQUIREMENTS_FILE); \
# 		python3 -m pytest -q ../tests_py/*;

py-testing: py-checks clean-py-files

local-cf:
	echo 'Start to build python local cloud function'
	set -eo pipefail; \
	cd $(PYTHON_FOLDER); \
		echo 'Create venv'; \
		python3 -m venv .venv; \
		source .venv/bin/activate; \
		echo 'Install requirements'; \
		pip install -r requirements.txt; \
		echo "$$ENV_VARIABLES" > .env; \
		functions-framework --target=run --debug;

