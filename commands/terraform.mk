TF_STATE_BUCKET := tf_state_football_data_collection
export TFVARS_FILE := default.tfvars
export TF_DATA_DIR := local_tf_states/$(ENV)

define TFVARS_CONTENT
region  = "$(GCP_REGION)"
project = "$(GCP_PROJECT_ID)"
env     = "$(ENV)"
endef
export TFVARS_CONTENT

deploy:
	@echo 'Start Terrform deployment of env > $(ENV)'
	cd tf_files; \
		echo "Check terraform syntax"; \
		terraform fmt; \
		echo "$$TFVARS_CONTENT" > $(TFVARS_FILE); \
		echo "Start Terraform init"; \
		terraform init -backend-config="bucket=$(TF_STATE_BUCKET)" -backend-config="prefix=$(ENV)"; \
		echo "Start Terraform plan"; \
		terraform plan -var-file=$(TFVARS_FILE); \
		echo "Start Terraform validate"; \
		terraform validate; \
		echo "Start Terraform apply"; \
		terraform apply -var-file=$(TFVARS_FILE) -auto-approve; \
		rm $(TFVARS_FILE);