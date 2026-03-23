---
name: CI/CD pipeline
description: Apply the GitHub Actions workflow i built in the CI/CD Pipelines . It should trigger on every push to main with at least three jobs.


# Skill Instructions (AWS only)
1.
Test job — Run linting and tests with a PostgreSQL 15 service container, run database_setup.sql before pytest, install uv using astral-sh/setup-uv.

2.
Build & Push job — Build the Docker image and push to your container registry, tagged with commit SHA and latest

3.
Deploy job — Connect to your K8s cluster, sed-substitute the image placeholder, apply manifests from k8s/ folder

4.
AZURE_CREDENTIALS secret — output of az ad sp create-for-rbac --sdk-auth

5
ACR_LOGIN_SERVER secret — your ACR login server URL.

6. 
ACR_USERNAME secret — ACR username

7. 
ACR_PASSWORD secret — ACR password

8.
AZURE_RESOURCE_GROUP secret — your resource group name

9.
AKS_CLUSTER_NAME secret — your AKS cluster name




