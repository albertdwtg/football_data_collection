TF_STATE_BUCKET := tf_state_football_data_collection
export TFVARS_FILE := default.tfvars
export TF_DATA_DIR := tf_states/$(ENV)

define TFVARS_CONTENT
region    	 = "$(GCP_REGION)"
region_id 	 = "$(GCP_REGION_ID)"
project   	 = "$(GCP_PROJECT_ID)"
env       	 = "$(ENV)"
module    	 = "$(MODULE)"
product_name = "$(PRODUCT_NAME)"
endef
export TFVARS_CONTENT

deploy-tf:
	@echo '[$@] --> Start Terraform deployment of env > $(ENV)'
	cd $(TARGET_DIR); \
		echo "[$@] --> Check terraform syntax"; \
		terraform fmt; \
		echo "$$TFVARS_CONTENT" > $(TFVARS_FILE); \
		echo "[$@] --> Start Terraform init"; \
		terraform init -backend-config="bucket=$(TF_STATE_BUCKET)" -backend-config="prefix=$(MODULE)/$(ENV)"; \
		echo "[$@] --> Start Terraform plan"; \
		terraform plan -var-file=$(TFVARS_FILE); \
		echo "[$@] --> Start Terraform validate"; \
		terraform validate; \
		echo "[$@] --> Start Terraform apply"; \
		terraform apply -var-file=$(TFVARS_FILE) -auto-approve; \
		rm $(TFVARS_FILE);

yaml-linter:
	#sudo apt-get install yamllint
	@echo '[$@] --> Checking yaml syntax in $(MODULE_DIR)'
	yamllint $(MODULE_DIR)

pre-checks:
ifndef MODULE
	@echo '[$@] --> MODULE value must be set'
	exit 1
endif

deploy-module: pre-checks yaml-linter deploy-tf