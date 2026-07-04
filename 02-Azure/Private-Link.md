---
category: Azure-Networking
tags: [azure, private-link, private-endpoint, security, zero-trust, architecture]
type: enterprise-architect-guide
status: active
---

# 🔗 Azure Private Link & Private Endpoint - Enterprise Architect Guide

## 1. Introduction
Azure Private Link enables you to access Azure PaaS Services (like Azure Storage, SQL Database, and Key Vault) over a private IP address within your Virtual Network (VNet). The network interface that sits in your VNet is called a **Private Endpoint**. This effectively brings the PaaS service inside your corporate network boundary.

## 2. Why This Service Exists
By default, Azure PaaS services are accessible over the public internet. While they are secured by Microsoft Entra ID authentication and firewall rules, many enterprise security policies (Zero Trust) mandate that no data should ever traverse or be exposed to the public internet. Private Endpoints solve this by removing the public endpoint entirely and replacing it with a private, internal IP address.

## 3. Architecture
- **Scope:** Regional.
- **Layer:** Network / Platform.
- **Under the Hood:** When you create a Private Endpoint, Azure provisions a Network Interface Card (NIC) in your selected subnet and assigns a private IP from your CIDR block. Traffic flowing from your VNet to the PaaS service routes securely over the Microsoft Azure backbone network — never touching the public internet.

## 4. Core Components
- **Private Endpoint:** The network interface (NIC) deployed into your VNet, holding the private IP address that represents the PaaS service.
- **Private Link Resource:** The destination PaaS service (e.g., Azure SQL, Cosmos DB, Storage Account).
- **Private DNS Zone:** Essential for overriding the public DNS name of the PaaS service so it resolves to your new private IP address internally (e.g., `privatelink.database.windows.net`).
- **Private Link Service:** A mechanism allowing you to offer your *own* custom application (behind a Standard Load Balancer) to other Azure customers or tenants via their own Private Endpoints.

## 5. Step-by-Step Request Flow
**Scenario:** A VM connects to an Azure SQL Database using a Private Endpoint.
1. The application attempts to connect to `mysqlserver.database.windows.net`.
2. The VNet's DNS setting resolves the query via an **Azure Private DNS Zone** (`privatelink.database.windows.net`).
3. The DNS returns the internal Private Endpoint IP (e.g., `10.0.1.5`) instead of the public IP.
4. The VM sends the SQL traffic to `10.0.1.5`.
5. The traffic hits the Private Endpoint NIC in the subnet.
6. Azure securely routes the traffic over the Microsoft backbone directly to the SQL Database.
7. The SQL Database, which has its public network access completely denied, accepts the connection via the Private Link.

## 6. Real-World Production Use Cases
1. **Zero-Trust Data Security:** Disabling public access on all Storage Accounts and Key Vaults, ensuring they can only be accessed by compute resources inside the VNet.
2. **On-Premises to PaaS:** Allowing a corporate office connected via ExpressRoute or VPN to access Azure PaaS services directly using private IP addresses, without traversing the public internet.
3. **Cross-Tenant PaaS Access:** Using Private Endpoints to securely access a vendor's Azure SQL database located in a completely different Microsoft Entra ID tenant, with explicit connection approval required.

## 7. Architecture & Design Considerations
- **DNS is the Hardest Part:** 99% of Private Endpoint issues are DNS-related. Because the application still connects using the public FQDN, you MUST intercept that DNS request and map it to the private IP via a Private DNS Zone. Failing to do so means the application resolves the public IP, which is blocked by the PaaS firewall.
- **Service Endpoints vs Private Endpoints:** Service Endpoints are a legacy approach — they route traffic over the Azure backbone, but the PaaS service still has a public IP. Private Endpoints assign a real private IP inside your VNet. **Always use Private Endpoints for new architectures.**

## 8. Microsoft Best Practices
- **Disable Public Access:** Merely creating a Private Endpoint does not make the service secure. You must explicitly go to the PaaS service's networking/firewall settings and select **"Deny Public Network Access"**.
- **Centralized DNS:** For Hub-and-Spoke architectures, deploy the Private DNS Zones in the Hub VNet and link all Spoke VNets to it. Do not create duplicate DNS zones in every Spoke — this causes DNS inconsistency.

## 9. Security Best Practices
- **NSG Support:** Private Endpoints now support Network Security Groups (NSGs). Apply NSGs to the Private Endpoint subnet to restrict which specific subnets or VMs can communicate with the Private Endpoint IP.
- **Approval Workflow:** Use the manual approval workflow when creating a Private Endpoint to a service in a different subscription or Entra ID tenant, ensuring the data owner explicitly approves the connection request.

## 10. Monitoring & Observability
- **Metrics:** Monitor `Bytes In` and `Bytes Out` on the Private Endpoint to track data volumes and detect potential data exfiltration or unexpected large transfers.
- **Diagnostic Logs:** Enable diagnostics on the target PaaS service (e.g., Azure SQL audit logs) to audit exactly who is connecting via the Private Link connection and what operations they are performing.

