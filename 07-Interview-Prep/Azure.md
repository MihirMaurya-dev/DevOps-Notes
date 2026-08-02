---
tags: [interview, prep, azure, questions]
source: devopsinsiders/batch-18
updated: 2026-07-26
---

# Azure Interview Questions

A collection of comprehensive interview questions regarding Azure core concepts and administration, ranging from basics to scenario-based.

---

## Basics

### Q1: What is Microsoft Azure and how does it differ from on-premises datacenters?
**A:** Azure is Microsoft's public cloud computing platform providing services like IaaS, PaaS, and SaaS over the internet. Unlike on-premises datacenters where you manage physical hardware, networking, and power, Azure operates on a pay-as-you-go model. This allows organizations to scale rapidly, reduce capital expenditure (CapEx) in favor of operational expenditure (OpEx), and shift the responsibility of physical infrastructure maintenance to Microsoft.

### Q2: What are the main differences between IaaS, PaaS, and SaaS?
**A:** 
- **IaaS (Infrastructure as a Service):** You rent IT infrastructure like VMs and networks. You manage the OS, runtime, and application (e.g., Azure Virtual Machines).
- **PaaS (Platform as a Service):** Provides a managed hosting environment. The cloud provider manages the OS and runtime, allowing developers to focus solely on deploying code (e.g., Azure App Service, Azure SQL Database).
- **SaaS (Software as a Service):** Fully managed applications hosted by the provider and accessed via the internet (e.g., Microsoft 365, GitHub).

### Q3: What is a Resource Group in Azure?
**A:** A Resource Group is a logical container that holds related resources for an Azure solution. It helps in organizing, managing, and monitoring resources as a single entity based on lifecycle or application. For example, you can deploy, update, or delete all resources for a web app in a single coordinated operation. Resources in a resource group can be located in different regions.

### Q4: Can an Azure resource exist in multiple Resource Groups?
**A:** No. An individual resource can only reside in exactly one Resource Group at a time. However, it can communicate and be linked with resources located in other Resource Groups. You can also move resources between Resource Groups if needed.

### Q5: What is the difference between Authentication and Authorization in Azure?
**A:** 
- **Authentication** proves who you are (Identity). In Azure, this is handled by Microsoft Entra ID (formerly Azure AD) which checks your credentials and MFA. It acts as the "key to the front door."
- **Authorization** determines what you are allowed to do once authenticated. In Azure, this is handled by Azure Role-Based Access Control (RBAC), which verifies if your account has roles like "Contributor" or "Reader" on a specific resource.

### Q6: How does Azure manage geographical redundancy and latency?
**A:** Azure organizes its datacenters into Regions (e.g., East US, West Europe). Each region is paired with another region within the same geography (Regional Pairs) for disaster recovery. Furthermore, regions have Availability Zones, which are physically separate datacenters with independent power, cooling, and networking to provide high availability within the region.

### Q7: What are Azure Subscriptions and Management Groups?
**A:** 
- An **Azure Subscription** is a logical container used to provision resources and serves as a boundary for billing and access control.
- **Management Groups** sit above subscriptions and allow you to manage access, policy, and compliance across multiple subscriptions. This hierarchical structure is essential for enterprise governance.

### Q8: What is the difference between Azure Application Gateway and Azure Load Balancer?
**A:**
| Feature | Azure Load Balancer | Application Gateway |
|---------|-------------------|-------------------|
| OSI Layer | Layer 4 (TCP/UDP) | Layer 7 (HTTP/HTTPS) |
| SSL Termination | No | Yes |
| WAF Support | No | Yes |
| URL Path Routing | No | Yes (`/api/*` → backend1) |
| Cost | Lower | Higher |
Use **Load Balancer** for non-HTTP traffic or high-throughput, low-latency L4 needs. Use **Application Gateway** for web apps needing WAF, SSL offload, or content-based routing.

