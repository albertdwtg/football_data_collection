resource "google_storage_bucket" "gcf_artifacts" {
  name     = var.gcs_bucket_source_code
  project  = var.project
  location = var.region
}

