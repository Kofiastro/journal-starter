# Infra Preflight (Terraform)

This directory contains Terraform for AWS infrastructure used by the journal API:

- ECR repository for container images
- EKS cluster + managed node group
- RDS PostgreSQL 15 instance
- IAM roles/policies for EKS and ECR pull access

## Files

- `providers.tf`: Terraform and provider configuration
- `variables.tf`: input variables
- `main.tf`: core resources
- `outputs.tf`: exported values
- `terraform.tfvars`: environment values (already git-ignored)

## Preflight commands

Run from this directory:

```bash
terraform init
terraform fmt -check
terraform validate
```

## Backend setup (S3 + DynamoDB)

Run from this directory:

```bash
cat > backend.hcl <<'EOF'
bucket         = "your-terraform-state-bucket"
key            = "journal-api/dev/terraform.tfstate"
region         = "us-east-1"
dynamodb_table = "your-terraform-locks"
encrypt        = true
EOF
```

```bash
terraform init -reconfigure -backend-config=backend.hcl
```

If this is a new backend with no existing state object yet:

```bash
terraform init -migrate-state -reconfigure -backend-config=backend.hcl
```

## Secret-safe deploy commands

Do not store `db_password` in `terraform.tfvars`. Pass it at runtime:

```bash
export TF_VAR_db_password='REPLACE_WITH_STRONG_PASSWORD'
terraform plan
terraform apply
```

Single-command alternative:

```bash
TF_VAR_db_password='REPLACE_WITH_STRONG_PASSWORD' terraform plan
TF_VAR_db_password='REPLACE_WITH_STRONG_PASSWORD' terraform apply
```

## Deploy

```bash
terraform plan
terraform apply
```

## Post-provision database setup

After apply, run the SQL bootstrap against your RDS endpoint:

```bash
psql "postgresql://<username>:<password>@<rds-endpoint>:5432/<db-name>" -f ../database_setup.sql
```
