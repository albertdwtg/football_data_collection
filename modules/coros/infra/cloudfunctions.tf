resource "google_cloudfunctions2_function" "function" {
  name        = "${var.product_name}-gcf-${var.module}-${var.region_id}-${var.env}"
  project     = var.project
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

resource "google_cloud_run_service_iam_member" "invoker_permission" {
  location = google_cloudfunctions2_function.function.location
  project  = google_cloudfunctions2_function.function.project
  service  = google_cloudfunctions2_function.function.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${module.iac_framework.execution_sa}"
}
