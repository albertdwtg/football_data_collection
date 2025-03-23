SHELL := /bin/bash
GCF_TESTS_FOLDER ?= tests_py
REQUIREMENTS_FILE = requirements.txt
BASE_REQUIREMENTS_FILE = $(ROOT)/commands/configs/py_requirements.txt
# File that will contain all requirements
TEST_REQUIREMENTS_FILE = test_requirements.txt
VENV_TEST_DIR = .venv_test
VENV_DIR = .venv
RUFF_CONFIG_FILE =  $(ROOT)/commands/configs/ruff.toml
export GCS_BUCKET_SOURCE_CODE = $(PRODUCT_NAME)_gcs_gcf_artifacts_$(GCP_REGION_ID)_$(ENV)

# .env file content for python project
define ENV_VARIABLES
PROJECT_ID = $(GCP_PROJECT_ID)
PROJECT_ENV = $(ENV)
endef
export ENV_VARIABLES

#This target must be run in first
create-checksum:
	echo '[$@] --> Create checksum of the source code'
	find $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE) -type f \( -name "*.py" -o -name "*.txt" \) -print0 | sort -z | xargs -0 sha1sum | sha1sum | head -c 40 > $(GCF_CODE_FOLDER)/$(GCF_CHECKSUM)

# Check if all dependencies have a fixed version
check-requirements:
	echo "[$@] --> Check versions in requirements file"
	@if grep -q -v "==" $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE)/$(REQUIREMENTS_FILE); then \
		echo "ERROR : Some requirements doesn't have a specified version"; \
		exit 1; \
	fi

# Run test and linter
py-checks:
	echo '[$@] --> Start to test python code'
	set -eo pipefail; \
	cd $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE); \
		echo "$$ENV_VARIABLES" > .env; \
		echo "[$@] --> Create test requirements"; \
		cat $(BASE_REQUIREMENTS_FILE) > $(TEST_REQUIREMENTS_FILE); \
		cat $(REQUIREMENTS_FILE) >> $(TEST_REQUIREMENTS_FILE); \
		python3 -m venv ../$(VENV_TEST_DIR); \
		source ../$(VENV_TEST_DIR)/bin/activate; \
		echo "[$@] --> Install test requirements"; \
		pip install -r $(TEST_REQUIREMENTS_FILE) --quiet; \
		echo "[$@] --> Run ruff linter"; \
		../$(VENV_TEST_DIR)/bin/ruff check --config=$(RUFF_CONFIG_FILE);\
		if [ -d "../$(GCF_TESTS_FOLDER)" ]; then \
			echo "[$@] --> Run unit tests"; \
			python3 -m pytest -q ../$(GCF_TESTS_FOLDER)/*;\
		else \
			echo "[$@] --> No unit tests to run"; \
		fi; \
		deactivate; \

zip-source:
	echo '[$@] --> Create zip of the source code'
	cd $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE); \
		zip -r ../$(GCF_SOURCE_ZIP) . -x ./$(VENV_TEST_DIR)/\* ./.ruff_cache/\*; \
		echo '[$@] --> copying into gs://$(GCS_BUCKET_SOURCE_CODE)/$(MODULE)/$(shell cat $(GCF_CODE_FOLDER)/$(GCF_CHECKSUM)).zip'; \
		gsutil cp ../$(GCF_SOURCE_ZIP) gs://$(GCS_BUCKET_SOURCE_CODE)/$(MODULE)/$(shell cat $(GCF_CODE_FOLDER)/$(GCF_CHECKSUM)).zip; \

# Remove files created during py-checks
clean-py-files:
	echo '[$@] --> Remove files generated by python code testing'
	cd $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE); \
		rm -f .env;\
		find . -type d -name "__pycache__" -exec rm -r {} +;\
		rm -f $(TEST_REQUIREMENTS_FILE);

# All operations in order
py-operations: create-checksum check-requirements py-checks clean-py-files zip-source

py-cicd:
	if [ -d $(GCF_CODE_FOLDER) ]; then \
		if [ -d $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE) ]; then \
			$(MAKE) py-operations ENV=$(ENV) MODULE=$(MODULE); \
		else \
			echo "[$@] --> No python folder found, $(GCF_SOURCE_CODE) was not found inside $(GCF_CODE_FOLDER)"; \
			exit 1; \
		fi; \
	else \
		echo "[$@] --> No GCF code folder found, $(GCF_CODE_FOLDER) was not found"; \
	fi

# Execute cloud functions locally
local-cf:
	echo '[$@] --> Start to build python local cloud function'
	set -eo pipefail; \
	cd $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE); \
		echo 'Create venv'; \
		python3 -m venv $(VENV_DIR); \
		source $(VENV_DIR)/bin/activate; \
		echo 'Install requirements'; \
		pip install -r $(REQUIREMENTS_FILE); \
		echo "$$ENV_VARIABLES" > .env; \
		functions-framework --target=run --debug;