### Q9: What is an NSG (Network Security Group) and how does it work?
**A:** An NSG is a virtual stateful firewall applied to a **Subnet** or a **NIC**. It contains ordered **inbound** and **outbound** security rules. Each rule specifies: source/destination IP (or ASG), port, protocol, and allow/deny action. Rules are evaluated in priority order (lower number = higher priority). Azure processes the lowest-priority matching rule and stops. NSGs are free and are the primary tool for micro-segmentation in Azure.

### Q10: What are the key components of Azure architecture you frequently work with?
**A:** Virtual Machines, AKS, App Services, VNets, Load Balancers, Application Gateway, Azure Functions, Key Vault, Storage Accounts, Azure SQL, Monitor, Log Analytics, and Azure DevOps for CI/CD pipelines.

### Q11: How do you ensure high availability and disaster recovery in Azure?
**A:**
- Use Availability Zones & Availability Sets
- Geo-redundant storage (GRS)
- Azure SQL active geo-replication
- Traffic Manager for global failover
- Automated backups & runbooks

---

## Intermediate

### Q12: Explain the difference between LRS, ZRS, and GRS in Azure Storage.
**A:**
- **LRS (Locally Redundant Storage):** Synchronously copies data 3 times within a single physical location. Protects against hardware failure but not a datacenter outage.
- **ZRS (Zone-Redundant Storage):** Synchronously copies data across 3 separate Availability Zones within a region. Protects against a complete datacenter failure.
- **GRS (Geo-Redundant Storage):** Copies data synchronously 3 times via LRS, then asynchronously copies it to a paired secondary region hundreds of miles away. It protects against massive regional disasters.

### Q13: Explain Azure Availability Zones vs Availability Sets.
**A:**
- **Availability Sets:** Protect VMs against rack-level hardware failure or planned maintenance by distributing them across different fault and update domains within a single datacenter. Offers a 99.95% SLA.
- **Availability Zones:** Protect VMs against entire datacenter failures by placing them in separate physical datacenters within a region. This is the modern standard, offering a 99.99% SLA.

### Q14: What is the difference between Azure Firewall and NSG?
**A:**
- **NSG (Network Security Group):** Operates at Layer 4 (TCP/UDP) and is applied to a NIC or Subnet for micro-segmentation. It is free and lacks advanced inspection.
- **Azure Firewall:** A managed, centralized service operating at Layer 4 and Layer 7. It provides features like FQDN filtering, threat intelligence, and centralized north-south traffic control. It incurs hourly and data processing costs.

### Q15: What is Azure Policy and how is it different from RBAC?
**A:**
- **RBAC:** Controls *who* can perform *what actions* (e.g., "User X can restart VM Y"). It focuses on identity permissions.
- **Azure Policy:** Controls *what resources* can exist and their properties (e.g., "All storage accounts must enforce HTTPS"). It focuses on resource compliance and governance, capable of denying non-compliant resource creation or automatically remediating them.

### Q16: How does Azure Front Door differ from Azure Application Gateway?
**A:**
- **Application Gateway:** A regional, Layer 7 load balancer designed for web traffic within a single region. It provides URL path routing and a regional WAF.
- **Front Door:** A global, Layer 7 load balancer and CDN. It routes client traffic to the nearest healthy region, offering global failover, caching, and edge-level WAF protection against DDoS attacks before traffic enters your VNet.

### Q17: What is an Azure Managed Identity?
**A:** A Managed Identity is a feature of Entra ID that gives Azure services (like VMs, App Services) an automatically managed identity. It eliminates the need for developers to manage credentials or connection strings. For example, a VM can securely authenticate to an Azure Key Vault using its Managed Identity, verified entirely by Azure via RBAC.

### Q18: System-Assigned vs User-Assigned Managed Identity.
**A:**
- **System-Assigned:** Tied directly to a single resource's lifecycle. If the resource is deleted, the identity is automatically deleted.
- **User-Assigned:** A standalone Azure resource that can be assigned to one or multiple resources. It persists independently of the resources using it, making it ideal for shared access scenarios.

