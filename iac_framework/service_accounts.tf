resource "google_service_account" "execution_sa" {
  project = var.project
  account_id = join("-", [
    var.product_name,
    "execution",
    "sa",
    var.module,
    var.env
  ])
  description = "Entity running executions of module ${var.module} in ${upper(var.env)} environment"
}

# PERMISSIONS > Project level

resource "google_project_iam_member" "execution_sa_project_roles" {
  for_each = toset(["logging.logWriter"])
  project  = var.project
  role     = "roles/${each.value}"
  member   = "serviceAccount:${google_service_account.execution_sa.email}"
}

# PERMISSIONS > Bucket level

locals {
  buckets_roles = ["storage.objectViewer"]
  buckets_roles_combination = flatten([
    for bucket in google_storage_bucket.buckets : [
      for role in local.buckets_roles : {
        bucket = bucket.name
        role   = "roles/${role}"
      }
    ]
  ])
}

resource "google_storage_bucket_iam_member" "execution_sa_bucket_roles" {
  for_each = { for idx, item in local.buckets_roles_combination : idx => item }

  bucket = each.value.bucket
  role   = each.value.role
  member = "serviceAccount:${google_service_account.execution_sa.email}"
}

output "execution_sa" {
  value = google_service_account.execution_sa.email
}
