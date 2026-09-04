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

variable "api_port" {
  description = "Port exposed by the API Kubernetes Service"
  type        = number
  default     = 8000

  validation {
    condition     = var.api_port >= 1 && var.api_port <= 65535
    error_message = "api_port must be between 1 and 65535."
  }
}

variable "api_node_port" {
  description = "NodePort exposed for the API Kubernetes Service"
  type        = number
  default     = 30080

  validation {
    condition     = var.api_node_port >= 30000 && var.api_node_port <= 32767
    error_message = "api_node_port must be between 30000 and 32767."
  }
}