### Q19: What is Azure ExpressRoute?
**A:** Azure ExpressRoute provides a private, dedicated connection between your on-premises infrastructure and Azure datacenters via a connectivity provider. It does not go over the public internet. This ensures higher security, more reliability, consistent latencies, and often higher speeds than typical VPN connections.

### Q20: If a VM goes down unexpectedly, what is your recovery process?
**A:**
1. **Identify the failure type**: Compute issue (VM crashed) vs disk issue (OS disk corrupted).
2. If disks are healthy: Restart the VM via Azure Portal/CLI.
3. If the OS is corrupted: Attach the OS disk to a recovery VM, fix the issue, re-attach.
4. If unrecoverable: Restore from **Azure Backup / Recovery Services Vault** using the latest restore point.
5. If no backup: Redeploy from Terraform IaC and restore data from DB backups.
Prevention: Enable automated backup policies, use VMSS for stateless workloads.

### Q21: Two VNets have overlapping IP ranges. Can they communicate via VNet Peering?
**A:** **No.** VNet Peering requires non-overlapping IP address spaces. If two VNets share the same CIDR (e.g., both use `10.0.0.0/16`), you cannot peer them. Options to work around this:
- **Azure Private Link**: Expose specific services from one VNet to another without peering.
- **NAT Gateway with custom routes** to translate addresses.
- **Redesign**: Assign non-overlapping CIDRs from the start using an enterprise IPAM strategy.

### Q22: What is a SAS Token, and when would you use it over RBAC?
**A:** A **Shared Access Signature (SAS)** token is a time-limited, signed URL that grants specific permissions (read/write/delete) to a specific Storage Account resource (blob, queue, container) **without requiring Azure AD authentication**.

Use SAS when:
- A **third party** or external system needs temporary access and cannot be assigned an Azure identity.
- You need **scoped, time-bound** access to a specific blob (e.g., share a download link for 24 hours).

Prefer **RBAC** for internal services and teams — it's auditable, identity-based, and doesn't require managing token expiry manually.

### Q23: What is Terraform Drift? How do you detect and handle it before running `terraform plan`?
**A:** Drift = the real-world Azure resource differs from what's in the Terraform state (due to manual Portal changes). Detection:
- `terraform plan` automatically performs a **refresh** of real-world state and shows drift as proposed changes.
- `terraform refresh` (deprecated) or `terraform plan -refresh-only` to see only drift without changes.

Handling drift:
- If the manual change is **correct** → update `.tf` code to match, so `plan` shows no changes.
- If the manual change is **wrong** → run `terraform apply` to revert to the defined state.
- Use `lifecycle { ignore_changes = [...] }` for attributes intentionally managed outside Terraform.

---

## Advanced

### Q24: When would you use Private Endpoints vs Service Endpoints?
**A:**
- **Service Endpoints:** Optimize routing to Azure PaaS services over the Azure backbone network. However, the service still retains a public IP, though access is restricted to your VNet.
- **Private Endpoints:** Use Azure Private Link to assign a private IP from your VNet to a PaaS service (like SQL or Storage). This completely removes the public IP footprint of the service, making it accessible only internally. Essential for strict compliance (e.g., PCI-DSS).

### Q25: Explain the AKS Networking Models: kubenet vs Azure CNI.
**A:**
- **kubenet:** Pods receive IPs from a logically distinct overlay network and are NAT'd behind the node's IP to access the VNet. It is highly IP efficient but integrates less cleanly with VNet resources.
- **Azure CNI:** Every Pod gets a real IP from the VNet subnet, making them first-class citizens on the network. It requires careful subnet sizing since it consumes many IPs.
*Note:* Azure CNI Overlay is a modern hybrid that offers the IP efficiency of kubenet with the performance and feature set of Azure CNI.

