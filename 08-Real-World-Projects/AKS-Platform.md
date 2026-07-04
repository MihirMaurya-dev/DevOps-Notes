---
tags: [project, aks, kubernetes, platform]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Project: AKS Enterprise Platform

## Overview
Design and deploy a production-grade Azure Kubernetes Service (AKS) cluster that acts as a multi-tenant platform for several internal development teams.

## Architecture Description
The architecture follows a Hub and Spoke model.
- **Hub VNet:** Contains Azure Firewall, VPN Gateway for on-premises connectivity, and central Bastion.
- **AKS Spoke VNet:** Connected via VNet Peering to the Hub.
  - **App Gateway WAF Subnet:** Houses the Application Gateway with WAF enabled to inspect incoming HTTP/HTTPS traffic from the internet.
  - **AKS Nodes Subnet:** Where the AKS VMSS nodes reside.
  - **Private Link Subnet:** Used for Azure Container Registry (ACR) and Azure Key Vault Private Endpoints.

Traffic flows from the Internet -> Azure App Gateway (WAF) -> NGINX Ingress Controller (Internal Load Balancer) -> AKS Pods.

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

## Lessons Learned
- **IP Exhaustion with Azure CNI:** Initially provisioned a `/24` subnet. With Azure CNI, each pod gets an IP from the VNet. With 3 nodes and max 30 pods per node, we quickly ran out of IPs. Solution: Recreated cluster with a `/22` subnet.
- **Private Cluster DNS Resolution:** Connecting to the private API server from the Azure DevOps pipeline required setting up a self-hosted agent in the Hub VNet and linking the Private DNS Zone.

## Monitoring Setup
- **Container Insights:** Enabled `oms_agent` addon to forward metrics to Log Analytics.
- **Prometheus/Grafana:** Deployed kube-prometheus-stack via Helm for rich dashboarding and Alertmanager integration for pod crash alerting.