## 11. Backup & Disaster Recovery
- Private Endpoints are tied to a specific VNet and Region.
- **Disaster Recovery:** If you fail over a PaaS service (like geo-replicated Azure SQL) to a secondary region, you must pre-provision a corresponding Private Endpoint in the DR VNet pointing to the secondary replica so the application can reconnect immediately without DNS changes.

## 12. Cost Optimization Techniques
- Private Endpoints incur an hourly charge per endpoint, plus a data processing charge for inbound/outbound bandwidth (per GB).
- For massive data transfers (e.g., copying Terabytes to Blob Storage), evaluate whether Private Link data processing costs are acceptable. For one-time bulk migrations, a temporary Service Endpoint may be more cost-effective.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Private Endpoint?
   **A:** A network interface in your VNet that uses a private IP address to connect privately to Azure PaaS services (like Storage or SQL) without using the public internet.
2. **Q:** Why use Private Endpoints?
   **A:** They completely remove the PaaS service from the public internet, satisfying strict Zero Trust, compliance, and security requirements.

### Intermediate
3. **Q:** Service Endpoints vs Private Endpoints?
   **A:** Service Endpoints route traffic over the Azure backbone but the service still has a public IP address. Private Endpoints assign a real private IP inside your VNet and allow you to disable the public endpoint entirely.
4. **Q:** Why is DNS critical when implementing Private Endpoints?
   **A:** Because applications still connect using the service's public hostname (e.g., `mysqlserver.database.windows.net`). You must use Azure Private DNS Zones to override that hostname to resolve to the new private IP.
5. **Q:** What happens if you forget to configure the Private DNS Zone?
   **A:** The application will resolve the PaaS service to its public IP. The connection will fail because the public endpoint is blocked by the PaaS firewall rules — even though the Private Endpoint exists.

### Advanced
6. **Q:** Can on-premises networks access an Azure Private Endpoint?
   **A:** Yes, if the on-premises network is connected to the VNet via VPN or ExpressRoute, and the on-premises DNS is configured to conditionally forward requests for `privatelink.*` zones to the Azure Private DNS resolver (Azure DNS Private Resolver).
7. **Q:** What is Azure Private Link Service?
   **A:** It allows you to offer your own application (behind a Standard Load Balancer) as a Private Link service, so other Azure customers or Entra ID tenants can connect to it privately via their own Private Endpoints.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** Application times out connecting to a Storage Account that has a Private Endpoint configured.
  - **Resolution:** Run `nslookup mystorage.blob.core.windows.net` from the VM. If it returns a public IP (e.g., `20.x.x.x`) instead of a private IP (`10.x.x.x`), the VM is not using the Private DNS Zone. Ensure the VNet is linked to the `privatelink.blob.core.windows.net` Private DNS Zone and that the A record exists.
- **Scenario:** `nslookup` returns the private IP, but the connection still fails.
  - **Resolution:** Check the Network Security Group (NSG) on the subnet where the Private Endpoint NIC resides. Verify the NSG allows inbound traffic from the application VM's subnet on the required port (e.g., 443 for Storage, 1433 for SQL). Also confirm the PaaS service itself has not denied the connection via its own firewall policies.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create Private Endpoint for Azure SQL
az network private-endpoint create \
  --name pe-sql-prod \
  --resource-group rg-prod \
  --vnet-name vnet-core-prod \
  --subnet snet-data \
  --private-connection-resource-id /subscriptions/.../servers/mysqlserver \
  --group-id sqlServer \
  --connection-name conn-sql-pe

# Create Private DNS Zone for SQL
az network private-dns zone create -g rg-prod -n privatelink.database.windows.net

# Link DNS Zone to VNet
az network private-dns link vnet create \
  -g rg-prod \
  -z privatelink.database.windows.net \
  -n dns-link \
  --virtual-network vnet-core-prod \
  --registration-enabled false
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_private_endpoint" "pe" {
  name                = "pe-sql-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.data.id

  private_service_connection {
    name                           = "conn-sql-pe"
    private_connection_resource_id = azurerm_mssql_server.sql.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.sql.id]
  }
}

resource "azurerm_private_dns_zone" "sql" {
  name                = "privatelink.database.windows.net"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "link" {
  name                  = "dns-link"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.sql.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  registration_enabled  = false
}
```

## 17. Production Readiness Checklist
- [ ] Is "Deny Public Network Access" enforced on every target PaaS service?
- [ ] Are Azure Private DNS Zones correctly configured with A records and linked to the VNet?
- [ ] Is Hub-and-Spoke DNS routing configured so on-premises networks can resolve private IPs (via Azure DNS Private Resolver)?
- [ ] Is NSG integration enabled on the Private Endpoint subnet for micro-segmentation?
- [ ] Are Private Endpoint connections using the auto-approval or manual-approval workflow appropriately (manual for cross-tenant)?