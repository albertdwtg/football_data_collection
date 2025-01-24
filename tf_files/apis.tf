resource "google_project_service" "apis" {
  for_each = toset([
    "bigquerydatatransfer",
    "workflows"
  ])
  project = var.project
  service = "${each.key}.googleapis.com"
}