resource "kubernetes_service" "devops_api" {
  wait_for_load_balancer = false

  metadata {
    name      = "devops-api"
    namespace = kubernetes_namespace.devops.metadata[0].name
  }

  spec {
    selector = {
      app = "devops-api"
    }

    port {
      port        = var.api_port
      target_port = var.api_port
      node_port   = var.api_node_port
    }

    type = "NodePort"
  }
}
