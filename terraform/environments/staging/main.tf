terraform {
  required_version = ">= 1.5.0"
}

module "network" { source = "../../modules/network" }
module "cluster" { source = "../../modules/cluster" }
module "registry" { source = "../../modules/registry" }
