resource "google_storage_bucket" "gcf_artifacts" {
  name     = "${var.product_name}_gcs_gcf_artifacts_${var.region_id}_${var.env}"
  project  = var.project
  location = var.region
}

