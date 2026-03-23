# Monitoring Stack (Preflight)

This folder contains Kubernetes manifests for Prometheus and Grafana.

## What gets deployed

- Prometheus (`prometheus-*` files)
- Grafana (`grafana-*` files)
- A pre-provisioned Grafana dashboard: `Journal API Overview`

## Apply manifests

From the repository root:

```bash
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml
kubectl apply -f k8s/monitoring/prometheus-service.yaml
kubectl apply -f k8s/monitoring/grafana-datasource-configmap.yaml
kubectl apply -f k8s/monitoring/grafana-dashboard-provider-configmap.yaml
kubectl apply -f k8s/monitoring/grafana-dashboard-configmap.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/grafana-service.yaml
```

## Access Grafana

Use port-forwarding:

```bash
kubectl port-forward svc/grafana-service 3000:3000
```

Then open `http://localhost:3000`.

- Username: `admin`
- Password: `admin`

## Prometheus scrape target

Prometheus is configured to scrape:

- `journal-api-service.default.svc.cluster.local:80/metrics`

This relies on the Journal API exposing `/metrics` and the `journal-api-service` service existing in the `default` namespace.
