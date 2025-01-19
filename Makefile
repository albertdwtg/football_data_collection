export GCP_PROJECT_ID ?= model-zoo-382809
export GCP_REGION ?= europe-west1
export GCP_REGION_ID ?= ew1
export PRODUCT_NAME ?= cdp
TF_COMMANDS_FILE := commands/terraform.mk
PY_COMMANDS_FILE := commands/python.mk

# Dont't print commands
ifndef VERBOSE
.SILENT:
endif

include $(PY_COMMANDS_FILE)
include $(TF_COMMANDS_FILE)

# Description des cibles
help:
	@echo "Available targets :"
	@echo "  py-checks           : Run test and linter for python code"
	@echo "  check-requirements  : Check if all dependencies have a fixed version"
	@echo "  clean-py-files      : Remove files created during py-checks"
	@echo "  py-testing          : All python operations in order"
	@echo "  local-cf            : Execute cloud functions locally"
	@echo "  help                : print this notice"

# Check input value for ENV variable
check-env:
	if [ "$(ENV)" != "prd" ] && [ "$(ENV)" != "dev" ]; then \
		echo "[$@] --> ERROR : ENV variable must be 'prd' or 'dev'."; \
		exit 1; \
	fi