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
      port        = 8000
      target_port = 8000
      node_port   = 30080
    }

    type = "NodePort"
  }
}
