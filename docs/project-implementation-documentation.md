# Journal API Project Implementation Documentation

## 1. Project Summary

This project delivers a cloud-deployed Journal API using:

- FastAPI application runtime
- PostgreSQL database
- Docker containerization
- Terraform-based infrastructure provisioning on AWS
- GitHub Actions CI/CD pipeline
- Kubernetes deployment on Amazon EKS
- Monitoring and observability with Prometheus and Grafana

The application is deployed to AWS and operated through Kubernetes manifests and automated pipeline stages.

## 2. Solution Architecture

### 2.1 Core Components

- Application: FastAPI service from api/
- Database: Amazon RDS PostgreSQL 15
- Container Registry: Amazon ECR repository
- Compute Orchestration: Amazon EKS managed cluster + node group
- Delivery: GitHub Actions workflow in .github/workflows/cm.yml
- Monitoring: Prometheus + Grafana deployed inside the cluster via k8s/monitoring/

### 2.2 Runtime Flow

1. Client calls Journal API endpoints.
2. Journal API reads/writes journal entries to PostgreSQL.
3. Application exposes metrics endpoint for scraping.
4. Prometheus scrapes API and self metrics.
5. Grafana visualizes metrics with a provisioned dashboard.

## 3. Containerization

### 3.1 Docker Build Strategy

Container build is defined in Dockerfile.

Key steps:

1. Base image: python:3.12-slim
2. Working directory: /app
3. Dependency manager: uv copied from official uv container image
4. Runtime environment variable set for imports:
   - ENV PYTHONPATH=/app
5. Dependency layer optimization:
   - Copy pyproject.toml and uv.lock first
   - Run uv sync --no-dev
6. Copy full application source
7. Expose port 8000
8. Start server with uvicorn (api.main:app)

### 3.2 Runtime Entrypoint

- Command runs FastAPI on 0.0.0.0:8000.
- This aligns with Kubernetes Service targetPort 8000.

### 3.3 Image Tagging and Registry

In CI, images are built and pushed to ECR with:

- Immutable SHA tag
- latest tag

Repository pattern in AWS:

- 362976989244.dkr.ecr.us-east-1.amazonaws.com/jj/journalapi

## 4. Infrastructure as Code (Terraform)

Terraform code is in infra/.

### 4.1 Provider and Backend

- Provider: hashicorp/aws (~> 5.0)
- Required Terraform version: >= 1.6.0
- Backend: S3 backend block prepared for remote state and locking configuration

### 4.2 Provisioned AWS Resources

From infra/main.tf:

1. ECR repository
   - Mutable tags
   - Scan on push enabled
   - AES256 encryption

2. IAM roles and policy attachments
   - EKS cluster role
   - EKS node role
   - Attachments for EKS worker, CNI, ECR read-only, SSM

3. EKS cluster
   - Version configurable (default 1.30)
   - Private subnet placement

4. EKS managed node group
   - Scalable node group with desired/min/max parameters
   - Update strategy max_unavailable = 1

5. Networking and data plane resources for database
   - RDS security group allowing 5432 from VPC CIDR
   - DB subnet group across private subnets

6. RDS PostgreSQL instance
   - Engine: postgres 15
   - Encrypted storage
   - Backup retention period 7 days
   - Private only (not publicly accessible)

### 4.3 Terraform Variables

Defined in infra/variables.tf:

- Environment naming and AWS region
- Existing VPC and private subnets
- EKS version and node scaling settings
- RDS class, storage, db credentials, multi-AZ toggle

### 4.4 Terraform Outputs

Defined in infra/outputs.tf:

- ECR repository URL
- Sensitive DB connection string
- EKS kubeconfig helper details and update command

## 5. CI/CD Pipeline

Pipeline is defined in .github/workflows/cm.yml.

### 5.1 Trigger Conditions

- Push to main
- Pull request
- Manual workflow_dispatch

### 5.2 Pipeline Stages

1. preflight
   - Install Python and uv
   - Install dependencies
   - Run:
     - ruff lint checks
     - ty type checks

2. test
   - Depends on preflight
   - Starts PostgreSQL 15 service container
   - Waits for DB readiness
   - Applies schema via database_setup.sql
   - Runs pytest with DATABASE_URL

3. build-and-push
   - Runs only on push to main after tests
   - Configures AWS credentials
   - Logs into ECR
   - Builds Docker image
   - Tags with commit SHA and latest
   - Pushes both tags to ECR

