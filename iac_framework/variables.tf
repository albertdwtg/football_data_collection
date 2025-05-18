variable "project" {
  type        = string
  description = "GCP project ID"
}

variable "module" {
  type        = string
  description = "Module name of the deployed resources"
}

variable "product_name" {
  type        = string
  description = "Name of the product. It's the object composed by all the resources"
}

variable "region" {
  type        = string
  description = "Region where to deploy resources"
}

variable "region_id" {
  type        = string
  description = "Region trigram where to deploy resources"
}

variable "env" {
  type        = string
  description = "Name of the current environment"
  validation {
    condition     = contains(["dev", "prd"], var.env)
    error_message = "Provide a correct env value, can be 'dev' or 'prd'"
  }
}

locals {
  user_variables = try(yamldecode(
    templatefile(
      "../../../modules/${var.module}/${local.resources_folder}/variables.yaml",
      {
        project : var.project
        region : var.region
        region_id : var.region_id
        module : var.module
        product_name : var.product_name
        env : var.env
      }
    )
  ), {})
}
