variable "environment" {
  description = "Environment managed by Terraform"
  type        = string
  default     = "local"
}

variable "namespace" {
  description = "Kubernetes namespace managed by Terraform"
  type        = string
  default     = "devops"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "devops-deploy-platform"
}