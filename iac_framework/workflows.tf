locals {
  workflows_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/workflows/**", "*.yaml")

  workflows_config_files_paths = {
    for file in local.workflows_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/workflows/${trim(file, "../")}"
  }

  workflows_configs = {
    for file_name, file_path in local.workflows_config_files_paths :
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
      source_contents = templatefile(
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
  source_contents = yamlencode(each.value.content.source_contents)
  labels          = local.common_labels
  depends_on      = [google_service_account.execution_sa]
}

output "workflows" {
  value = google_workflows_workflow.workflows
}
