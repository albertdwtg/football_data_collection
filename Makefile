export GCP_PROJECT_ID ?= model-zoo-382809
export GCP_REGION ?= europe-west1
export GCP_REGION_ID ?= ew1
export PRODUCT_NAME ?= cdp
export IS_PR ?= false
export BASE_MODULE_NAME = base
export GCF_CODE_FOLDER ?= modules/$(MODULE)/gcf_code
export GCF_SOURCE_CODE ?= src
export TARGET_DIR=modules/$(MODULE)/infra
export MODULE_DIR=modules/$(MODULE)
TF_COMMANDS_FILE := commands/terraform.mk
PY_COMMANDS_FILE := commands/python.mk

include $(PY_COMMANDS_FILE)
include $(TF_COMMANDS_FILE)

# Dont't print commands
ifndef VERBOSE
.SILENT:
endif

ifndef MODULE
	@echo '[$@] --> MODULE value must be set'
	exit 1
endif
ifneq ($(filter true false,$(IS_PR)),$(IS_PR))
	@echo '[$@] --> IS_PR must be 'true' or 'false''
	exit 1
endif
ifneq ($(filter dev prd,$(ENV)),$(ENV))
	@echo '[$@] --> ENV must be 'dev' or 'prd''
	exit 1
endif
ifeq ($(MODULE), $(BASE_MODULE_NAME))
	echo "[$@] --> BASE"; 
	export TARGET_DIR=$(BASE_MODULE_NAME);
	export MODULE_DIR=$(BASE_MODULE_NAME);
else 
	echo "[$@] --> COMMON"; 
	export TARGET_DIR=modules/$(MODULE)/infra; 
	export MODULE_DIR=modules/$(MODULE); 
endif

pre-checks:
	@echo '[$@] --> EMPTY'

deploy: pre-checks py-cicd tf-cicd

# Description des cibles
help:
	@echo "Available targets :"
	@echo "  py-checks           : Run test and linter for python code"
	@echo "  check-requirements  : Check if all dependencies have a fixed version"
	@echo "  clean-py-files      : Remove files created during py-checks"
	@echo "  py-testing          : All python operations in order"
	@echo "  local-cf            : Execute cloud functions locally"
	@echo "  help                : print this notice"
