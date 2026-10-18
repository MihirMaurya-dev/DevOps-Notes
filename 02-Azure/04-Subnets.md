---
category: Azure-Networking
tags: [azure, subnets, vnet, segmentation, architecture]
type: enterprise-architect-guide
status: active
---

# 🧩 Azure Subnets - Enterprise Architect Guide

## 1. Introduction
A Subnet is a logical subdivision of an Azure Virtual Network (VNet). It allows you to segment the VNet's IP address space into smaller, manageable blocks, enabling you to isolate resources, apply specific security policies, and control traffic routing at a granular level.

## 2. Why This Service Exists
A massive, flat network (e.g., placing Web, App, and Database servers in the same `/16` IP space) is a security nightmare. If a web server is compromised, the attacker has unfettered access to the database. Subnets exist to enforce **micro-segmentation**. By separating tiers into different subnets, you create security boundaries where you can apply firewalls (NSGs) and routing rules to control exactly who can talk to whom.

## 3. Architecture
- **Scope:** Zonal/Regional (Resides entirely within a VNet).
- **Layer:** Layer 3 (Network).
- **Under the Hood:** A subnet is simply a CIDR block carved out of the VNet's CIDR block. Azure's Software Defined Networking (SDN) fabric uses these blocks to apply boundary rules and routing tables.

## 4. Core Components
- **CIDR Prefix:** The IP range of the subnet (e.g., `10.0.1.0/24`).
- **Network Security Group (NSG):** The stateful firewall applied to the subnet to filter traffic.
- **Route Table (UDR):** Custom routing rules attached to the subnet.
- **Service Endpoints:** Enables the subnet to access Azure PaaS services over the Azure backbone.
- **Subnet Delegation:** Yielding control of the subnet to a specific Azure PaaS service (like Azure SQL Managed Instance or App Service) so the service can deploy its instances directly into it.

## 5. Step-by-Step Request Flow
**Scenario:** A packet travels from a Web Subnet to a DB Subnet.
1. The Web VM sends a packet destined for `10.0.2.4` (the DB VM).
2. The packet leaves the Web VM's NIC and hits the **Web Subnet**.
3. Azure evaluates the Route Table on the Web Subnet. It sees the destination is local to the VNet, so it routes it internally.
4. The packet arrives at the boundary of the **DB Subnet**.
5. The **NSG** attached to the DB Subnet evaluates the packet. A rule says "Allow TCP 1433 from 10.0.1.0/24".
6. The packet is allowed through and reaches the DB VM.

## 6. Real-World Production Use Cases & Common Subnet Types

In enterprise deployments, a VNet is typically split into dedicated subnets based on the function of the resources they host. This enables strict network security and routing boundaries.

### Core N-Tier Subnets
1. **Web Subnet (`snet-web`):**
   - **Purpose:** Hosts web servers, front-end UI applications, or Application Gateways.
   - **Security:** This is the only subnet that should typically accept inbound traffic from the internet (or via a WAF/Load Balancer). It is the public-facing entry point of the application.
   - **Routing:** Has routes to talk to the App subnet, but is explicitly denied access directly to the Database subnet.
2. **App Subnet (`snet-app`):**
   - **Purpose:** Hosts the core business logic, middle-tier APIs, or microservices.
   - **Security:** Strictly isolated from the internet. It only accepts inbound traffic from the `snet-web` subnet and is allowed outbound to the DB subnet.
3. **Database Subnet (`snet-db`):**
   - **Purpose:** Hosts database servers (e.g., SQL VMs) or delegated PaaS databases (e.g., PostgreSQL Flexible Server).
   - **Security:** The most locked-down tier. NSGs must explicitly deny all traffic except inbound connections on specific database ports (like 1433 for SQL) originating *only* from the `snet-app` subnet.

### Management & Security Subnets
4. **Management Subnet (`snet-mgmt`):**
   - **Purpose:** Hosts jumpboxes (jump servers), monitoring agents, and IT administration tools.
   - **Security:** Used by administrators to securely SSH/RDP into other servers. Admins connect to the management subnet (often via VPN or Azure Bastion) and from there, jump to servers in the Web, App, or DB subnets.
5. **Private Endpoint Subnet (`snet-pe` or `snet-endpoints`):**
   - **Purpose:** A dedicated subnet for Azure Private Endpoints.
   - **How it works:** When you create a Private Endpoint for a PaaS service (like a Storage Account or Key Vault), Azure places a virtual Network Interface (NIC) with a private IP in this subnet. This allows your VNet to talk to the PaaS service entirely over the Microsoft backbone network, bypassing the public internet.
6. **Key Vault Subnet (often part of `snet-pe`):**
   - **Purpose:** Securely accessing Azure Key Vault.
   - **Implementation:** Usually, Key Vault is accessed by placing its Private Endpoint in the `snet-pe` subnet. Alternatively, you can use **Service Endpoints** on the `snet-app` subnet to allow the App VMs to securely route to Key Vault. It is rare to need a completely dedicated subnet *just* for Key Vault unless there are extremely strict compliance isolation rules.

### Specialized PaaS Subnets
7. **Gateway Subnet (`GatewaySubnet`):** The mandatory subnet to host a VPN or ExpressRoute gateway.
8. **Delegated Subnets:** Subnets given over to PaaS services (e.g., App Service VNet Integration) so web apps can securely query internal VNet databases.

