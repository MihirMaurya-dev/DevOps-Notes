---
category: Azure-Networking
tags: [azure, networking, vnet, peering, architecture]
type: enterprise-architect-guide
status: active
---

# 🌐 Azure Virtual Network (VNet) - Enterprise Architect Guide

## 1. Introduction
Azure Virtual Network (VNet) is the fundamental building block for your private network in Azure. It enables many types of Azure resources, such as Azure Virtual Machines (VM), to securely communicate with each other, the internet, and on-premises networks. It provides isolation, segmentation, and highly secure routing in the cloud.

## 2. Why This Service Exists
Before VNets, resources in public clouds often shared flat, public-facing network spaces, which was a massive security vulnerability. VNets exist to provide complete network isolation. They give you the equivalent of a traditional on-premises data center network in the cloud, but with the immense scale, redundancy, and dynamic capabilities of Azure's Software Defined Networking (SDN).

## 3. Architecture
- **Scope:** VNet is a **Regional** service. It cannot span regions, but VNets in different regions can be connected via Global VNet Peering.
- **Layer:** It operates primarily at **Layer 3 (Network)** and **Layer 4 (Transport)** of the OSI model.
- **Under the Hood:** It uses Microsoft's proprietary Software Defined Networking (SDN) stack, allowing rapid provisioning without touching physical hardware switches or routers.

## 4. Core Components
- **Address Space (CIDR):** The total IP range assigned to the VNet (e.g., `10.0.0.0/16`).
- **Subnets:** Logical subdivisions of the Address Space (e.g., `10.0.1.0/24`). Used to group resources by tier or security boundary.
- **Network Interfaces (NICs):** The virtual network cards attached to VMs to provide VNet connectivity.
- **Route Tables & UDRs (User Defined Routes):** Define custom paths for traffic flowing inside and outside the VNet.
- **Network Security Groups (NSGs):** Stateful firewalls applied at the subnet or NIC level to filter inbound/outbound traffic.

## 5. Step-by-Step Request Flow
**Scenario:** A VM in a Spoke VNet needs to securely download an update from the internet via a central Hub Firewall.
1. The VM initiates an outbound HTTPS request destined for the internet (`0.0.0.0/0`).
2. The traffic hits the VM's **Subnet**. The subnet has a custom **Route Table (UDR)** attached.
3. The UDR overrides the default internet route, directing `0.0.0.0/0` traffic to a **Next Hop** IP (the private IP of the Azure Firewall in the Hub VNet).
4. The traffic crosses the **VNet Peering** connection securely over Microsoft's backbone into the Hub VNet.
5. The **Azure Firewall** inspects the traffic against its rules.
6. If allowed, the Firewall performs **SNAT (Source Network Address Translation)**, changing the source IP to the Firewall's Public IP, and sends it to the internet.

## 6. Real-World Production Use Cases
1. **N-Tier Application Isolation:** Separating Web, App, and Database tiers into different subnets. The Web subnet is exposed to an App Gateway, the App subnet only accepts traffic from the Web subnet, and the DB subnet only accepts traffic from the App subnet.
2. **Hybrid Cloud Connectivity:** Connecting an on-premises datacenter to a Hub VNet via ExpressRoute or VPN Gateway, extending the corporate network securely into Azure.
3. **PaaS Security (Zero Trust):** Using Private Endpoints to bring PaaS services (like Azure SQL or Storage Accounts) directly into the VNet, completely disabling their public internet access.

## 7. Architecture & Design Considerations
- **IP Overlap:** Never use overlapping CIDR blocks if you plan to peer VNets or connect to on-premises networks. Once deployed, IP conflicts cause routing failures.
- **Azure Reserved IPs:** Azure reserves **5 IP addresses** in every subnet (Network, Default Gateway, 2x DNS, Broadcast). Account for this in sizing (e.g., a `/29` subnet gives 8 IPs, but only 3 are usable).
- **Non-Transitive Peering:** VNet Peering is not transitive by default. If VNet A peers to Hub, and Hub peers to VNet C, VNet A **cannot** reach VNet C directly. You must deploy a routing appliance (like Azure Firewall) in the Hub to route between them.

## 8. Microsoft Best Practices
- **Adopt Hub-and-Spoke Topology:** Use a central Hub VNet for shared services (Firewall, VPN, DNS) and separate Spoke VNets for individual applications/environments.
- **Plan for Growth:** Always leave extra, unallocated IP space in your VNet design. Resizing VNets or subnets when resources are running is difficult.
- **Avoid Public IPs on VMs:** Never assign Public IPs directly to VMs unless absolutely necessary. Route outbound traffic through Azure NAT Gateway (for performance) or Azure Firewall (for security).

