export GCP_PROJECT_ID ?= model-zoo-382809
export GCP_REGION ?= europe-west1
export GCP_REGION_ID ?= ew1
export PRODUCT_NAME ?= cdp
export IS_PR ?= false
export BASE_MODULE_NAME = base
export GCF_CODE_FOLDER ?= modules/$(MODULE)/gcf_code
export GCF_SOURCE_CODE ?= src
export GCF_SOURCE_ZIP ?= zip_source.zip
export GCF_CHECKSUM := .checksum.txt

export EXECUTION_VARS_FOLDER = .execution_vars
export TF_DIR_LOCATION := $(EXECUTION_VARS_FOLDER)/TF_DIR.txt
export MODULE_DIR_LOCATION := $(EXECUTION_VARS_FOLDER)/MODULE_DIR.txt

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

vars-build:
	@echo '[$@] --> Running vars-build'
	mkdir -p $(EXECUTION_VARS_FOLDER);
	@if [ "$(MODULE)" = "$(BASE_MODULE_NAME)" ]; then \
		echo "$(BASE_MODULE_NAME)" > $(TF_DIR_LOCATION); \
		echo "$(BASE_MODULE_NAME)" > $(MODULE_DIR_LOCATION); \
	else \
		echo "modules/$(MODULE)/infra" > $(TF_DIR_LOCATION); \
		echo "modules/$(MODULE)" > $(MODULE_DIR_LOCATION); \
	fi


clean-cicd:
	echo '[$@] --> Remove files at the end of the CICD process'
	rm -rf $(EXECUTION_VARS_FOLDER);
	rm -rf $(shell cat $(TF_DIR_LOCATION))/$(TF_DATA_DIR);
	if [ -d "$(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE)" ]; then \
		cd $(GCF_CODE_FOLDER)/$(GCF_SOURCE_CODE); \
			rm -f ../$(GCF_SOURCE_ZIP); \
			rm -f ../$(GCF_CHECKSUM); \
	fi


deploy: vars-build py-cicd tf-cicd clean-cicd

# Description des cibles
help:
	@echo "Available targets :"
	@echo "  py-checks           : Run test and linter for python code"
	@echo "  check-requirements  : Check if all dependencies have a fixed version"
	@echo "  clean-py-files      : Remove files created during py-checks"
	@echo "  py-testing          : All python operations in order"
	@echo "  local-cf            : Execute cloud functions locally"
	@echo "  help                : print this notice"
