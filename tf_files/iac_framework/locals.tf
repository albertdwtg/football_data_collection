locals {
  common_labels = {
    "env" : var.env
    "module" : var.module
    "product" : var.product_name
    "region" : var.region
    "region_id" : var.region_id
  }
}
