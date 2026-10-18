---
tags: [caf, mapping, framework, azure]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# CAF Phase Mapping for Current Projects

A mapping of our current ongoing projects to the Microsoft Cloud Adoption Framework (CAF) phases to ensure we are following best practices.

## CAF Overview

The Microsoft Cloud Adoption Framework (CAF) is a lifecycle-based framework organized into six iterative phases:

```
Strategy → Plan → Ready → Adopt → Govern → Manage
                            ↑
                     (Landing Zone lives here)
```

> [!important]
> The **Ready** phase (Landing Zone) must be completed before the **Adopt** phase begins. Skipping Ready leads to sprawl, security gaps, and costly remediation.

---

## 1. Strategy Phase
*Defining business justification and expected outcomes.*

**Goal:** Secure executive sponsorship. Quantify the business value of cloud adoption.

- **Current Project:** TCO (Total Cost of Ownership) analysis comparing our current on-premises VMware cluster costs vs a proposed Azure IaaS migration.
- **Key Deliverables:** Business case document, Cloud Economics report, Stakeholder RACI matrix
- **Tools Used:** [Azure Total Cost of Ownership Calculator](https://azure.microsoft.com/en-us/pricing/tco/calculator/), Azure Pricing Calculator

### Motivations Identified
| Motivation | Category | Priority |
|------------|----------|----------|
| Reduce datacenter footprint | Cost optimization | High |
| Improve developer agility | Innovation | Medium |
| GDPR data sovereignty compliance | Critical business event | High |
| End of support for Windows Server 2016 | Critical business event | High |

---

## 2. Plan Phase
*Aligning actionable adoption plans to business outcomes.*

**Goal:** Create a digital estate inventory. Rationalize applications. Build the skills readiness plan.

- **Current Project:** Creating a comprehensive inventory of all on-premises applications and categorizing them into the **5 R's** (Rehost, Refactor, Rearchitect, Rebuild, Replace).
- **Key Deliverables:** Application inventory spreadsheet, Skills gap analysis, Cloud adoption plan with milestones

### 5 R's Rationalization Summary
| Workload                           | Current State       | Strategy                | Target State        |
| ---------------------------------- | ------------------- | ----------------------- | ------------------- |
| 50x legacy Windows Server 2016 VMs | On-premises vSphere | Rehost (Lift & Shift)   | Azure IaaS          |
| Monolithic inventory app           | On-prem .NET 4.8    | Refactor → Containerize | AKS microservices   |
| SAP ERP                            | On-prem SAP HANA    | Rehost                  | Azure VM (M-series) |
| Legacy HR portal                   | Old PHP app         | Replace                 | SaaS (Workday)      |
| Internal ticketing tool            | On-prem Jira        | Replace                 | Azure DevOps Boards |

---

## 3. Ready Phase
*Preparing the cloud environment — the **Landing Zone**.*

**Goal:** Deploy the foundational environment before any workloads are migrated.

- **Current Project:** **Azure Landing Zone Deployment.** Designing the Management Group hierarchy, configuring the Hub and Spoke network topology using Azure Virtual WAN, and setting up the central Log Analytics Workspace. *(This must be completed before the Adopt phase begins).*

### Landing Zone Checklist
- [x] Entra ID tenant configured (custom domain, MFA enforced)
- [x] Management Group hierarchy deployed via Terraform
- [x] Platform subscriptions created (Connectivity, Identity, Management)
- [x] Hub VNet deployed with Azure Firewall in Connectivity subscription
- [x] Azure Bastion deployed for secure VM management access
- [x] Central Log Analytics Workspace deployed in Management subscription
- [x] Diagnostic settings forwarding all platform logs to Log Analytics
- [x] Baseline Azure Policies assigned at Root Management Group
- [ ] ExpressRoute circuit ordered and provisioned (8-12 week lead time from ISP)
- [ ] Private DNS Resolver deployed and linked to on-premises DNS

---

## 4. Adopt Phase
*Implementing the desired changes.*

### Migrate Track
- **Goal:** Move existing workloads to Azure (Rehost, Replatform)
- **Current Project:** Using Azure Migrate to "Lift and Shift" 50 legacy Windows Server 2016 VMs to Azure IaaS in the new Landing Zone spokes.

**Migration Waves:**
| Wave | Workloads | Timeline | Status |
|------|-----------|----------|--------|
| Wave 1 (Pilot) | 3 non-critical Dev/Test VMs | Week 1-2 | ✅ Complete |
| Wave 2 | 15 internal tools VMs | Week 3-6 | 🔄 In Progress |
| Wave 3 | 20 business-critical app VMs | Week 7-10 | ⏳ Planned |
| Wave 4 | 12 production database VMs | Week 11-14 | ⏳ Planned |

### Innovate Track
- **Goal:** Build cloud-native applications that leverage Azure PaaS services
- **Current Project:** Refactoring the monolithic inventory application into containerized microservices and deploying them to an Azure Kubernetes Service (AKS) cluster.

**AKS Platform Status:** See [[08-Real-World-Projects/AKS-Platform]]

---

## 5. Govern Phase (Ongoing)
*Benchmarking and implementing governance best practices.*

**Goal:** Prevent cloud sprawl. Enforce organizational standards automatically.

- **Current Project:** Drafting and deploying Custom Azure Policies to automatically tag resources with `CostCenter` and `Environment` tags upon creation.

### Active Policy Assignments
| Policy Name | Effect | Scope | Status |
|-------------|--------|-------|--------|
| Require CostCenter tag | `Modify` (append tag) | Root MG | ✅ Active |
| Deny Public IP on NICs | `Deny` | Corp Landing Zone MG | ✅ Active |
| Enforce TLS 1.2 on Storage | `Deny` | Root MG | ✅ Active |
| Deploy Diagnostic Settings | `DeployIfNotExists` | Root MG | ✅ Active |
| Allowed VM SKUs | `Deny` | Non-prod MGs | ✅ Active |
| Require Key Vault soft delete | `Deny` | Root MG | ⏳ In Review |

### Microsoft Defender for Cloud
- **Secure Score Target:** > 80%
- **Current Score:** 71% (as of last assessment)
- **Top Remediation Items:** Enable MFA for admin accounts, enable disk encryption on remaining VMs

---

## 6. Manage Phase (Ongoing)
*Establishing operational baselines.*

**Goal:** Monitor health. Respond to incidents. Optimize costs continuously.

- **Current Project:** Configuring Azure Monitor Action Groups to page the on-call DevOps engineer if the Azure Firewall CPU utilization exceeds 85%.

### Operational Baselines Implemented
| Capability | Tool | Status |
|-----------|------|--------|
| Infrastructure monitoring | Azure Monitor | ✅ Active |
| Log aggregation | Log Analytics Workspace | ✅ Active |
| Alerting & on-call | Azure Monitor Action Groups + PagerDuty | ✅ Active |
| Container monitoring | Container Insights (AKS) | ✅ Active |
| Cost management | Azure Cost Management budgets | ✅ Active |
| Backup | Azure Backup (VMs + SQL) | ✅ Active |
| DR plan | Terraform IaC + Geo-Redundant backups | 🔄 In Progress |
| Security operations | Microsoft Sentinel | ⏳ Planned |

---

## CAF Alignment Summary

| CAF Phase | Our Maturity | Next Step |
|-----------|-------------|-----------|
| Strategy | ✅ Complete | N/A |
| Plan | ✅ Complete | N/A |
| Ready (Landing Zone) | 🔄 ~85% | Complete ExpressRoute + DNS Resolver |
| Adopt (Migrate) | 🔄 ~40% | Complete migration waves 3 & 4 |
| Adopt (Innovate) | 🔄 ~60% | Deploy AKS prod workloads |
| Govern | 🔄 ~70% | Reach Secure Score > 80%, add Key Vault policy |
| Manage | 🔄 ~60% | Deploy Sentinel, complete DR plan |
