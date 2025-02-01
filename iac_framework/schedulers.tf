locals {
  schedulers_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/schedulers/**", "*.yaml")

  schedulers_config_files_paths = {
    for file in local.schedulers_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/schedulers/${trim(file, "../")}"
  }

  schedulers_configs = {
    for file_name, file_path in local.schedulers_config_files_paths :
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

resource "google_cloud_scheduler_job" "schedulers" {
  for_each         = local.schedulers_configs
  project          = var.project
  region           = var.region
  name             = "${var.product_name}_trigger_${each.value.base_name}_${var.region_id}_${var.env}"
  description      = each.value.content.description
  schedule         = each.value.content.schedule
  time_zone        = try(each.value.content.time_zone, "Europe/Paris")
  paused           = try(each.value.content.paused, null)
  attempt_deadline = try(each.value.content.attempt_deadline, null)

  http_target {
    http_method = upper(each.value.content.http_target.http_method)
    uri         = each.value.content.http_target.uri
    body        = base64encode(try(each.value.content.http_target.body, ""))
    headers     = try(each.value.content.http_target.headers, null)
    dynamic "oidc_token" {
      for_each = contains(keys(each.value.content.http_target), "oidc_token") ? [1] : []
      content {
        service_account_email = each.value.content.http_target.oidc_token.service_account_email
        audience              = try(each.value.content.http_target.oidc_token.audience, null)
      }
    }
    dynamic "oauth_token" {
      for_each = contains(keys(each.value.content.http_target), "oauth_token") ? [1] : []
      content {
        service_account_email = each.value.content.http_target.oauth_token.service_account_email
        scope                 = try(each.value.content.http_target.oauth_token.scope, null)
      }
    }
  }

  dynamic "retry_config" {
    for_each = contains(keys(each.value.content), "retry_config") ? [1] : []
    content {
      retry_count          = try(each.value.content.retry_config.retry_count, null)
      max_retry_duration   = try(each.value.content.retry_config.max_retry_duration, null)
      min_backoff_duration = try(each.value.content.retry_config.min_backoff_duration, null)
      max_backoff_duration = try(each.value.content.retry_config.max_backoff_duration, null)
      max_doublings        = try(each.value.content.retry_config.max_doublings, null)
    }
  }
}

output "schedulers" {
  value = google_cloud_scheduler_job.schedulers
}