4. deploy
   - Runs only on push to main after build-and-push
   - Configures AWS credentials
   - Sets up kubectl
   - Updates kubeconfig for EKS
   - Replaces IMAGE_PLACEHOLDER in k8s/deployment.yaml
   - Applies manifests from k8s/

### 5.3 Required GitHub Secrets

At minimum, pipeline references:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- EKS_CLUSTER_NAME
- OPENAI_API_KEY (test runtime)

## 6. Container Orchestration (Kubernetes)

### 6.1 Application Deployment

Kubernetes manifests are in k8s/:

- k8s/deployment.yaml
- k8s/service.yaml
- k8s/secret.example.yaml

Deployment characteristics:

- 2 replicas
- LoadBalancer service for external reachability
- Readiness and liveness probes (HTTP GET /health on 8000)
- Secret-backed env loading via envFrom using journal-secrets
- Application health endpoint exposed at /health

Service exposure:

- journal-api-service on port 80, forwarding to container port 8000

### 6.2 Deployment Pattern

CI deploy stage injects image URI and applies manifests.

Operationally, this gives repeatable rolling updates and health-gated rollout behavior.

## 7. Monitoring and Observability

Monitoring manifests are in k8s/monitoring/.

### 7.1 Application Instrumentation

In api/main.py:

- FastAPI instrumentation is enabled.
- Prometheus metrics endpoint is exposed via prometheus-fastapi-instrumentator.

### 7.2 Prometheus

Configured via k8s/monitoring/prometheus-configmap.yaml:

- Scrape interval: 15s
- Scrape targets:
  - Prometheus self target localhost:9090
  - Journal API target journal-api-service.default.svc.cluster.local:80
- Metrics path for API target: /metrics/

Deployed as:

- prometheus deployment
- prometheus service

### 7.3 Grafana

Configured and deployed via:

- grafana deployment and service
- provisioned Prometheus datasource
- provisioned dashboard provider
- preloaded dashboard JSON: Journal API Overview

Dashboard covers:

- Request throughput
- Error behavior
- Latency indicators
- Target health panels

### 7.4 Local Access Runbook

To check Grafana from a personal machine:

1. Ensure AWS and kubectl access is valid.
2. Refresh kubeconfig:
   - aws eks update-kubeconfig --region us-east-1 --name journal-api-dev-eks
3. Free local port if needed:
   - lsof -ti tcp:3000 | xargs kill -9 2>/dev/null || true
4. Port-forward:
   - kubectl port-forward svc/grafana-service 3000:3000
5. Open browser:
   - http://localhost:3000

### 7.5 Verification Commands

Prometheus target health:

- kubectl port-forward svc/prometheus-service 9090:9090
- curl -s "http://localhost:9090/api/v1/targets"

Expected target state for journal-api:

- health: up
- lastError: empty

## 8. Security and Operational Notes

### 8.1 Security Controls Implemented

- Kubernetes secrets used for sensitive runtime env values
- RDS not publicly accessible
- ECR image scanning enabled on push
- Encrypted storage for database

### 8.2 Recommended Hardening Next Steps

1. Move Grafana admin credentials to Kubernetes Secret and rotate defaults.
2. Restrict Grafana exposure via controlled Ingress and TLS.
3. Add persistent volumes for Prometheus and Grafana data durability.
4. Add alerting rules for API down, high 5xx, and high latency.
5. Use OIDC for GitHub Actions to AWS instead of long-lived AWS keys.

## 9. Delivery Checklist Mapping

The project has implemented the requested areas:

1. Containerization of the application
   - Dockerfile with reproducible build and runtime startup

2. Infrastructure as code
   - Terraform modules for ECR, EKS, IAM, and RDS

3. CI/CD pipeline
   - Preflight, test, build/push, and deploy stages in GitHub Actions

4. Container orchestration
   - Kubernetes deployment/service manifests with health probes and secrets

5. Monitoring and observability
   - Prometheus + Grafana stack with dashboard provisioning and API metrics scraping

## 10. Reference Files

- Dockerfile
- .github/workflows/cm.yml
- infra/main.tf
- infra/providers.tf
- infra/variables.tf
- infra/outputs.tf
- k8s/deployment.yaml
- k8s/service.yaml
- api/main.py
- k8s/monitoring/prometheus-configmap.yaml
- k8s/monitoring/grafana-deployment.yaml
- k8s/monitoring/grafana-dashboard-configmap.yaml
- k8s/monitoring/README.md
