---
tags: [interview, prep, landing-zone, alz, architecture]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Landing Zone Interview Questions

A collection of common interview questions regarding Azure Landing Zones and Enterprise Architecture.

## Q1: What is an Azure Landing Zone and why is it necessary?
**A:** An Azure Landing Zone is the foundational environment—essentially the plumbing, security, and governance architecture—required to host workloads in the cloud securely. It is necessary because without it, teams will deploy resources haphazardly, leading to overlapping IP addresses, lack of centralized logging, security vulnerabilities, and out-of-control costs.

## Q2: Explain the concept of "Subscription Democratization".
**A:** Subscription Democratization is a core design principle of the Azure Landing Zone Accelerator. It means treating subscriptions as disposable units of scale rather than trying to fit an entire enterprise into one or two subscriptions. By giving different workloads or environments their own subscriptions, you isolate the "blast radius" of errors, avoid hitting Azure resource limits, and make billing allocation much simpler.

## Q3: If you have dozens of subscriptions, how do you enforce security rules across all of them efficiently?
**A:** By using **Management Groups** and **Azure Policy**. I would organize the subscriptions under a logical Management Group hierarchy (e.g., placing all internal apps under a "Corp" management group). Then, I would assign Azure Policies at the Management Group level (e.g., "Deny public IPs"). This policy automatically cascades down and is enforced on every single subscription inside that group, eliminating the need to configure them individually.

## Q4: How do you handle routing between multiple Spoke VNets in a Hub and Spoke architecture?
**A:** Because VNet Peering is not transitive (Spoke A cannot talk to Spoke B directly even if both are peered to the Hub), I would deploy a Network Virtual Appliance (like Azure Firewall) in the Hub VNet. I would then attach a Route Table with a User Defined Route (UDR) to the subnets in Spoke A and Spoke B, instructing them to send traffic destined for other spokes to the private IP of the Azure Firewall.

## Q5: What is the Cloud Adoption Framework (CAF)?
**A:** The Microsoft Cloud Adoption Framework is a set of documentation, best practices, and tools that guide an organization through their cloud journey. It covers everything from business strategy and planning to the actual technical implementation (the Ready phase, which produces the Landing Zone), and ongoing Governance and Management.

## Q6: What are the different subscription types in an Azure Landing Zone?
**A:** The Azure Landing Zone Accelerator defines these key subscription archetypes:
- **Platform subscriptions:** Managed by the central Cloud Center of Excellence (CCoE) team. Contains shared infrastructure that all workloads depend on:
  - **Connectivity subscription:** Hub VNet, Firewalls, ExpressRoute Gateways, VPN Gateways
  - **Identity subscription:** Domain Controllers, Active Directory, Entra Domain Services
  - **Management subscription:** Log Analytics Workspace, Automation Accounts, Defender for Cloud
- **Landing Zone subscriptions:** Individual subscriptions for each application team or environment (Corp, Online, SAP).
- **Sandbox subscriptions:** Loosely governed, time-limited subscriptions where developers can experiment without impacting production. Often have a soft budget cap enforced by Azure Policy.
- **Decommissioned subscriptions:** A management group where cancelled subscriptions are moved before final deletion, retaining their audit logs for compliance.

## Q7: How do Azure Policies differ from RBAC, and when would you use each?
**A:**
- **RBAC (Role-Based Access Control)** controls *who* can *do what*. It answers: "Can John create a VM?" It grants permissions to perform actions (read, write, delete) on resources.
- **Azure Policy** controls *what* can be *created* and *ensures compliance* of existing resources. It answers: "Even if John has permission to create a VM, is the configuration compliant?" For example, Policy can deny the creation of any VM without a specific tag, or automatically remediate resources that don't use TLS 1.2.

> [!important]
> RBAC and Policy work *together*, not exclusively. Use RBAC to manage access, and Policy to enforce governance guardrails regardless of who made the change.

## Q8: Explain the concept of "Policy-Driven Governance" and give a real example.
**A:** Policy-Driven Governance means encoding your organizational security and compliance standards as Azure Policy definitions that automatically enforce themselves, rather than relying on human approval gates or documentation that people might ignore.

**Real example:** Instead of documenting "all storage accounts must be encrypted with Customer Managed Keys," you:
1. Create an Azure Policy with effect `Deny` that blocks any Storage Account creation without CMK enabled.
2. Create a separate `DeployIfNotExists` policy that automatically deploys a Diagnostic Setting to a central Log Analytics Workspace for every newly created Storage Account.
3. Assign both policies at the root Management Group so they apply everywhere.

Now the governance is self-enforcing — no security review required per resource.

## Q9: What is the difference between Hub-and-Spoke and Azure Virtual WAN? When do you choose each?
**A:**
| Factor | Hub & Spoke | Azure Virtual WAN |
|--------|-------------|-------------------|
| **Management** | Self-managed (you deploy Firewall, UDRs, peerings) | Microsoft-managed, automated routing |
| **Scale** | Works well up to ~50 spokes in a single region | Designed for 100s of spokes across multiple regions |
| **Transitivity** | Not native (requires NVA/Firewall in hub) | Native global transit between all hubs and spokes |
| **Cost** | Lower base cost | Higher base cost, justified at scale |
| **Multi-region** | Requires manual Global VNet Peering setup | Built-in global mesh between Virtual Hubs |
| **Best for** | Single-region, < 50 spokes, need fine-grained NVA control | Multi-region global enterprise, many branches |

## Q10: What is "Platform as Code" in the context of Landing Zones, and how do you implement it?
**A:** Platform as Code means that the entire Landing Zone infrastructure (Management Groups, subscriptions, policies, hub networking, logging) is defined in Terraform/Bicep code and deployed via CI/CD pipelines — just like application code. The benefits are:
1. **Auditability:** Every change is tracked in Git with a pull request, reviewer, and commit message.
2. **Reproducibility:** You can spin up an identical copy of the Landing Zone in a DR region in minutes.
3. **Drift Detection:** Running `terraform plan` against the production Landing Zone infrastructure detects unauthorized manual changes made via the Portal.

**Implementation:** Use a dedicated Git repository (e.g., `platform-landing-zone`) with a GitHub Actions pipeline that:
1. On PR → runs `terraform plan` and posts the output as a PR comment
2. On merge to `main` → runs `terraform apply` with `-auto-approve`
3. Is protected by branch protection rules requiring 2 reviewers before merge