### Q26: What are Entra ID Conditional Access and Privileged Identity Management (PIM)?
**A:**
- **Conditional Access:** An Entra ID policy engine evaluating signals (user, location, device compliance, risk score) to enforce access controls like requiring MFA.
- **PIM:** Provides Just-In-Time (JIT) role activation. Users are eligible for admin roles but must actively request them for a limited time (e.g., 2 hours), usually requiring justification and MFA. This drastically reduces the attack surface of standing privileges.

### Q27: How do you achieve cross-region VNet connectivity?
**A:** You use Global VNet Peering. It securely connects VNets in different Azure regions over the Microsoft backbone infrastructure. Once peered, resources in either VNet can communicate using private IP addresses as if they were in the same network, without requiring VPN gateways.

### Q28: Describe Azure Key Vault and how it secures secrets.
**A:** Azure Key Vault is a centralized cloud service for securely storing and accessing secrets, encryption keys, and certificates. Access is strictly controlled via Entra ID RBAC or Access Policies. It supports network restrictions (Firewalls/Private Endpoints) and ensures that sensitive strings (like DB connection strings) are never hardcoded in configuration files or code.

### Q29: What is the difference between Azure Monitor, Log Analytics, and Application Insights?
**A:**
- **Azure Monitor:** The overarching service for collecting, analyzing, and acting on telemetry data from cloud and on-premises environments.
- **Log Analytics:** A workspace within Azure Monitor where logs are aggregated and queried using Kusto Query Language (KQL).
- **Application Insights:** A feature of Azure Monitor focused on Application Performance Management (APM). It instruments your code to provide deep insights into application errors, performance bottlenecks, and usage.

### Q30: What are Azure Virtual Machine Scale Sets (VMSS)?
**A:** VMSS allow you to create and manage a group of load-balanced VMs. The number of VM instances can automatically increase or decrease in response to demand or a defined schedule. This provides high availability and fault tolerance for applications, natively integrating with Azure Load Balancer or Application Gateway.

### Q31: How does Azure Key Vault secure secrets and how do you integrate it?
**A:** Key Vault stores secrets, keys, and certificates. Access is controlled via:
1. **RBAC** (recommended): Assign roles like `Key Vault Secrets User` to identities.
2. **Access Policies** (legacy): Grant get/list/set permissions per identity.

Integration in Terraform:
```hcl
data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.main.id
}
# Use it in a resource:
# password = data.azurerm_key_vault_secret.db_password.value
```
In CI/CD pipelines, reference via Variable Group linked to Key Vault.

### Q32: Explain Active-Passive vs Active-Active Disaster Recovery in Azure.
**A:**
- **Active-Passive**: Primary region serves all traffic. Secondary region is a warm standby (pre-provisioned infra, synced data). On failure, DNS or Traffic Manager points to secondary. **Lower cost, higher RTO** (time to fail over).
- **Active-Active**: Both regions serve traffic simultaneously behind Azure Front Door or Traffic Manager. Requires data synchronization (Cosmos DB global replication, SQL geo-replication). **Zero RTO, higher cost** — both regions must be fully sized.

---

## Scenario-Based

### Q33: Scenario: An Azure Web App cannot connect to an Azure SQL Database. How do you troubleshoot?
**A:** 
First, I would verify the network configuration. If the Web App uses VNet Integration, I'd check the NSGs on the delegated subnet and the SQL database firewall rules. Next, I would confirm if Private Endpoints are in use and verify that DNS resolution within the VNet correctly resolves the SQL server's Private IP. Finally, I'd check authentication, ensuring the Web App's Managed Identity or connection string is correct and has the necessary RBAC/SQL permissions.

### Q34: Scenario: Your organization requires that developers cannot spin up expensive VMs (like GPU instances). How do you enforce this?
**A:** 
I would implement an **Azure Policy** and assign it at the Management Group or Subscription level. The policy would be defined to "Allowed virtual machine size SKUs" and list only the cost-effective VM sizes (like the B-series or standard D-series). Any attempt to deploy a non-compliant VM size would be blocked by the `Deny` effect, ensuring proactive cost control without removing the developers' Contributor access.

