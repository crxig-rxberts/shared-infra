provider "aws" {
  region = "eu-west-1"
}

terraform {
  backend "local" {
    path = "state/terraform.tfstate"
  }
}
