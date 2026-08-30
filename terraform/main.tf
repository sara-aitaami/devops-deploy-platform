resource "kubernetes_config_map" "terraform_info" {
  metadata {
    name      = "terraform-info"
    namespace = "devops"
  }

  data = {
    managed_by  = "terraform"
    project     = "devops-deploy-platform"
    phase       = "phase-e"
    environment = var.environment
  }
}