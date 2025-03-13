TF_STATE_BUCKET := tf_state_football_data_collection
export TFVARS_FILE := default.tfvars
export TF_DATA_DIR := tf_state/

define TFVARS_CONTENT
region    	 		   = "$(GCP_REGION)"
region_id 	 		   = "$(GCP_REGION_ID)"
project   	 		   = "$(GCP_PROJECT_ID)"
env       	 		   = "$(ENV)"
module    	    	   = "$(MODULE)"
product_name    	   = "$(PRODUCT_NAME)"
gcf_checksum    	   = "$(GCF_CHECKSUM)"
gcf_code_folder 	   = "$(notdir $(GCF_CODE_FOLDER))"
zip_source_file 	   = "$(GCF_SOURCE_ZIP)"
gcs_bucket_source_code = "$(GCS_BUCKET_SOURCE_CODE)"
endef
export TFVARS_CONTENT

deploy-tf:
	@echo '[$@] --> Start Terraform deployment of env > $(ENV)'
	cd $(shell cat $(TF_DIR_LOCATION)); \
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
	@echo '[$@] --> Checking yaml syntax in $(shell cat $(MODULE_DIR_LOCATION))'
	yamllint $(shell cat $(MODULE_DIR_LOCATION))


tf-cicd: yaml-linter deploy-tf