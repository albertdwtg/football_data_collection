terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.6.0"
    }
  }
  backend "gcs" {
  }
}

provider "google" {
  project = var.project
}