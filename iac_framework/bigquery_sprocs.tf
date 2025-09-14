locals {
  sprocs_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/sprocs/**", "*.yaml")

  sprocs_config_files_paths = {
    for file in local.sprocs_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/sprocs/${trim(file, "../")}"
  }

  sprocs_configs = {
    for file_name, file_path in local.sprocs_config_files_paths :
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
            datasets : {
              for k, v in google_bigquery_dataset.datasets :
              k => {
                id : v.dataset_id
              }
            }
            tables : {
              for k, v in google_bigquery_table.tables :
              k => {
                id : v.table_id
              }
            }
          }
        )
      ))
    }
  }
}

resource "google_bigquery_routine" "sprocs" {
    for_each        = local.sprocs_configs
    project         = try(each.value.content.project, var.project)
    routine_id      = "sproc_${each.value.content.name}_v${each.value.content.version}"
    dataset_id      = each.value.content.dataset_id
    routine_type    = "PROCEDURE"
    language        = "SQL"
    definition_body = try(each.value.content.definition_body, null)
    # description     = try(each.value.content.description, null)

    lifecycle {
        precondition {
            condition     = each.key == "sproc_${each.value.content.name}_v${each.value.content.version}"
            error_message = "File name must match sproc name and version"
        }
        precondition {
            condition     = length(each.value.content.description) > 5
            error_message = "It's mandatory to provide a description"
        }
    }

    depends_on = [google_bigquery_dataset.datasets]
}