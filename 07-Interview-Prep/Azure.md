---
tags: [interview, prep, azure, questions]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Azure Interview Questions

A collection of common interview questions regarding Azure core concepts and administration.

---

## Q1: What is the difference between Authentication and Authorization in Azure?
**A:** 
- **Authentication** is the process of proving who you are (Identity). In Azure, this is handled by Microsoft Entra ID (formerly Azure AD) checking your username, password, and MFA. It's the "key to the front door."
- **Authorization** is the process of determining what you are allowed to do once you are inside. This is handled by Azure Role-Based Access Control (RBAC), which checks if your account has the "Contributor" or "Reader" role on a specific resource.

---

## Q2: How is an Entra ID Global Administrator different from an Azure Subscription Owner?
**A:** 
- A **Global Administrator** has full control over the Entra ID tenant (managing users, groups, and tenant-level policies). However, they do *not* automatically have access to any Azure resources (like VMs or VNets).
- A **Subscription Owner** has full control over all Azure resources within a specific subscription and can assign Azure roles to other users for those resources. They cannot manage Entra ID users unless they also have a role like User Administrator in Entra ID.

---

## Q3: What is a Managed Identity and why should we use it?
**A:** A Managed Identity is a feature of Entra ID that provides Azure services (like a VM or Web App) with an automatically managed identity. You should use it to eliminate the need for developers to manage credentials (like connection strings or API keys). Instead of hardcoding a password to connect a VM to a Key Vault, you grant the VM's Managed Identity RBAC access to the Key Vault.

> [!tip] System-Assigned vs User-Assigned
> **System-Assigned**: tied to a single resource lifecycle — deleted when the resource is deleted.  
> **User-Assigned**: standalone identity that can be shared across multiple resources and persists independently.

---

## Q4: Can a resource exist in multiple Resource Groups?
**A:** No. A resource can only reside in exactly one Resource Group at a time. However, it can communicate with resources in other Resource Groups.

---

## Q5: Explain the difference between LRS, ZRS, and GRS in Azure Storage.
**A:**
- **LRS (Locally Redundant Storage):** Synchronously copies data 3 times within a single physical location (server rack). Protects against hardware failure but not a datacenter going down.
- **ZRS (Zone-Redundant Storage):** Synchronously copies data across 3 separate Availability Zones within a region. Protects against a datacenter failure.
- **GRS (Geo-Redundant Storage):** Copies data synchronously 3 times within a single location using LRS, then asynchronously copies it to a secondary region hundreds of miles away. Protects against regional disasters.

---

## Q6: Explain Azure Availability Zones vs Availability Sets
**A:**

| Feature | Availability Zones | Availability Sets |
|---|---|---|
| **Scope** | Separate physical datacenters within a region | Separate fault/update domains within one datacenter |
| **Protection against** | Datacenter-level failure | Rack-level hardware failure or planned maintenance |
| **SLA** | 99.99% VM uptime | 99.95% VM uptime |
| **Use case** | Zone-redundant, modern workloads | Legacy workloads that can't be zone-aware |

> [!important]
> Availability Zones are the **modern standard**. Availability Sets are an older construct and are generally recommended only when Zone support is unavailable for a specific VM SKU or region. In AKS, you configure zone distribution at the node pool level.

---

## Q7: What is the difference between Azure Firewall and NSG?
**A:**

| Feature | NSG (Network Security Group) | Azure Firewall |
|---|---|---|
| **Layer** | Layer 4 (TCP/UDP ports and IPs) | Layer 4 + Layer 7 (FQDNs, URLs, TLS inspection) |
| **Scope** | Applied to a NIC or Subnet | Centralized, deployed in a dedicated subnet |
| **FQDN filtering** | No | Yes (can allow `*.microsoft.com`) |
| **Threat Intelligence** | No | Yes (blocks known malicious IPs) |
| **Cost** | Free | ~$1.25/hr + data processing costs |
| **Management** | Per-resource rules | Centralized via Firewall Policy |

> [!note] When to use which
> Use **NSGs** for micro-segmentation between subnets (east-west traffic control). Use **Azure Firewall** for centralized north-south traffic control (internet ingress/egress), FQDN filtering, and threat intelligence. In a production hub-spoke topology, you typically use **both** together.

```
Internet --> Azure Firewall (hub VNet) --> NSG rules --> Application Subnet
```

---

## Q8: When would you use Private Endpoints vs Service Endpoints?
**A:**

| Feature | Service Endpoint | Private Endpoint |
|---|---|---|
| **Traffic path** | Optimized public path (still uses public IP of service) | Fully private via a private IP in your VNet |
| **Network exposure** | Service still has a public IP | Service is completely off the public internet |
| **DNS** | No change needed | Requires Private DNS Zone to resolve to private IP |
| **Cost** | Free | ~$0.01/hr + data transfer |
| **Use case** | Quick, low-cost private access for trusted subnets | Regulatory compliance, zero public exposure required |

