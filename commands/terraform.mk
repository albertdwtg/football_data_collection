TF_STATE_BUCKET := tf_state_football_data_collection
export TFVARS_FILE := default.tfvars
export TF_DATA_DIR := tf_states/$(ENV)

define TFVARS_CONTENT
region    	 	= "$(GCP_REGION)"
region_id 	 	= "$(GCP_REGION_ID)"
project   	 	= "$(GCP_PROJECT_ID)"
env       	 	= "$(ENV)"
module    	    = "$(MODULE)"
product_name    = "$(PRODUCT_NAME)"
zip_source_file = "$(GCF_SOURCE_ZIP)"
endef
export TFVARS_CONTENT

# ifneq ($(MODULE), $(BASE_MODULE_NAME))
# 	echo "[$@] --> TARGETTTTTTTTTTTTTTTTTT"; \
# else \
# 	echo "[$@] --> TARGETTTTTTTTTTTTTTTTTT"; \
# 	export TARGET_DIR=modules/$(MODULE)/infra; \
# 	export MODULE_DIR=modules/$(MODULE); \
# endif

# variable-assignment:
# 	@echo '[$@] --> ENTER'
# 	if [ "$(MODULE)" = "$(BASE_MODULE_NAME)" ]; then \
# 		echo '[$@] --> BASE'; \
# 		TARGET_DIR=$(BASE_MODULE_NAME); \
# 		MODULE_DIR=$(BASE_MODULE_NAME); \
# 	else \
# 		echo '[$@] --> COMMON'; \
# 		export TARGET_DIR=modules/$(MODULE)/infra; \
# 		export MODULE_DIR=modules/$(MODULE); \
# 	fi

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
		if [ "$(IS_PR)" = "false" ]; then \
			echo "[$@] --> Start Terraform apply"; \
			terraform apply -var-file=$(TFVARS_FILE) -auto-approve; \
		fi; \
		rm $(TFVARS_FILE);

deploy-base:
	@echo '[$@] --> Start Terraform deployment of env > $(ENV)'
	cd $(BASE_MODULE_NAME); \
		echo "[$@] --> Check terraform syntax"; \
		terraform fmt; \
		echo "$$TFVARS_CONTENT" > $(TFVARS_FILE); \
		echo "[$@] --> Start Terraform init"; \
		terraform init -backend-config="bucket=$(TF_STATE_BUCKET)" -backend-config="prefix=$(MODULE)/$(ENV)"; \
		echo "[$@] --> Start Terraform plan"; \
		terraform plan -var-file=$(TFVARS_FILE); \
		echo "[$@] --> Start Terraform validate"; \
		terraform validate; \
		if [ "$(IS_PR)" = "false" ]; then \
			echo "[$@] --> Start Terraform apply"; \
			terraform apply -var-file=$(TFVARS_FILE) -auto-approve; \
		fi; \
		rm $(TFVARS_FILE);


yaml-linter:
	#sudo apt-get install yamllint
	yamllint ./iac_framework
	@echo '[$@] --> Checking yaml syntax in $(MODULE_DIR)'
	yamllint $(MODULE_DIR)


tf-cicd: yaml-linter deploy-tf