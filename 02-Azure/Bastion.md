---
category: Azure-Security
tags: [azure, bastion, security, rdp, ssh, architecture]
type: enterprise-architect-guide
status: active
---

# 🛡️ Azure Bastion - Enterprise Architect Guide

## 1. Introduction
Azure Bastion is a fully managed Platform as a Service (PaaS) that provides secure and seamless Remote Desktop Protocol (RDP) and Secure Shell (SSH) connectivity to your virtual machines directly from the Azure portal over TLS (HTTPS port 443). No public IP address is required on the target VM.

## 2. Why This Service Exists
Traditionally, administrators accessed cloud VMs by opening port 3389 (RDP) or 22 (SSH) to the internet, or by setting up a "Jump Box" (a dedicated VM with a public IP). These are massive security risks and prime targets for brute-force attacks and internet port scanners. Azure Bastion eliminates the need for public IP addresses on your VMs, preventing internet exposure while still allowing secure, browser-based administrative access.

## 3. Architecture
- **Scope:** Regional (Deployed into a specific VNet).
- **Layer:** PaaS Security Appliance (operates at Layer 7).
- **Under the Hood:** Bastion is deployed into a dedicated subnet (`AzureBastionSubnet`). It acts as a reverse proxy gateway. Users connect to Bastion via port 443 (HTTPS), and Bastion translates that connection to RDP (port 3389) or SSH (port 22) internally using the private IPs of the target VMs. The RDP/SSH ports are never exposed to the internet.

## 4. Core Components
- **Bastion Host:** The managed appliance instance deployed in the `AzureBastionSubnet`.
- **AzureBastionSubnet:** A dedicated, tightly controlled subnet (must be named exactly `AzureBastionSubnet` and be at least `/26`) where the service is deployed.
- **Target VMs:** The VMs you wish to connect to — they do not require public IPs.
- **Standard SKU vs Basic SKU:**
  - **Basic SKU:** Browser-only RDP/SSH access within a single VNet. No VNet Peering support, no native client, no session recording.
  - **Standard SKU:** Supports scaling (multiple instances), native client connections (via Azure CLI), VNet Peering for Hub-and-Spoke, IP-based connection, and session recording.

## 5. Step-by-Step Request Flow
**Scenario:** A cloud admin needs to configure IIS on a production web server.
1. The admin logs into the Azure Portal (authenticated via Microsoft Entra ID and MFA).
2. The admin navigates to the target VM and clicks "Connect → Bastion".
3. An HTML5 TLS (HTTPS/443) session is established between the admin's browser and the Azure Bastion public endpoint.
4. Azure Bastion initiates an internal RDP (port 3389) connection to the target VM's **private IP**.
5. The RDP graphical interface is streamed back to the admin entirely within their web browser — no RDP client software required.

## 6. Real-World Production Use Cases
1. **Zero-Trust Admin Access:** Providing secure access to database VMs (SQL IaaS) without deploying VPNs, ExpressRoute, or opening public ports to the internet.
2. **Third-Party Vendor Access:** Granting external contractors temporary access to a specific VM via the portal without giving them VPN access to the entire corporate network.
3. **Hub-and-Spoke Administration:** Deploying one Standard Bastion in the Hub VNet to centrally manage VMs across all peered Spoke VNets — dramatically reducing cost and complexity.

## 7. Architecture & Design Considerations
- **Subnet Naming and Sizing:** The subnet MUST be named exactly `AzureBastionSubnet` (case-sensitive). The minimum size is `/26` (64 addresses), which provides enough IP space for Bastion's internal scaling instances.
- **Hub-and-Spoke:** If using VNet Peering, you MUST use the **Standard SKU**. Deploy ONE Bastion host in the Hub, and it can access VMs in all peered Spoke VNets. This avoids the massive cost of deploying a Bastion instance in every Spoke VNet.
- **Native Client Support:** If engineers prefer using Putty, MSTSC, or the OpenSSH client instead of the browser, the Standard SKU supports this via the `az network bastion tunnel` or `az network bastion rdp` commands.

## 8. Microsoft Best Practices
- **Do not apply NSGs to `AzureBastionSubnet` arbitrarily:** Bastion requires specific ingress/egress rules to function (e.g., inbound 443 from internet, inbound 443 from GatewayManager, outbound 3389/22 to VirtualNetwork). Always follow Microsoft's documented NSG rules for Bastion.
- **Leverage Microsoft Entra ID Conditional Access:** Secure the Azure Portal with strict Conditional Access policies (e.g., require MFA, compliant devices, and specific named locations) to ensure the entry point to Bastion is impenetrable.

## 9. Security Best Practices
- **Remove Public IPs from VMs:** Once Bastion is deployed, audit all VMs in the VNet and remove their Public IP addresses. Close all inbound 3389/22 rules from the internet in all VM subnet NSGs.
- **JIT Integration:** Bastion integrates with Microsoft Defender for Cloud's Just-In-Time (JIT) access. Require admins to submit a JIT request before Bastion can connect to the VM, providing a time-bound access window.
- **Session Auditing (Standard SKU):** Standard SKU supports session recording to Azure Storage, allowing security teams to play back video recordings of exactly what the admin did during an RDP/SSH session for audit and compliance.

