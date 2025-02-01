locals {
  dts_config_files_set = fileset("../../../modules/${var.module}/${local.resources_folder}/data_transfers/**", "*.yaml")

  dts_config_files_paths = {
    for file in local.dts_config_files_set :
    trim(file, "../") => "../../../modules/${var.module}/${local.resources_folder}/data_transfers/${trim(file, "../")}"
  }

  dts_configs = {
    for file_name, file_path in local.dts_config_files_paths :
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
            buckets : {
              for k, v in google_storage_bucket.buckets :
              k => {
                url : v.url
              }
            }
          }
        )
      ))
    }
  }
}

resource "google_bigquery_data_transfer_config" "data_transfers" {
  for_each               = local.dts_configs
  display_name           = "${var.product_name}_dts_${each.value.base_name}_${var.region_id}_${var.env}"
  project                = var.project
  location               = var.region
  data_source_id         = try(each.value.content.data_source_id, null)
  destination_dataset_id = try(each.value.content.destination_dataset_id, null)
  service_account_name   = google_service_account.execution_sa.email
  params = {
    destination_table_name_template = try(each.value.content.params.destination_table_name_template, null)
    data_path_template              = try(each.value.content.params.data_path_template, null)
    write_disposition               = try(each.value.content.params.write_disposition, null)
    file_format                     = try(each.value.content.params.file_format, null)
    max_bad_records                 = try(each.value.content.params.max_bad_records, null)
    decimal_target_types            = try(each.value.content.params.decimal_target_types, null)
    ignore_unknown_values           = try(each.value.content.params.ignore_unknown_values, null)
    use_avro_logical_types          = try(each.value.content.params.use_avro_logical_types, null)
    parquet_enum_as_string          = try(each.value.content.params.parquet_enum_as_string, null)
    delete_source_files             = try(each.value.content.params.delete_source_files, null)
  }
  depends_on = [google_bigquery_dataset.datasets, google_bigquery_table.tables, google_storage_bucket.buckets, google_service_account.execution_sa]
}
