---
name: Monitoring and observability

description: Set up monitoring to track your application's health and performance. This step is not auto-verified but is essential for production readiness.

# Skill Instructions (AWS only)
1.
Add prometheus-fastapi-instrumentator to your project dependencies (exposes /metrics endpoint automatically)

2.
Deploy Prometheus and Grafana in your K8s cluster (via manifests in k8s/monitoring/ or kube-prometheus-stack Helm chart)

3.
Configure Prometheus to scrape your Journal API's /metrics endpoint

4.
Set up a Grafana dashboard to visualize request latency, error rates, and pod health