## 9. Security Best Practices
- **Apply NSGs Everywhere:** Apply Network Security Groups to *every* subnet to enforce micro-segmentation.
- **Use ASGs (Application Security Groups):** Group VMs logically (e.g., "WebServers") rather than hardcoding IP addresses into NSG rules.
- **Azure Bastion:** Use Azure Bastion for secure RDP/SSH access instead of opening port 3389 or 22 to the internet.
- **DDoS Protection:** Enable Azure DDoS Protection Standard for mission-critical VNets that have public-facing endpoints.

## 10. Monitoring & Observability
- **VNet Flow Logs:** The recommended, newer method for capturing 5-tuple traffic data scoped to an entire VNet. Enable these to send logs to a Log Analytics Workspace and use **Traffic Analytics** to visualize traffic patterns and identify malicious IPs. (NSG Flow Logs are the legacy per-NSG equivalent; prefer VNet Flow Logs for new deployments.)
- **Network Watcher:** Use this suite for packet capture, next-hop analysis, and connection troubleshooting.
- **Metrics:** Monitor VNet Peering bandwidth, VPN tunnel status, and dropped packets via Azure Monitor Metrics.

## 11. Backup & Disaster Recovery
- **State Backup:** VNets do not store data, but their configuration state must be backed up. The best practice is to define the VNet in **Infrastructure as Code (Terraform/Bicep)** so it can be recreated instantly.
- **Disaster Recovery (DR):** For business continuity, create a duplicate VNet structure in your paired secondary region. Use **Azure Site Recovery (ASR)** to replicate VMs into this secondary VNet so they can spin up with the same private IPs during a failover.

## 12. Cost Optimization Techniques
- **VNet Creation is Free:** There is no charge to create a VNet itself.
- **Peering Costs:** VNet Peering incurs ingress/egress charges. If two microservices are highly chatty (transferring Terabytes of data), place them in the same VNet to avoid peering costs.
- **Global vs Regional Peering:** Global VNet Peering (across regions) is significantly more expensive than Regional Peering. Keep heavy traffic regional.
- **NAT Gateway vs Load Balancer:** Use NAT Gateway to avoid the per-VM Public IP charges and prevent costly port exhaustion issues.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is an Azure Virtual Network (VNet)?
   **A:** A fundamental building block for your private network in Azure, providing isolation and segmentation.
2. **Q:** What is VNet Peering?
   **A:** A mechanism to connect two VNets securely via Microsoft's private backbone.

### Intermediate
3. **Q:** Is VNet Peering transitive?
   **A:** No. If VNet A is peered to B, and B is peered to C, A cannot talk to C directly. You need a peering between A and C, or a routing appliance in B.
4. **Q:** What is Global VNet Peering?
   **A:** Connecting VNets that reside in different Azure regions.
5. **Q:** Can you peer two VNets with overlapping IP address spaces?
   **A:** No, peering requires non-overlapping CIDR blocks.

### Advanced
6. **Q:** Explain the Hub-and-Spoke network topology.
   **A:** A central Hub VNet hosts shared services (firewall, VPN, DNS), and Spoke VNets host specific workloads. Spokes peer to the Hub, preventing the need for a full mesh of peerings.
7. **Q:** How do you force all Spoke traffic to exit to the internet via a firewall in the Hub?
   **A:** By creating a User-Defined Route (UDR) on the Spoke subnets, setting `0.0.0.0/0` (internet bound traffic) to have a Next Hop of the firewall's private IP in the Hub.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** A VM in Spoke A cannot reach a VM in Spoke B.
  - **Resolution:** Because VNet Peering is non-transitive, ensure that: (1) A UDR on Spoke A directs traffic destined for Spoke B to the Hub Firewall. (2) The Hub Firewall has a Network Rule allowing traffic from Spoke A to Spoke B. (3) The Hub's peering connections have "Allow forwarded traffic" enabled.
- **Scenario:** Cannot create a VNet Peering connection.
  - **Resolution:** Verify the CIDR blocks of the two VNets. If they overlap (e.g., both use `10.0.0.0/16`), Azure will block the peering.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create a Resource Group
az group create --name rg-networking-prod --location eastus

# Create a VNet and default Subnet
az network vnet create \
  --name vnet-core-prod \
  --resource-group rg-networking-prod \
  --address-prefix 10.0.0.0/16 \
  --subnet-name snet-web \
  --subnet-prefix 10.0.1.0/24
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-core-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]

  tags = {
    Environment = "Production"
    Tier        = "Hub"
  }
}

resource "azurerm_subnet" "web" {
  name                 = "snet-web"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}
```

## 17. Production Readiness Checklist
- [ ] Are VNet CIDR blocks verified against on-premises networks to ensure zero overlap?
- [ ] Is the Hub-and-Spoke model implemented instead of a flat network?
- [ ] Are NSGs applied to all subnets?
- [ ] Are VNet Flow Logs enabled and shipping to a Log Analytics Workspace with Traffic Analytics?
- [ ] Are there zero Public IPs directly attached to application VMs?
- [ ] Is Azure DDoS Protection Standard enabled on VNets with public-facing endpoints?
- [ ] Is the entire network configuration managed via Terraform/Bicep?