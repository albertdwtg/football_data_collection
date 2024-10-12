resource "google_storage_bucket" "football_data_collection" {
  name     = "football_data_collection_${var.env}"
  location = var.region
  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }
}
