resource "google_bigquery_dataset" "ingest_football_data_collection" {
  dataset_id  = "ingest_football_data_collection_${var.env}"
  description = "Dataset containing raw data coming from data transfer"
  location    = var.region
}

resource "google_bigquery_table" "events_stats" {
  dataset_id          = google_bigquery_dataset.ingest_football_data_collection.dataset_id
  table_id            = "events_stats"
  schema              = <<EOF
        [
            {
                "name": "metadata",
                "mode": "NULLABLE",
                "type": "JSON",
                "description": "",
                "fields": []
            },
            {
                "name": "statistics",
                "mode": "NULLABLE",
                "type": "JSON",
                "description": "",
                "fields": []
            }
        ]
        EOF
  deletion_protection = false
  time_partitioning {
    type = "DAY"
  }
}

resource "google_service_account" "gcs_to_bq_sa" {
  account_id  = "gcs-to-bq-${var.env}"
  description = "Service Account used to transfer data from GCS to BQ via data transfer"
}

resource "google_storage_bucket_iam_member" "project" {
  bucket = google_storage_bucket.football_data_collection.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.gcs_to_bq_sa.email}"
}

resource "google_bigquery_data_transfer_config" "events_stats_dts" {
  service_account_name   = google_service_account.gcs_to_bq_sa.email
  display_name           = "events_stats_${var.env}"
  location               = var.region
  data_source_id         = "google_cloud_storage"
  destination_dataset_id = google_bigquery_dataset.ingest_football_data_collection.dataset_id
  params = {
    data_path_template              = "${google_storage_bucket.football_data_collection.url}/events_stats/*.json",
    file_format                     = "JSON"
    destination_table_name_template = google_bigquery_table.events_stats.table_id
    delete_source_files             = true
  }
  schedule_options {
    disable_auto_scheduling = true
  }
  depends_on = [google_service_account.gcs_to_bq_sa]
}
