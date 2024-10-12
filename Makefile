export GCP_PROJECT_ID ?= model-zoo-382809
export GCP_REGION ?= europe-west1
TF_COMMANDS_FILE := commands/terraform.mk
PY_COMMANDS_FILE := commands/python.mk
export ENV

deploy-tf:
	make -s -f $(TF_COMMANDS_FILE)

deploy-py:
	make -s -f $(PY_COMMANDS_FILE)