terraform {
  backend "remote" {
    organization = "devops-deploy-platform"

    workspaces {
      name = "devops-deploy-platform"
    }
  }
}
