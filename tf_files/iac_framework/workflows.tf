locals {
  workflows_config_files_set = fileset("../modules/${var.module}/workflows/**", "*.yaml")

  workflows_config_files_paths = {
    for file in local.workflows_config_files_set :
    trim(file, "../") => "../modules/${var.module}/workflows/${trim(file, "../")}"
  }

  workflows_configs = {
    for file_name, file_path in local.workflows_config_files_paths :
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
          }
        )
      ))
      source_contents = templatefile(
        file_path,
        merge(
          yamldecode(file("../modules/${var.module}/variables.yaml")),
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

resource "google_service_account" "workflows_sa" {
  for_each = local.workflows_configs
  project  = var.project
  account_id = join("-", [
    var.product_name,
    "wkf",
    "sa",
    each.value.base_name,
    var.env
  ])
  description = "Entity running ${each.value.base_name} workflow of module ${var.module} in ${upper(var.env)} environment"
}

resource "google_workflows_workflow" "workflows" {
  for_each        = local.workflows_configs
  project         = var.project
  region          = var.region
  service_account = google_service_account.workflows_sa[each.key].id
  name            = "${var.product_name}_wkf_${each.value.base_name}_${var.region_id}_${var.env}"
  description     = each.value.content.description
  call_log_level  = upper(try(each.value.content.call_log_level, "LOG_ALL_CALLS"))
  source_contents = tostring(yamlencode(each.value.content.source_contents))
}

output "workflows" {
  value = google_workflows_workflow.workflows
}
