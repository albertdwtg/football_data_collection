resource "google_cloudbuild_trigger" "terraform_trigger" {
  name     = "terraform-apply-trigger"
  location = "global"

  github {
    owner = "albertdwtg"
    name  = "football_data_collection"
    push {
      branch = "^main$" # Déclencher lors des push sur la branche main
    }
  }

  filename = "cicd/cloudbuild.yaml" # Référence au fichier cloudbuild.yaml
}
