module "iac_framework" {
  source       = "./iac_framework"
  project      = var.project
  module       = var.module
  region       = var.region
  region_id    = var.region_id
  env          = var.env
  product_name = var.product_name
}