> [!warning]
> **Service Endpoints** do not make the service private — they only restrict *which* VNet can reach the public endpoint. A **Private Endpoint** actually assigns a private IP (e.g., `10.0.1.5`) inside your VNet, making it completely isolated from the public internet. For PCI-DSS, HIPAA, or any compliance-sensitive workload, always prefer **Private Endpoints**.

---

## Q9: What is Azure Policy and how is it different from RBAC?
**A:**
- **RBAC (Role-Based Access Control)** controls *what actions* a user or identity **can do** (e.g., "can this person create a VM?"). It is about **permissions on identities**.
- **Azure Policy** controls *what resources* **can exist** (e.g., "all storage accounts in this subscription MUST use HTTPS only and MUST be in East US"). It is about **compliance enforcement on resources**.

**Key Azure Policy effects:**

| Effect | Behavior |
|---|---|
| `Deny` | Blocks the resource creation/update if it violates the rule |
| `Audit` | Allows the action but flags it as non-compliant in the compliance report |
| `Append` | Adds additional fields to the resource (e.g., tags) |
| `DeployIfNotExists` | Deploys a remediation resource if the condition is not met |

> [!tip]
> Group related policies into a **Policy Initiative (Policy Set)** for easier assignment. Use `Audit` mode first when rolling out new policies to understand impact before switching to `Deny`.

---

## Q10: Explain the AKS Networking Models (kubenet vs Azure CNI)
**A:**

| Feature | kubenet | Azure CNI |
|---|---|---|
| **IP allocation** | Pods get IPs from a private overlay network, NAT'd to node IP | Each Pod gets a real IP from the VNet subnet |
| **VNet integration** | Indirect (only nodes have VNet IPs) | Direct (pods are first-class VNet citizens) |
| **IP consumption** | Low (efficient) | High (need to pre-allocate IPs for max pod count) |
| **Network Policy** | Calico only | Calico or Azure Network Policy |
| **Windows node pools** | Not supported | Supported |
| **Use case** | Dev/test, large clusters needing IP efficiency | Production, service integration with other VNet resources |

> [!important] Azure CNI Overlay (modern choice)
> Azure CNI Overlay is the recommended modern option — it assigns pods IPs from a private CIDR (not consuming VNet space) while still allowing direct VNet-level connectivity. It combines the IP efficiency of kubenet with the capabilities of Azure CNI.

```bash
# Create AKS cluster with Azure CNI Overlay
az aks create \
  --resource-group myRG \
  --name myAKS \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --pod-cidr 192.168.0.0/16
```

---

## Q11: What is Entra ID Conditional Access and PIM?
**A:**

**Conditional Access** is a policy engine in Entra ID that evaluates signals (user, device, location, app, risk) and enforces access controls. It operates as an "if-then" policy:

```
IF user is accessing Azure Portal
AND sign-in risk is High
THEN require MFA + compliant device
```

Common signals: User/Group, IP location, Device compliance (Intune), Application, Sign-in risk score.

**Privileged Identity Management (PIM)** provides **Just-In-Time (JIT)** privileged access:
- Users are **eligible** for high-privilege roles (e.g., Global Admin, Subscription Owner) but do **not** hold them permanently.
- When needed, they **activate** the role for a limited time window (e.g., 1-8 hours) with a justification and optional MFA/approval.
- All activations are **audited**.

> [!important]
> The combination of Conditional Access + PIM is a core **Zero Trust** control. No account should have permanent standing privileges. PIM enforces this at the identity layer while Conditional Access enforces contextual access controls.

---

## Q12: How does Azure Front Door differ from Azure Application Gateway?
**A:**

| Feature | Azure Application Gateway | Azure Front Door |
|---|---|---|
| **Scope** | Regional load balancer (one region) | Global load balancer (multi-region) |
| **Layer** | Layer 7 (HTTP/HTTPS) | Layer 7 + global anycast |
| **WAF** | Yes (WAF v2) | Yes (WAF Policy) |
| **SSL Termination** | Yes | Yes |
| **URL path routing** | Yes | Yes |
| **Global failover** | No | Yes (routes to nearest healthy origin) |
| **CDN / Caching** | No | Yes |
| **Private backend** | Yes (via Private Link) | Yes (Premium SKU via Private Link) |
| **Use case** | Single-region app with WAF | Multi-region app, global CDN, geo-routing |

> [!note] Decision guide
> - Single-region microservices on AKS/VMs → **Application Gateway** (often as the AKS ingress controller via AGIC).
> - Multi-region SaaS application requiring global load balancing and CDN → **Azure Front Door**.
> - For maximum security, Front Door Premium + WAF Policy blocks attacks at the **edge** before traffic even reaches your region.

---

## Related Notes
- [[Security]] — Azure security controls and NSG deep dive
- [[AKS]] — Kubernetes on Azure architecture
- [[Networking]] — VNet, peering, and DNS concepts