### Q35: Scenario: You need to migrate an on-premises web application to Azure with minimal downtime. What approach do you take?
**A:** 
For the database, I would use Azure Database Migration Service (DMS) to continuously replicate data to Azure SQL, ensuring the data is synced. For the application layer, I would use Azure Migrate or Azure Site Recovery to lift-and-shift the VMs, or containerize the application and deploy it to AKS or App Service. On cutover day, I'd update DNS records (or Azure Front Door routing) to point to the new Azure environment and perform a final data sync.

### Q36: Scenario: How would you design a highly available, secure 3-tier architecture in Azure?
**A:** 
I would deploy resources across multiple Availability Zones. 
- **Web Tier:** Placed in a subnet behind an Application Gateway (with WAF) to distribute incoming HTTP/HTTPS traffic.
- **App Tier:** VMs in a Virtual Machine Scale Set or AKS nodes in a separate subnet.
- **Data Tier:** Azure SQL Database with Zone-Redundant HA and a Private Endpoint. 
I would secure the traffic between tiers using NSGs, allowing the App tier to only accept traffic from the Web tier, and the Data tier to only accept traffic from the App tier.

### Q37: Scenario: An AKS pod cannot reach the internet to download updates. What could be the issue?
**A:** 
This is likely a networking or egress configuration issue. If the cluster uses a custom VNet, I would check if a Route Table is attached to the AKS subnet forcing traffic (0.0.0.0/0) to a firewall or NVA. If so, I'd verify the firewall rules allow outbound traffic on port 443. I would also check if the cluster was created with `outboundType: userDefinedRouting` and verify the NAT Gateway or standard Load Balancer configurations.

### Q38: Scenario: You need to grant a contractor temporary administrative access to an Azure subscription. How do you do it securely?
**A:** 
I would use Entra ID Privileged Identity Management (PIM). I would invite the contractor as an external guest user and assign them the specific administrative role as "Eligible" with a strict expiration date. When they need to perform a task, they must activate the role via PIM, provide a justification, and pass an MFA prompt. Their access will automatically expire after a few hours, leaving zero standing privileges.

### Q39: Scenario: How would you troubleshoot if a user cannot RDP/SSH to an Azure VM?
**A:**
1. **NSG Check**: `IP Flow Verify` (Network Watcher) to see if the NSG is blocking port 3389/22.
2. **VM Status**: Ensure the VM is Running, not deallocated.
3. **Public IP**: Confirm the VM or Bastion has a valid public IP (or use Bastion for private VMs).
4. **JIT Access**: If JIT is enabled, request access first.
5. **OS Firewall**: Use Azure Serial Console to check if Windows Firewall or iptables is blocking.
6. **DNS/IP**: Ensure you are connecting to the correct IP address.

### Q40: Scenario: How do you provide outbound internet access to private VMs during migration without assigning Public IPs?
**A:** Use **Azure NAT Gateway** attached to the subnet. VMs keep their private IPs, and outbound traffic is translated via the NAT Gateway's public IP. Alternatively, in a Hub-Spoke model, route all traffic through **Azure Firewall** in the Hub with FQDN allow rules for the specific software download URLs. Remove or tighten the rule after migration is complete.

### Q41: Scenario: How does a backend communicate with a database securely in Azure?
**A:**
1. **Private Endpoint on the DB**: The database (Azure SQL, Cosmos DB) is assigned a private IP in the VNet — no public exposure.
2. **Managed Identity**: The backend app (App Service, VM) uses its Managed Identity to authenticate to the DB without any connection string passwords.
3. **NSG rules**: Only allow traffic from the backend subnet IP range to the DB subnet on the specific port (e.g., 1433).
4. **SSL/TLS enforced**: Enable `Require Secure Transport` on the DB server.
