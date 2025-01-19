locals {
  buckets_config_files_set = fileset("../modules/${var.module}/buckets/**", "*.yaml")

  buckets_config_files_paths = {
    for file in local.buckets_config_files_set :
    trim(file, "../") => "../modules/${var.module}/buckets/${trim(file, "../")}"
  }

  buckets_configs = {
    for file_name, file_path in local.buckets_config_files_paths :
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
    }
  }
}

resource "google_storage_bucket" "buckets" {
  for_each                    = local.buckets_configs
  name                        = "${var.product_name}_${each.value.base_name}_${var.region_id}_${var.env}"
  project                     = var.project
  location                    = try(each.value.content.location, var.region)
  force_destroy               = try(each.value.content.force_destroy, null)
  storage_class               = try(each.value.content.storage_class, null)
  uniform_bucket_level_access = try(each.value.content.uniform_bucket_level_access, null)
  requester_pays              = try(each.value.content.requester_pays, null)
  dynamic "lifecycle_rule" {
    for_each = flatten(try(each.value.content.lifecycle_rule, []))
    content {
      action {
        type          = try(each.value.action.type, null)
        storage_class = try(each.value.content.lifecycle_rule.action.storage_class, null)
      }
      condition {
        age                   = try(each.value.content.lifecycle_rule.condition.age, null)
        created_before        = try(each.value.content.lifecycle_rule.condition.created_before, null)
        matches_storage_class = try(each.value.content.lifecycle_rule.condition.matches_storage_class, null)
      }
    }
  }
}

output "buckets" {
  value = google_storage_bucket.buckets
}
