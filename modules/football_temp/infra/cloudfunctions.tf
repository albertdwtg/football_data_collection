resource "google_cloudfunctions2_function" "function" {
  name        = "${var.product_name}_gcf_${var.module}_${var.region_id}_${var.env}"
  location    = var.region
  description = "Cloud Function created in module ${var.module}"

  build_config {
    runtime     = "python312"
    entry_point = "run" # Set the entry point 
    source {
      storage_source {
        bucket = var.gcs_bucket_source_code
        object = "${var.module}/${file("../${var.gcf_code_folder}/${var.gcf_checksum}")}.zip"
      }
    }
  }

  service_config {
    max_instance_count             = 1
    available_memory               = "256M"
    timeout_seconds                = 60
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = module.iac_framework.execution_sa

    environment_variables = {
      PROJECT_ID  = var.project
      PROJECT_ENV = var.env
    }
  }
}