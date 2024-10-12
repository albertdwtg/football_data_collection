resource "google_project_service" "apis" {
  project = var.project
  service = "bigquerydatatransfer.googleapis.com"
}