## 10. Monitoring & Observability
- **Diagnostic Settings:** Route `BastionAuditLogs` to a Log Analytics Workspace. This logs who connected, to which VM (by private IP), and when the session started and ended.
- **Metrics:** Monitor `Total Session Count` and `CPU/Memory` utilization of the Bastion host to determine if you need to scale out the number of instances (Standard SKU).

## 11. Backup & Disaster Recovery
- Bastion is stateless — it does not store session data or configuration beyond what is in the ARM resource definition.
- In a Disaster Recovery scenario, deploy a new Bastion instance in the DR VNet via Infrastructure as Code (Terraform/Bicep). Because it is stateless, it recreates instantly.

## 12. Cost Optimization Techniques
- Azure Bastion has a fixed hourly cost per host PLUS outbound data transfer charges.
- **Avoid Bastion Sprawl:** Deploying a Basic or Standard Bastion in every individual VNet is extremely expensive. Centralize it in a Hub VNet (Standard SKU) to drastically reduce costs across the entire organization.
- **Dev/Test Environments:** If you only need occasional access for a small dev environment, deploy it on-demand, use it, and delete it via automation script when done — saving the hourly fee during idle hours.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Bastion?
   **A:** A PaaS service providing secure browser-based RDP and SSH access to Azure VMs directly from the Azure portal, without requiring a public IP on the VM.
2. **Q:** Does a VM need a public IP to use Azure Bastion?
   **A:** No, Bastion connects to the VM using its private IP address only.

### Intermediate
3. **Q:** What port does the user connect to when using Azure Bastion?
   **A:** The user connects to Bastion over Port 443 (HTTPS) in their browser. Bastion then connects internally to the VM on port 3389 (RDP) or 22 (SSH).
4. **Q:** What is the `AzureBastionSubnet`?
   **A:** A dedicated subnet (exact name required, minimum /26) required for deploying the Azure Bastion host. No other resources may reside in this subnet.
5. **Q:** Can one Bastion host serve multiple VNets?
   **A:** Yes, with the Standard SKU. If the VNets are peered (Hub-and-Spoke), a Bastion in the Hub can connect to VMs in all the Spoke VNets.

### Advanced
6. **Q:** How does Bastion prevent brute-force attacks compared to a traditional Jump Box?
   **A:** It completely hides RDP/SSH ports from the internet. A jump box with an open port 3389/22 is discoverable by internet scanners. Bastion only exposes standard HTTPS (443), and the RDP/SSH tunnel is established internally between Bastion and the VM on the private network.
7. **Q:** Does Azure Bastion support native client connections (like Putty or MSTSC) instead of just the browser?
   **A:** Yes, with the Standard SKU. You can use native RDP/SSH clients via the Azure CLI commands `az network bastion rdp` and `az network bastion ssh`, or via tunnel mode (`az network bastion tunnel`).

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** The deployment of Azure Bastion fails immediately.
  - **Resolution:** Verify two things: (1) The subnet name is EXACTLY `AzureBastionSubnet` (case-sensitive). (2) The subnet is at least a `/26`. If either condition is wrong, Azure will reject the deployment.
- **Scenario:** The portal opens the Bastion connection tab, but the screen stays black or the connection fails after a moment.
  - **Resolution:** Check the NSG on the **target VM's subnet** — it must allow inbound TCP traffic on port 3389 (for RDP) or 22 (for SSH) sourced from the `AzureBastionSubnet` IP range. Also check the Guest OS firewall inside the VM (Windows Defender Firewall or iptables) to ensure it allows connections on those ports from the Bastion subnet.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create the required AzureBastionSubnet
az network vnet subnet create \
  -g rg-hub-prod \
  --vnet-name vnet-hub-prod \
  -n AzureBastionSubnet \
  --address-prefixes 10.0.254.0/26

# Create Public IP for Bastion (Standard SKU required)
az network public-ip create -g rg-hub-prod -n pip-bastion --sku Standard --zone 1 2 3

# Create Bastion Host (Standard SKU for Hub-and-Spoke VNet Peering support)
az network bastion create \
  --name bastion-hub-prod \
  --public-ip-address pip-bastion \
  --resource-group rg-hub-prod \
  --vnet-name vnet-hub-prod \
  --sku Standard
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_subnet" "bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.254.0/26"]
}

resource "azurerm_public_ip" "bastion_pip" {
  name                = "pip-bastion"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = ["1", "2", "3"]
}

resource "azurerm_bastion_host" "bastion" {
  name                = "bastion-hub-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.bastion.id
    public_ip_address_id = azurerm_public_ip.bastion_pip.id
  }
}
```

## 17. Production Readiness Checklist
- [ ] Is the Hub-and-Spoke topology using a single centralized Standard SKU Bastion (not one per VNet)?
- [ ] Are all Public IPs detached from VMs managed by Bastion?
- [ ] Do VM subnet NSGs allow inbound 3389/22 from `AzureBastionSubnet` only (and deny it from the internet)?
- [ ] Is the Bastion Public IP zone-redundant (Standard SKU with zones 1, 2, 3)?
- [ ] Are Bastion Diagnostic Logs (`BastionAuditLogs`) enabled and shipping to Log Analytics?
- [ ] Is session recording evaluated and enabled for high-security environments (Standard SKU)?