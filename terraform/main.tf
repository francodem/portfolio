terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67.0"
    }
  }
  required_version = ">= 1.4" 
}

provider "aws" {
    region = "us-east-1"
}

variable "sec_group_name" {
    type    = string
    default = "test_env_security"
}

variable "ec2_name" {
    type    = string
    default = "frmo_portfolio"
}

resource "aws_instance" "ec2" {
    ami                 = "ami-053b0d53c279acc90"
    instance_type       = "t2.micro"
    key_name            = "personal"
    tags                = {
        Name = var.ec2_name
    }

    // Put it into a security group
    security_groups     = [var.sec_group_name]

    // Apllying more local storage
    root_block_device {
        volume_size     = 8
        volume_type     = "gp2"
    }
}