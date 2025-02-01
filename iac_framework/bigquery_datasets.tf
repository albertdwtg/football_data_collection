locals {
  ds_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/datasets/**", "*.yaml")

  ds_config_files_paths = {
    for file in local.ds_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/datasets/${trim(file, "../")}"
  }

  ds_configs = {
    for file_name, file_path in local.ds_config_files_paths :
    trimsuffix(file_name, ".yaml") => {
      base_name = trimsuffix(basename(file_name), ".yaml")
      content = yamldecode(templatefile(
        file_path,
        merge(
          yamldecode(file("../../../modules/${var.module}/${local.resources_folder}/variables.yaml")),
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

resource "google_bigquery_dataset" "datasets" {
  for_each                        = local.ds_configs
  dataset_id                      = "${var.product_name}_${each.value.base_name}_${var.region_id}_${var.env}"
  project                         = var.project
  friendly_name                   = try(each.value.content.friendly_name, null)
  description                     = try(each.value.content.description, null)
  location                        = try(each.value.content.location, var.region)
  default_table_expiration_ms     = try(each.value.content.default_table_expiration_ms, null)
  default_partition_expiration_ms = try(each.value.content.default_partition_expiration_ms, null)
  max_time_travel_hours           = try(each.value.content.max_time_travel_hours, null)
  labels = merge(
    try(each.value.content.labels, null),
    local.common_labels
  )
}

output "datasets" {
  value = google_bigquery_dataset.datasets
}
