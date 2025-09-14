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
  for_each = toset(["logging.logWriter", "bigquery.admin"])
  project  = var.project
  role     = "roles/${each.value}"
  member   = "serviceAccount:${google_service_account.execution_sa.email}"
}

# PERMISSIONS > Bucket level

locals {
  buckets_roles = ["storage.objectAdmin"]
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

# PERMISSIONS > Dataset level

locals {
  datasets_roles = ["bigquery.dataEditor"]
  datasets_roles_combination = flatten([
    for dataset in google_bigquery_dataset.datasets : [
      for role in local.datasets_roles : {
        dataset_id = dataset.dataset_id
        role       = "roles/${role}"
      }
    ]
  ])
}

resource "google_bigquery_dataset_iam_member" "execution_sa_dataset_roles" {
  for_each = { for idx, item in local.datasets_roles_combination : idx => item }

  dataset_id = each.value.dataset_id
  role       = each.value.role
  member     = "serviceAccount:${google_service_account.execution_sa.email}"
}

# PERMISSIONS > Secret level

locals {
  secrets_roles = ["secretmanager.secretAccessor"]
  secrets_roles_combination = flatten([
    for secret in google_secret_manager_secret.secrets : [
      for role in local.secrets_roles : {
        secret_id = secret.secret_id
        role      = "roles/${role}"
      }
    ]
  ])
}

resource "google_secret_manager_secret_iam_member" "execution_sa_secret_roles" {
  for_each = { for idx, item in local.secrets_roles_combination : idx => item }

  secret_id = each.value.secret_id
  role      = each.value.role
  member    = "serviceAccount:${google_service_account.execution_sa.email}"
}

output "execution_sa" {
  value = google_service_account.execution_sa.email
}
