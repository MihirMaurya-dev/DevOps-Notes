---
tags: [azure, containers, acr, docker]
source: devopsinsiders/batch-18
created: 2026-06-14
updated: 2026-06-14
---

# Azure Container Registry (ACR)

Azure Container Registry (ACR) is a managed, private Docker registry service based on the open-source Docker Registry 2.0. It is used to store and manage container images and related artifacts (like Helm charts) for your Kubernetes deployments or App Services.

## Key Features

1. **Security & RBAC:**
   - ACR integrates natively with Entra ID.
   - You can assign specific roles: `AcrPull` (for AKS to download images), `AcrPush` (for CI/CD pipelines to upload images), and `AcrDelete`.
   - **Best Practice:** Always disable the `admin_enabled` credential, as it provides unrestricted push/pull access via a static username/password. Rely entirely on Managed Identities or Service Principals.

2. **Network Security:**
   - **Premium Tier:** Allows you to completely disable public internet access and force all image pulls to go through an Azure **Private Endpoint**. This ensures your proprietary source code/images never traverse the public internet.

3. **Geo-Replication:**
   - Available in the Premium tier, this allows a single registry to be replicated across multiple Azure regions. An AKS cluster in West Europe will automatically pull from the local West Europe replica, reducing latency and egress costs.

4. **ACR Tasks:**
   - A suite of features that provide cloud-based container image building (similar to Docker Hub automated builds) and OS/Framework patching.

## Terraform Implementation Snippet

```hcl
resource "azurerm_container_registry" "acr" {
  name                = "crcontosoprod001" # Must be globally unique, alphanumeric only
  resource_group_name = azurerm_resource_group.shared_rg.name
  location            = azurerm_resource_group.shared_rg.location
  sku                 = "Premium"
  admin_enabled       = false # Security best practice
  
  public_network_access_enabled = false # Force Private Endpoint usage

  # Optional Geo-Replication
  georeplications {
    location                = "westeurope"
    zone_redundancy_enabled = true
  }
}

# Granting AKS permission to pull images from ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}
```

## Integration with AKS
When deploying AKS, you must ensure that the cluster's Kubelet Managed Identity has the `AcrPull` RBAC role assigned over the ACR resource. Without this, Kubernetes will throw an `ImagePullBackOff` or `ErrImagePull` error.
