output "terraform_config_map_name" {
  description = "Name of the ConfigMap managed by Terraform"
  value       = kubernetes_config_map.terraform_info.metadata[0].name
}