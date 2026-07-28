---
tags: [devops, azure, cost-governance, kubernetes, opencost, aks]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# OpenCost — Open-source Kubernetes Cost Monitoring

## Basics
**OpenCost** is an open-source, vendor-neutral project for measuring and allocating infrastructure and container costs in Kubernetes environments. Originally built by Kubecost, it provides a standardized way to calculate cost metrics directly within your cluster.

## Why it matters
Azure Cost Management gives you the total cost of your Azure Kubernetes Service (AKS) cluster, but it cannot see *inside* the cluster. If you have 5 teams sharing one AKS cluster, Azure Cost Management can't tell you how much each team is spending. OpenCost solves this by allocating the cluster's total cost down to the namespace, deployment, pod, or even label level. This enables **chargeback** (billing teams for what they use) and **showback** (showing teams what they use to build awareness).

## How it works
OpenCost runs as a pod within your AKS cluster. It works by:
1. Scraping resource usage metrics (CPU, Memory, Storage, Network) from Prometheus.
2. Connecting to the Azure Retail Prices API to get the exact billing rates for your specific VM sizes and disks.
3. Combining usage data with pricing data to calculate the exact cost of each Kubernetes workload over time.

## Azure implementation (with code/CLI)

### 1. Install Prometheus (Pre-requisite)
OpenCost requires Prometheus for metrics collection.
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus \
  --namespace prometheus-system --create-namespace
```

### 2. Install OpenCost on AKS
Install OpenCost using Helm and configure it to use the Azure pricing API.

```bash
helm repo add opencost https://opencost.github.io/helm-charts
helm install opencost opencost/opencost \
  --namespace opencost --create-namespace \
  --set opencost.exporter.defaultClusterId="my-aks-cluster" \
  --set opencost.prometheus.internal.serviceName="prometheus-server.prometheus-system.svc" \
  --set opencost.exporter.cloudProviderApiKey="<your-azure-api-key-if-using-custom-pricing>"
```

### 3. Integration with Grafana
OpenCost exposes standard Prometheus metrics (`node_total_hourly_cost`, `pod_total_hourly_cost`). You can import the official OpenCost Grafana dashboard (Dashboard ID: `18684`) to visualize these costs.

## Production best practices
- **Labeling Strategy**: Enforce mandatory labels on all pods (e.g., `team: frontend`, `cost-center: 1234`). OpenCost aggregates costs based on these labels.
- **Namespace-level Allocation**: Create a dedicated namespace per team or project. This makes cost allocation trivial compared to relying solely on labels.
- **Persistent Storage**: Ensure Prometheus is configured with a Persistent Volume (PV) to retain cost metrics across pod restarts.
- **Azure Spot VMs**: Mix spot and regular node pools in AKS. OpenCost will automatically detect the lower price of spot instances and reflect the accurate cost.

## CI/CD integration
You can automate the extraction of cost reports and send them to your teams weekly.

### GitHub Actions Example
```yaml
name: Weekly Cost Report
on:
  schedule:
    - cron: '0 8 * * 1' # Every Monday at 8 AM

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - name: Get AKS Credentials
        run: az aks get-credentials --resource-group myRG --name myAKS

      - name: Query OpenCost API
        run: |
          kubectl port-forward --namespace opencost service/opencost 9003:9003 &
          sleep 5
          curl -s "http://localhost:9003/allocation/compute?window=7d" > cost-report.json
          
      - name: Send to Slack
        run: ./scripts/send-slack-alert.sh cost-report.json
```

## Interview Q&A

1. **Why do we need OpenCost if we already have Azure Cost Management?**
   *Answer*: Azure Cost Management sees the AKS cluster as a single black box. OpenCost provides visibility inside the cluster, allocating costs to specific namespaces, pods, and labels, which is essential for multi-tenant clusters.

2. **How does OpenCost calculate the cost of a specific pod?**
   *Answer*: It pulls the pod's CPU, RAM, and storage usage metrics from Prometheus, and multiplies that usage by the hourly rate of the underlying Azure VM (node) fetched from the Azure pricing API.

3. **What is the difference between Showback and Chargeback?**
   *Answer*: Showback is simply reporting the cost to the responsible team to raise awareness. Chargeback goes a step further and actually bills that team's specific budget or department for their cloud usage.