## 7. Architecture & Design Considerations
- **The 5 Reserved IPs:** Azure reserves the first four and the last IP in *every* subnet (e.g., `.0` Network, `.1` Gateway, `.2/.3` DNS, `.255` Broadcast). Never use a `/31` or `/32`. The smallest recommended subnet is `/29` (which gives only 3 usable IPs out of 8 total).
- **Subnet Sizing:** Size subnets based on future growth. Standard workloads usually get a `/24` (251 usable IPs). Gateway subnets require a minimum of `/27`. Azure Bastion requires a minimum of `/26`. Azure Firewall requires a minimum of `/26` in a subnet named exactly `AzureFirewallSubnet`.
- **Non-Overlapping:** Subnet CIDRs must be wholly contained within the VNet CIDR and cannot overlap with each other.

## 8. Microsoft Best Practices
- **Do not mix resources:** Keep different resource types in different subnets. Do not put an App Gateway, an AKS cluster, and standard VMs in the same subnet.
- **Always attach an NSG:** An empty subnet has no security boundaries. Every subnet must have an NSG attached, even if it just contains default rules initially.

## 9. Security Best Practices
- **Zero Trust:** By default, VMs in different subnets within the same VNet can talk to each other. You must write explicit NSG `Deny All` rules at the bottom of your subnet NSGs to enforce a Zero Trust architecture, explicitly allowing only required traffic above it.
- **Private Endpoints:** Place Private Endpoints in a dedicated `snet-endpoints` subnet to easily track and isolate PaaS traffic.

## 10. Monitoring & Observability
- **NSG Flow Logs / VNet Flow Logs:** Enable flow logs on the NSGs attached to your subnets (or use the newer VNet Flow Logs). This sends 5-tuple information (source, destination, port, protocol, allow/deny) to Log Analytics for Traffic Analytics visualization.
- **Route Diagnostics:** Use the "Next Hop" tool in Network Watcher to verify that traffic leaving a subnet is routing correctly.

## 11. Backup & Disaster Recovery
- Subnets are configuration objects. Back them up via Infrastructure as Code (Terraform, Bicep, ARM templates).
- When failing over VMs to a secondary region (via ASR), the secondary VNet must have identically named subnets so the VMs can map to them successfully during the failover.

## 12. Cost Optimization Techniques
- Subnets themselves are **free**.
- **Consolidation:** If you have 50 microservices that share the exact same security profile, put them in one `/23` subnet rather than creating 50 separate `/29` subnets. It reduces management overhead and the number of NSGs you have to maintain.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is a Subnet?
   **A:** A subdivision of a VNet's IP address range used to group resources logically.
2. **Q:** How many IP addresses does Azure reserve in every subnet?
   **A:** 5 IP addresses.

### Intermediate
3. **Q:** What are the 5 reserved IPs used for?
   **A:** Network address, Default gateway, two for Azure DNS mapping, and the Broadcast address.
4. **Q:** Can a single VM have network interfaces in two different subnets?
   **A:** Yes, a VM can have multiple NICs, each attached to a different subnet within the same VNet.
5. **Q:** What is a Gateway Subnet?
   **A:** A dedicated subnet required when deploying a VPN Gateway or ExpressRoute Gateway. You cannot deploy regular VMs here.

### Advanced
6. **Q:** How do you secure traffic between a web subnet and a database subnet?
   **A:** Attach Network Security Groups (NSGs) to the subnets, with rules allowing traffic only on specific ports (e.g., 1433 for SQL) originating exclusively from the web subnet's IP range.
7. **Q:** What is Subnet Delegation?
   **A:** A feature that allows you to designate a specific subnet for a particular Azure PaaS service (e.g., Azure App Service or PostgreSQL Flexible Server), giving the service control over that subnet.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** Unable to deploy Azure Firewall into the VNet.
  - **Resolution:** Azure Firewall requires a specifically named subnet: `AzureFirewallSubnet` with a minimum size of `/26`. Rename your target subnet or create a new one meeting these exact requirements.
- **Scenario:** VMs in a subnet cannot access the internet, but other subnets can.
  - **Resolution:** Check the Route Table (UDR) attached to that specific subnet. A custom route for `0.0.0.0/0` might be pointing to a dead Next Hop (like a misconfigured firewall), or the subnet's NSG is blocking outbound port 443/80.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create a Subnet and attach an existing NSG and Route Table
az network vnet subnet create \
  --resource-group rg-network \
  --vnet-name vnet-prod \
  --name snet-app \
  --address-prefixes 10.0.1.0/24 \
  --network-security-group nsg-app \
  --route-table rt-spoke
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_subnet" "app" {
  name                 = "snet-app"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]

  # Example of Subnet Delegation for App Service VNet Integration
  delegation {
    name = "app-service-delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

# Attach NSG to Subnet
resource "azurerm_subnet_network_security_group_association" "nsg_assoc" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}
```

## 17. Production Readiness Checklist
- [ ] Are all subnets sized appropriately, accounting for the 5 reserved Azure IPs?
- [ ] Are NSGs attached to *every* subnet?
- [ ] Are required PaaS subnets (GatewaySubnet, AzureBastionSubnet, AzureFirewallSubnet) named exactly as Azure requires?
- [ ] Is subnet delegation used appropriately for PaaS VNet integration?
- [ ] Is subnet configuration managed entirely via Infrastructure as Code (Terraform/Bicep)?