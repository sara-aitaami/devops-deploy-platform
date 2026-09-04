resource "kubernetes_config_map" "terraform_info" {
  metadata {
    name      = "terraform-info"
    namespace = kubernetes_namespace.devops.metadata[0].name
  }

  data = {
    managed_by  = "terraform"
    project     = var.project_name
    phase       = "phase-e"
    environment = var.environment
  }
}
