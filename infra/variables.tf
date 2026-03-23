variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project/application name used for resource naming"
  type        = string
  default     = "journal-api"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "dev"
}

variable "vpc_id" {
  description = "Existing VPC ID where EKS and RDS are deployed"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC used to scope database ingress"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used for EKS node groups and RDS"
  type        = list(string)
}

variable "eks_version" {
  description = "EKS Kubernetes version"
  type        = string
  default     = "1.30"
}

variable "node_instance_types" {
  description = "Instance types for EKS managed node group"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "journal"
}

variable "db_username" {
  description = "PostgreSQL admin username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "PostgreSQL admin password"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "RDS storage in GiB"
  type        = number
  default     = 20
}

variable "db_multi_az" {
  description = "Whether to run the database in multi-AZ mode"
  type        = bool
  default     = false
}
