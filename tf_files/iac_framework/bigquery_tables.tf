locals {
  tables_config_files_set = fileset("../modules/${var.module}/tables/**", "*.yaml")

  tables_config_files_paths = {
    for file in local.tables_config_files_set :
    trim(file, "../") => "../modules/${var.module}/tables/${trim(file, "../")}"
  }

  tables_configs = {
    for file_name, file_path in local.tables_config_files_paths :
    trimsuffix(file_name, ".yaml") => {
      base_name = trimsuffix(basename(file_name), ".yaml")
      content = yamldecode(templatefile(
        file_path,
        merge(
          yamldecode(file("../modules/${var.module}/variables.yaml")),
          {
            project : var.project
            region : var.region
            module : var.module
            env : var.env
            datasets : {
              for k, v in google_bigquery_dataset.datasets :
              k => {
                id : v.dataset_id
              }
            }
          }
        )
      ))
    }
  }
}

resource "google_bigquery_table" "tables" {
  for_each                 = local.tables_configs
  project                  = var.project
  table_id                 = "${each.value.content.table_id}_v${each.value.content.version}"
  dataset_id               = each.value.content.dataset_id
  description              = each.value.content.description
  schema                   = try(jsonencode(each.value.content.schema), null)
  expiration_time          = try(each.value.content.expiration_time, null)
  require_partition_filter = try(each.value.content.require_partition_filter, null)
  deletion_protection      = try(each.value.content.deletion_protection, null)
  clustering               = try(each.value.content.clustering, null)
  dynamic "time_partitioning" {
    for_each = contains(keys(each.value.content), "time_partitioning") ? [1] : []
    content {
      type  = each.value.content.time_partitioning.type
      field = try(each.value.content.time_partitioning.field, null)
    }
  }
  labels = merge(
    try(each.value.content.labels, null),
    local.common_labels,
    {
      "has_schema_defined" : contains(keys(each.value.content), "schema")
      "finops_score" : sum([
        contains(keys(each.value.content), "clustering") ? 1 : 0,
        contains(keys(each.value.content), "time_partitioning") ? 1 : 0,
        contains(keys(each.value.content), "require_partition_filter") ? 1 : 0,
        contains(keys(each.value.content), "expiration_time") ? 1 : 0
      ])
    }
  )

  lifecycle {
    precondition {
      condition     = endswith(each.key, "v${each.value.content.version}")
      error_message = "File name must end with same version as defined in 'version' field"
    }
    precondition {
      condition     = length(each.value.content.description) > 5
      error_message = "It's mandatory to provide a description"
    }
  }

  depends_on = [google_bigquery_dataset.datasets]
}

output "tables" {
  value = google_bigquery_table.tables
}