output "ecr_repository_url" {
  description = "ECR repository URL to push journal API images"
  value       = aws_ecr_repository.journal_api.repository_url
}

output "db_connection_string" {
  description = "PostgreSQL connection string for application configuration"
  value       = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.journal_postgres.address}:5432/${var.db_name}"
  sensitive   = true
}

output "kubeconfig" {
  description = "Connection info for configuring kubectl against the EKS cluster"
  value = {
    cluster_name               = aws_eks_cluster.this.name
    endpoint                   = aws_eks_cluster.this.endpoint
    certificate_authority_data = aws_eks_cluster.this.certificate_authority[0].data
    update_command             = "aws eks update-kubeconfig --name ${aws_eks_cluster.this.name} --region ${var.aws_region}"
  }
}
