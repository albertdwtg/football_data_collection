data "google_storage_bucket" "gcf_artifacts" {
  name = "${var.product_name}_gcs_gcf_artifacts_${var.region_id}_${var.env}"
}

locals {
  sha_gcf_source = sha1(join("", [for f in fileset("../gcf_code/src", "*") : filesha1("../gcf_code/src/${f}")]))
}

resource "google_storage_bucket_object" "gcf_source_zip" {
  name   = "${var.module}/gcf_source_${local.sha_gcf_source}.zip"
  bucket = data.google_storage_bucket.gcf_artifacts.name
  source = "../gcf_code/${var.zip_source_file}" # Add path to the zipped function source code
}

resource "google_cloudfunctions2_function" "function" {
  name        = "${var.product_name}_gcf_${var.module}_${var.region_id}_${var.env}"
  location    = var.region
  description = "Cloud Function created in module ${var.module}"

  build_config {
    runtime     = "python312"
    entry_point = "run" # Set the entry point 
    source {
      storage_source {
        bucket = data.google_storage_bucket.gcf_artifacts.name
        object = google_storage_bucket_object.gcf_source_zip.name
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
