---
tags: [project, aks, kubernetes, platform]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Project: AKS Enterprise Platform

## Overview
Design and deploy a production-grade Azure Kubernetes Service (AKS) cluster that acts as a multi-tenant platform for several internal development teams.

## Architecture Diagram

```
                        Internet
                            │
                            ▼
                ┌───────────────────────┐
                │  App Gateway (WAF)    │  ← HTTPS 443 only, WAF in Prevention mode
                │  agw-subnet           │
                └───────────┬───────────┘
                            │
              ┌─────────────▼──────────────┐
              │       AKS Spoke VNet       │
              │                            │
              │  ┌─────────────────────┐   │
              │  │   AKS Nodes Subnet  │   │
              │  │  (VMSS Node Pools)  │   │
              │  │  ┌───────────────┐  │   │
              │  │  │ NGINX Ingress │  │   │  ← Internal LB (private IP only)
              │  │  │  (Int. LB)   │  │   │
              │  │  └──────┬────────┘  │   │
              │  │         │ (pods)    │   │
              │  └─────────┼───────────┘   │
              │            │               │
              │  ┌─────────▼───────────┐   │
              │  │  Private Link Subnet│   │
              │  │  ● ACR (PE)         │   │  ← No public registry access
              │  │  ● Key Vault (PE)   │   │  ← Secrets via Managed Identity
              │  └─────────────────────┘   │
              └─────────────┬──────────────┘
                            │ VNet Peering
              ┌─────────────▼──────────────┐
              │          Hub VNet          │
              │  ● Azure Firewall          │  ← All egress traffic inspected
              │  ● VPN / ExpressRoute GW   │  ← On-premises connectivity
              │  ● Azure Bastion           │  ← Secure SSH/RDP (no public IPs)
              └────────────────────────────┘
```

## Architecture Description
The architecture follows a Hub and Spoke model.
- **Hub VNet:** Contains Azure Firewall, VPN Gateway for on-premises connectivity, and central Bastion.
- **AKS Spoke VNet:** Connected via VNet Peering to the Hub.
  - **App Gateway WAF Subnet:** Houses the Application Gateway with WAF enabled to inspect incoming HTTP/HTTPS traffic from the internet.
  - **AKS Nodes Subnet:** Where the AKS VMSS nodes reside.
  - **Private Link Subnet:** Used for Azure Container Registry (ACR) and Azure Key Vault Private Endpoints.

Traffic flows from the Internet → Azure App Gateway (WAF) → NGINX Ingress Controller (Internal Load Balancer) → AKS Pods.

## Terraform Implementation Snippet

### AKS Cluster Configuration

```hcl
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-enterprise-prod"
  location            = azurerm_resource_group.aks_rg.location
  resource_group_name = azurerm_resource_group.aks_rg.name
  dns_prefix          = "aks-enterprise-prod"
  kubernetes_version  = "1.28.5"
  private_cluster_enabled = true # Do not expose API server to internet

  default_node_pool {
    name           = "system"
    node_count     = 3
    vm_size        = "Standard_DS2_v2"
    vnet_subnet_id = azurerm_subnet.aks_subnet.id
    zones          = ["1", "2", "3"]
    only_critical_addons_enabled = true # Taint: CriticalAddonsOnly
  }

  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
    dns_service_ip     = "192.168.100.10"
    service_cidr       = "192.168.100.0/24"
    docker_bridge_cidr = "172.17.0.1/16"
  }

  azure_active_directory_role_based_access_control {
    managed                = true
    azure_rbac_enabled     = true
    admin_group_object_ids = [azuread_group.aks_admins.object_id]
  }

  identity {
    type = "SystemAssigned"
  }

  linux_profile {
    admin_username = "aksadmin"
    ssh_key {
      key_data = var.ssh_public_key
    }
  }

  lifecycle {
    ignore_changes = [default_node_pool[0].node_count]
  }
}
```

### Node Pools
```hcl
resource "azurerm_kubernetes_cluster_node_pool" "user_memory" {
  name                  = "memorypool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size               = "Standard_E4s_v3"
  node_count            = 2
  vnet_subnet_id        = azurerm_subnet.aks_subnet.id
  zones                 = ["1", "2", "3"]
  
  node_labels = {
    "workload" = "memory-intensive"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "user_cpu" {
  name                  = "cpupool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size               = "Standard_F4s_v2"
  node_count            = 2
  vnet_subnet_id        = azurerm_subnet.aks_subnet.id
  zones                 = ["1", "2", "3"]

  node_labels = {
    "workload" = "cpu-intensive"
  }
}
```

## Ingress Deployment (Helm)
The Nginx Ingress Controller must be deployed using an Internal Load Balancer annotation so it gets an IP from the AKS subnet.

```yaml
controller:
  service:
    annotations:
      service.beta.kubernetes.io/azure-load-balancer-internal: "true"
      service.beta.kubernetes.io/azure-load-balancer-internal-subnet: "aks-subnet"
```

## Key Design Decisions
- **Azure CNI vs Kubenet:** Chosen Azure CNI for advanced VNet integration and network policies, despite the IP address consumption overhead.
- **Private Cluster:** `private_cluster_enabled = true` was set to prevent the control plane API server from being exposed publicly.
- **System-Assigned Identity:** Selected over Service Principal for seamless rotation and native Azure integration.

## Monitoring Setup
- **Container Insights:** Enabled `oms_agent` addon to forward metrics to Log Analytics.
- **Prometheus/Grafana:** Deployed kube-prometheus-stack via Helm for rich dashboarding and Alertmanager integration for pod crash alerting.

## Lessons Learned

| # | Problem Faced | Root Cause | Solution Applied |
|---|--------------|------------|------------------|
| 1 | **IP Exhaustion with Azure CNI** | Provisioned `/24` subnet. Azure CNI gives each pod a real VNet IP — 3 nodes × 30 pods = 90 IPs instantly | Recreated cluster with a `/22` subnet (1022 usable IPs) |
| 2 | **Private Cluster API unreachable from CI** | `private_cluster_enabled = true` blocks public API access, including Azure DevOps hosted agents | Set up a **self-hosted agent VM** in the Hub VNet; linked the Private DNS Zone to Hub VNet |
| 3 | **ACR Pull failure after Private Endpoint** | Helm charts pulled images using public ACR FQDN, which stopped resolving after Private Endpoint | Linked Private DNS Zone `privatelink.azurecr.io` to AKS spoke VNet |
| 4 | **Node pool upgrade caused downtime** | Upgraded node pool without surge nodes configured | Set `max_surge = "1"` on node pool to ensure rolling upgrades with zero downtime |
| 5 | **`ignore_changes` on node_count critical** | Cluster Autoscaler changes node_count at runtime; Terraform would reset it on next apply | Added `ignore_changes = [default_node_pool[0].node_count]` in lifecycle block |

## Production Readiness Checklist
- [ ] AKS private cluster enabled — API server not publicly accessible
- [ ] Azure CNI with `/22` or larger subnet for pod IP headroom
- [ ] NGINX Ingress uses Internal Load Balancer annotation
- [ ] ACR and Key Vault accessed via Private Endpoints only
- [ ] Cluster Autoscaler enabled with `max_surge` set on node pools
- [ ] Container Insights + Prometheus/Grafana deployed
- [ ] Self-hosted CI agent in Hub VNet for pipeline access to private API
- [ ] Workload Identity (OIDC) used instead of Service Principal for pod authentication
