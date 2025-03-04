data "google_storage_bucket" "gcf_artifacts" {
  name = "${var.product_name}_gcs_gcf_artifacts_${var.region_id}_${var.env}"
}

data "archive_file" "cf_code_zip" {
  type        = "zip"
  source_dir  = "../gcf_code/src"
  output_path = "../files/init.zip"
  #   excludes    = ["modules/${var.module}/gcf_code/src/.venv_test/"]
}

resource "google_storage_bucket_object" "zip_file" {
  # Append file MD5 to force bucket to be recreated
  name   = "gcf_${var.module}_${data.archive_file.cf_code_zip.output_md5}.zip"
  bucket = data.google_storage_bucket.gcf_artifacts.name
  source = data.archive_file.cf_code_zip.output_path
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
        object = google_storage_bucket_object.zip_file.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }
}
