---
tags: [architecture, patterns, shared-services]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Architecture Pattern: Shared Services

In an enterprise environment, many applications require access to the exact same supporting services (like Active Directory, DNS, monitoring, or security scanning tools). Deploying these services separately for every single application is extremely expensive and difficult to maintain.

## The Shared Services Pattern
Instead, you deploy these common resources into a **Shared Services Subnet** or a dedicated **Shared Services VNet** (often synonymous with the Hub VNet in a Hub and Spoke design).

## Breakdown of Shared Services

### 1. Identity Services
Identity is the core of most enterprise applications. 
- **Active Directory Domain Services (AD DS) VMs:** Traditional domain controllers hosted on IaaS VMs. Used when full domain admin rights or legacy Kerberos/NTLM authentication is heavily relied upon by older applications. Requires you to patch and manage the VMs.
- **Microsoft Entra Domain Services:** A managed PaaS version of AD. Good for lifting and shifting legacy apps without managing DC VMs.
- **Comparison:** Entra DS is easier to manage but lacks Enterprise/Domain Admin privileges and does not support trust relationships to on-premises AD in the same way full AD DS VMs do.

### 2. Private DNS Resolution
- Azure Private DNS Zones (`privatelink.database.windows.net`) are centrally hosted in the Shared Services or Hub subscription.
- VNet Links connect these central zones to all Spoke VNets, ensuring any Spoke can resolve the private IP of a PaaS service located in another Spoke.

### 3. CI/CD Self-Hosted Runners
- To deploy to private AKS clusters or private SQL databases without exposing them to the internet, CI/CD pipelines need agents inside the network.
- **Implementation:** Deploy Azure VM Scale Sets running Azure DevOps Agents or GitHub Actions Runners in a dedicated subnet in the Shared Services VNet.

### 4. Container Registries (ACR)
- A single, central Azure Container Registry (ACR) should be used to store base images and approved third-party images.
- Connect it using a Private Endpoint in the Shared Services VNet so Spoke AKS clusters can pull images securely over the Azure backbone.

## Terraform Implementation Example (Hub & Private DNS)

```hcl
# The central Hub VNet
resource "azurerm_virtual_network" "hub" {
  name                = "vnet-hub-shared"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.shared.location
  resource_group_name = azurerm_resource_group.shared.name
}

# Subnet for Shared CI/CD Runners
resource "azurerm_subnet" "runners" {
  name                 = "snet-runners"
  resource_group_name  = azurerm_resource_group.shared.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Central Private DNS Zone for Key Vault
resource "azurerm_private_dns_zone" "kv_zone" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.shared.name
}

# Link the DNS Zone to the Hub VNet
resource "azurerm_private_dns_zone_virtual_network_link" "hub_link" {
  name                  = "link-hub-to-kv-zone"
  resource_group_name   = azurerm_resource_group.shared.name
  private_dns_zone_name = azurerm_private_dns_zone.kv_zone.name
  virtual_network_id    = azurerm_virtual_network.hub.id
}
```

## Cost Optimization Strategies
- **Consolidation:** The primary cost saving of this pattern is avoiding N-number of firewalls, Bastion hosts, and VPN gateways in each Spoke.
- **Spot Instances for Runners:** Use Azure Spot VMs for self-hosted build runners if the pipeline can tolerate occasional evictions.
- **Reserved Instances:** Apply 1- or 3-year reservations to the Domain Controller VMs as they must run 24/7.

## Security Hardening Checklist
- [ ] Ensure the Shared Services VNet has no direct public inbound internet access.
- [ ] Route all outbound traffic from Shared Services through the Azure Firewall.
- [ ] Apply strict NSGs to the AD DS subnet (allow only DNS, Kerberos, LDAP, SMB from known Spoke IP ranges).
- [ ] Use JIT (Just-In-Time) access for any administrative SSH/RDP into the shared services VMs.
- [ ] Ensure the central ACR has admin user disabled and uses Entra ID RBAC for pull/push.
