output "terraform_config_map_name" {
  description = "Name of the ConfigMap managed by Terraform"
  value       = kubernetes_config_map.terraform_info.metadata[0].name
}

output "kubernetes_namespace" {
  description = "Kubernetes namespace managed by Terraform"
  value       = kubernetes_namespace.devops.metadata[0].name
}

output "api_service_name" {
  description = "Name of the API Kubernetes Service"
  value       = kubernetes_service.devops_api.metadata[0].name
}

output "api_port" {
  description = "Port exposed by the API Kubernetes Service"
  value       = kubernetes_service.devops_api.spec[0].port[0].port
}

output "api_node_port" {
  description = "NodePort exposed for the API Kubernetes Service"
  value       = kubernetes_service.devops_api.spec[0].port[0].node_port
}
