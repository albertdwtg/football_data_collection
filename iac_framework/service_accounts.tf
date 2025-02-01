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

# resource "google_project_iam_member" "execution_sa_roles" {
    #droits de lecture et suppresion sur les buckets du module
    #droits d'update sur les datasets du module
# }
