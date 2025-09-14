locals {
  workflows_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/workflows/**", "*.yaml")

  workflows_config_files_paths = {
    for file in local.workflows_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/workflows/${trim(file, "../")}"
  }

  sub_wkfs = join("\n",[
    for file_path in fileset("../../../iac_framework/wkf_library/**", "*.yaml") : 
    templatefile("../../../iac_framework/wkf_library/${trim(file_path, "../")}",
      merge(
        try(yamldecode(file("../../../modules/${var.module}/${local.resources_folder}/variables.yaml")), {}),
        {
          project : var.project
          region : var.region
          module : var.module
          env : var.env
        }
      )
    )
  ])

  workflows_configs = {
    for file_name, file_path in local.workflows_config_files_paths :
    trimsuffix(file_name, ".yaml") => {
      base_name = trimsuffix(basename(file_name), ".yaml")
      content = templatefile(
        file_path,
        merge(
          local.user_variables,
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
            buckets : {
              for k, v in google_storage_bucket.buckets :
              k => {
                url : v.url
              }
            }
            data_transfers : {
              for k, v in google_bigquery_data_transfer_config.data_transfers :
              k => {
                id : v.name
              }
            }
          }
        )
      )
    }
  }
}

resource "google_workflows_workflow" "workflows" {
  for_each        = local.workflows_configs
  project         = var.project
  region          = var.region
  service_account = google_service_account.execution_sa.id
  name            = "${var.product_name}_wkf_${each.value.base_name}_${var.region_id}_${var.env}"
  description     = "Workflow created in module ${var.module}"
  call_log_level  = "LOG_ALL_CALLS"
  source_contents = replace(join("\n ##SUB-WORKFLOWS\n", [each.value.content, local.sub_wkfs]), "---", "")
  labels          = local.common_labels
  depends_on      = [google_service_account.execution_sa, google_bigquery_table.tables]
}

output "workflows" {
  value = google_workflows_workflow.workflows
}
