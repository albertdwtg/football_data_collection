locals {
  secrets_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/secrets/**", "*.yaml")

  secrets_config_files_paths = {
    for file in local.secrets_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/secrets/${trim(file, "../")}"
  }

  secrets_configs = {
    for file_name, file_path in local.secrets_config_files_paths :
    trimsuffix(file_name, ".yaml") => {
      base_name = trimsuffix(basename(file_name), ".yaml")
      content = yamldecode(templatefile(
        file_path,
        merge(
          try(yamldecode(file("../../../modules/${var.module}/${local.resources_folder}/variables.yaml")), {}),
          {
            project : var.project
            region : var.region
            module : var.module
            env : var.env
          }
        )
      ))
    }
  }
}

resource "google_secret_manager_secret" "secrets" {
  for_each            = local.secrets_configs
  secret_id           = "${var.product_name}_srt_${each.value.base_name}_${var.env}"
  project             = var.project
  annotations         = try(each.value.content.annotations, null)
  version_aliases     = try(each.value.content.version_aliases, null)
  version_destroy_ttl = try(each.value.content.version_destroy_ttl, null)
  expire_time         = try(each.value.content.expire_time, null)

  replication {
    auto {}
  }
  labels = merge(
    try(each.value.content.labels, null),
    local.common_labels
  )
}

output "secrets" {
  value = google_secret_manager_secret.secrets
}
