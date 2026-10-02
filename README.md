<div align="center">

# 🚀 DevOps Knowledge Base
### DevOps Insiders Batch 18

![Views](https://komarev.com/ghpvc/?username=MihirMaurya-dev-DevOps-Notes&label=Views&color=007EC6&style=flat)
![Platform](https://img.shields.io/badge/Platform-Azure-0089D6?logo=microsoft-azure&logoColor=white)
![IaC](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Azure_DevOps-0078D7?logo=azure-devops&logoColor=white)
![Obsidian Vault](https://img.shields.io/badge/Obsidian-Vault-7c3aed?logo=obsidian&logoColor=white)

> **A production-grade Obsidian vault for mastering Azure, Terraform, CI/CD, Linux, and Enterprise Architecture**  
> Built for real-world DevOps engineering roles and Azure certification interviews.

</div>

---

## 🧭 About This Vault

This vault is a structured, evergreen knowledge base developed as part of the **DevOps Insiders Batch 18** learning program. It covers the full DevOps engineering stack — from IaC fundamentals to enterprise-scale Azure Landing Zones — with a focus on:

- ✅ **Interview readiness** for Azure/DevOps engineer roles
- ✅ **Production-grade patterns** drawn from real enterprise projects
- ✅ **Microsoft CAF alignment** for Landing Zone and governance design
- ✅ **Hands-on implementations** with annotated code and decision logs

> **Vault Engine:** [Obsidian](https://obsidian.md) | **Program:** DevOps Insiders Batch 18 | **Last Updated:** August 2026

---

## 📚 Table of Contents

| #   | Section                            | Description                      | Notes                                |
| --- | ---------------------------------- | -------------------------------- | ------------------------------------ |
| 🏗️ | [01 — Terraform](#-01--terraform)             | IaC from zero to advanced        | HCL, State, Modules, Workspaces      |
| ☁️  | [02 — Azure](#-02--azure)                 | Core Azure services & networking | AKS, VNet, RBAC, Key Vault           |
| 🏢  | [03 — Landing Zone](#-03--landing-zone)          | Azure Landing Zone & CAF         | Enterprise-Scale, Governance         |
| 🔄  | [04 — CI/CD](#-04--cicd)                 | Pipelines & GitOps automation    | Azure DevOps, GitHub Actions         |
| 🐧  | [05 — Linux](#-05--linux)                 | Linux mastery for DevOps         | Commands, Bash, Networking           |
| 🏛️ | [06 — Architecture Patterns](#-06--architecture-patterns) | Enterprise design patterns       | Hub-Spoke, Zero-Trust, DR            |
| 🎯  | [07 — Interview Prep](#-07--interview-prep)        | Curated Q&A by domain            | Scenario-based, Security             |
| 🔨  | [08 — Real-World Projects](#-08--real-world-projects)   | Full project implementations     | AKS Platform, Secure Hub-Spoke       |
| 📋  | [09 — Decision Logs](#-09--decision-logs)         | Architecture Decision Records    | ADRs with rationale                  |
| 🗺️ | [10 — CAF Mapping](#-10--caf-mapping)           | Cloud Adoption Framework map     | Workloads ↔ CAF pillars              |
| 📅  | [11 — Weekly Learning](#-11--weekly-learning)       | Progress tracker & goals         | Weekly reviews                       |
| 🤖  | [12 — Agentic AI](#-12--agentic-ai)            | AI in DevOps engineering         | Tool calling, automation             |
| 🌿  | [13 — Git](#-13--git)                   | Git & platform workflows         | GitHub, Azure Repos, PR, Code Review |
| 🔐  | [14 — Security Scanning](#-14--security-scanning)     | IaC & secrets security scanning  | TFLint, tfsec, Checkov, Gitleaks     |
| 💰  | [15 — Cost & Governance](#-15--cost--governance)     | Cost management & governance     | Tagging, Naming, RBAC, OpenCost      |
| ❓  | [16 — DI Interview Questions](#-16--di-interview-questions) | DevOps Insiders interview questions | Companies & topics                   |

---

## 🏗️ 01 — Terraform

> Infrastructure as Code fundamentals through advanced enterprise patterns using HashiCorp Terraform.

### Fundamentals
| Topic                        | File                                                                                                                             | Description                    |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| 📖 Declarative vs Imperative | [`01-Terraform/00-IaC-Fundamentals/Declarative-vs-Imperative.md`](01-Terraform/00-IaC-Fundamentals/01-Declarative-vs-Imperative.md) | IaC approaches explained       |
| 📖 State Theory              | [`01-Terraform/00-IaC-Fundamentals/State-Theory.md`](01-Terraform/00-IaC-Fundamentals/02-State-Theory.md)                           | Deep dive into Terraform state |

### Core Topics
| Topic | File | Description |
|-------|------|-------------|
| 📖 Introduction | [`01-Terraform/01-Introduction.md`](01-Terraform/01-Introduction.md) | What is Terraform, why IaC |
| ⚙️ Installation | [`01-Terraform/02-Installation.md`](01-Terraform/02-Installation.md) | Install, configure, tfenv |
| 🔌 Providers | [`01-Terraform/03-Providers.md`](01-Terraform/03-Providers.md) | AzureRM, version locking |
| 🧱 Resources | [`01-Terraform/04-Resources.md`](01-Terraform/04-Resources.md) | Resource blocks, meta-args |
| 📥 Variables | [`01-Terraform/05-Variables.md`](01-Terraform/05-Variables.md) | Input vars, tfvars, env vars |
| 🔧 Locals | [`01-Terraform/06-Locals.md`](01-Terraform/06-Locals.md) | Local values, expressions |
| 📤 Outputs | [`01-Terraform/07-Outputs.md`](01-Terraform/07-Outputs.md) | Output blocks, sensitive values |
| 💾 State Management | [`01-Terraform/08-State-Management.md`](01-Terraform/08-State-Management.md) | State file, locking, drift |
| 🌐 Remote Backend | [`01-Terraform/09-Remote-Backend.md`](01-Terraform/09-Remote-Backend.md) | Azure Blob, state locking, env-wise state |
| 📦 Modules | [`01-Terraform/10-Modules.md`](01-Terraform/10-Modules.md) | Module structure, registry |
| 🌍 Workspaces | [`01-Terraform/11-Workspaces.md`](01-Terraform/11-Workspaces.md) | Multi-env with workspaces |
| 🔍 Data Sources | [`01-Terraform/12-Data-Sources.md`](01-Terraform/12-Data-Sources.md) | Querying existing resources |
| 🔁 Loops & Conditionals | [`01-Terraform/13-Loops-Conditionals.md`](01-Terraform/20-Loops-Conditionals.md) | count, for_each, dynamic |
| ♻️ Lifecycle | [`01-Terraform/14-Lifecycle.md`](01-Terraform/14-Lifecycle.md) | create_before_destroy, ignore_changes |
| ⭐ Best Practices | [`01-Terraform/15-Best-Practices.md`](01-Terraform/15-Best-Practices.md) | Naming, structure, security |
| 🖥️ Commands Reference | [`01-Terraform/16-Commands-Reference.md`](01-Terraform/16-Commands-Reference.md) | Every CLI command — what it does, effects, before/after |
| 📝 Cheat Sheet | [`01-Terraform/Cheat-Sheet.md`](01-Terraform/19-Cheat-Sheet.md) | Quick command reference |
| ❓ Interview Questions | [`01-Terraform/Interview-Questions.md`](01-Terraform/18-Interview-Questions.md) | Top interview Q&A |

### Resource Library
| Resource | File | Description |
|----------|------|-------------|
| 📋 README | [`01-Terraform/Resource-Library/README.md`](01-README.md) | Library index |
| ☸️ AKS | [`01-Terraform/Resource-Library/AKS.md`](02-AKS.md) | AKS Terraform snippets |
| 🔑 Key Vault | [`01-Terraform/Resource-Library/Key-Vault.md`](03-Key-Vault.md) | Key Vault resource blocks |
| 📊 Log Analytics | [`01-Terraform/Resource-Library/Log-Analytics.md`](04-Log-Analytics.md) | Log Analytics workspace |
| 🛡️ NSG | [`01-Terraform/Resource-Library/NSG.md`](05-NSG.md) | NSG + rules resource blocks |
| 📁 Resource Group | [`01-Terraform/Resource-Library/Resource-Group.md`](06-Resource-Group.md) | Resource Group patterns |
| 💾 Storage Account | [`01-Terraform/Resource-Library/Storage-Account.md`](07-Storage-Account.md) | Storage Account resource |
| 🔀 Subnet | [`01-Terraform/Resource-Library/Subnet.md`](08-Subnet.md) | Subnet resource blocks |
| 🖥️ VM | [`01-Terraform/Resource-Library/VM.md`](09-VM.md) | Linux/Windows VM resource |
| 🌐 VNet | [`01-Terraform/Resource-Library/VNet.md`](10-VNet.md) | Virtual Network resource |

---

## ☁️ 02 — Azure

> Core Azure services, networking fundamentals, and identity — the building blocks of every Azure deployment.

### Cloud & Networking Fundamentals
| Topic | File | Description |
|-------|------|-------------|
| ☁️ Cloud Models & Virtualisation | [`02-Azure/00-Cloud-Fundamentals/Cloud-Models-And-Virtualization.md`](02-Azure/00-Cloud-Fundamentals/01-Cloud-Models-And-Virtualization.md) | IaaS/PaaS/SaaS, cloud types |
| 💻 Virtualisation Basics | [`02-Azure/00-Cloud-Fundamentals/Virtualization-Basics.md`](02-Azure/00-Cloud-Fundamentals/02-Virtualization-Basics.md) | Hypervisors, VMs, containers |
| ❓ Cloud Fundamentals Q&A | [`02-Azure/00-Cloud-Fundamentals/Interview-Questions.md`](02-Azure/00-Cloud-Fundamentals/03-Interview-Questions.md) | Cloud basics interview Q&A |
| 🌐 DNS & Routing | [`02-Azure/00-Networking-Fundamentals/DNS-and-Routing.md`](02-Azure/00-Networking-Fundamentals/01-DNS-and-Routing.md) | DNS resolution, routing tables |
| 🔢 IP Addressing & CIDR | [`02-Azure/00-Networking-Fundamentals/IP-Addressing-and-CIDR.md`](02-Azure/00-Networking-Fundamentals/02-IP-Addressing-and-CIDR.md) | Subnetting, CIDR notation |
| 🔌 Ports & Protocols | [`02-Azure/00-Networking-Fundamentals/Ports-and-Protocols.md`](02-Azure/00-Networking-Fundamentals/03-Ports-and-Protocols.md) | TCP/UDP, common ports |
| ❓ Networking Q&A | [`02-Azure/00-Networking-Fundamentals/Interview-Questions.md`](02-Azure/00-Networking-Fundamentals/04-Interview-Questions.md) | Networking interview Q&A |

### Azure Services
| Topic | File | Description |
|-------|------|-------------|
| 🧩 Azure Fundamentals | [`02-Azure/Azure-Fundamentals.md`](02-Azure/01-Azure-Fundamentals.md) | Regions, Resource Manager |
| 🏗️ Architecture Fundamentals | [`02-Azure/Azure-Architecture-Fundamentals.md`](02-Azure/02-Azure-Architecture-Fundamentals.md) | Availability Zones, pairs |
| 🌐 VNet | [`02-Azure/VNet.md`](02-Azure/03-VNet.md) | Virtual Networks, peering |
| 🔀 Subnets | [`02-Azure/Subnets.md`](02-Azure/04-Subnets.md) | Subnet design, delegation |
| 🛡️ NSG | [`02-Azure/NSG.md`](02-Azure/36-NSG.md) | Network Security Groups |
| 🗺️ Route Tables | [`02-Azure/Route-Tables.md`](02-Azure/06-Route-Tables.md) | UDR, BGP, forced tunneling |
| 🔑 RBAC | [`02-Azure/RBAC.md`](02-Azure/35-RBAC.md) | Roles, assignments, custom roles |
| 🪪 Managed Identity | [`02-Azure/Managed-Identity.md`](02-Azure/08-Managed-Identity.md) | System/User assigned MI |
| 🔒 Key Vault | [`02-Azure/Key-Vault.md`](02-Azure/09-Key-Vault.md) | Secrets, certs, access policies |
| 💾 Storage Account | [`02-Azure/Storage-Account.md`](02-Azure/10-Storage-Account.md) | Blob, tiers, lifecycle |
| 📊 Monitor | [`02-Azure/Monitor.md`](02-Azure/11-Monitor.md) | Metrics, Alerts, Dashboards |
| 📋 Log Analytics | [`02-Azure/Log-Analytics.md`](02-Azure/37-Log-Analytics.md) | Workspace, KQL queries |
| ☸️ AKS | [`02-Azure/AKS.md`](02-Azure/13-AKS.md) | Azure Kubernetes Service |
| 📁 Resource Groups | [`02-Azure/Resource-Groups.md`](02-Azure/14-Resource-Groups.md) | RG design patterns |
| 🖥️ VM | [`02-Azure/VM.md`](02-Azure/15-VM.md) | Virtual Machines, scale sets |
| ⚖️ VMSS | [`02-Azure/VMSS.md`](02-Azure/16-VMSS.md) | Virtual Machine Scale Sets |
| 🚪 Bastion | [`02-Azure/Bastion.md`](02-Azure/17-Bastion.md) | Secure RDP/SSH access |
| 🔌 NIC | [`02-Azure/NIC.md`](02-Azure/18-NIC.md) | Network Interfaces, IP forwarding |
| 🛡️ App Gateway | [`02-Azure/App-Gateway.md`](02-Azure/19-App-Gateway.md) | Layer 7 routing, WAF, AGIC |
| 🌍 Front Door | [`02-Azure/Front-Door.md`](02-Azure/20-Front-Door.md) | Global CDN, Edge WAF |
| 🔀 Traffic Manager | [`02-Azure/Traffic-Manager.md`](02-Azure/21-Traffic-Manager.md) | DNS-based global routing |
| ⚖️ Load Balancer | [`02-Azure/Load-Balancer.md`](02-Azure/22-Load-Balancer.md) | Layer 4 TCP/UDP load balancer |
| 🔗 Private Link | [`02-Azure/Private-Link.md`](02-Azure/23-Private-Link.md) | Private Endpoints, DNS |
| 🚢 ACR | [`02-Azure/ACR.md`](02-Azure/24-ACR.md) | Azure Container Registry |
| 🚇 VNet Gateway | [`02-Azure/Virtual-Network-Gateway.md`](02-Azure/25-Virtual-Network-Gateway.md) | VPN & ExpressRoute |
| 🛡️ Azure Policy | [`02-Azure/Azure-Policy.md`](02-Azure/26-Azure-Policy.md) | Governance & Compliance |
| 🔐 Entra ID | [`02-Azure/Entra-ID.md`](02-Azure/27-Entra-ID.md) | Identity and Access Management |
| 🏗️ Entra ID Architecture | [`02-Azure/Entra-ID-Architecture.md`](02-Azure/28-Entra-ID-Architecture.md) | Tenant, RBAC, Conditional Access |
| 💾 Azure Backup | [`02-Azure/Azure-Backup.md`](02-Azure/29-Azure-Backup.md) | VM, SQL, Files backup |
| 🌩️ Azure DR | [`02-Azure/Azure-DR.md`](02-Azure/30-Azure-DR.md) | Site Recovery, Cross-Region DR |
| 🛡️ Azure Security | [`02-Azure/Azure-Security.md`](02-Azure/31-Azure-Security.md) | Defender for Cloud, CSPM |
| 📝 Cheat Sheet | [`02-Azure/Cheat-Sheet.md`](02-Azure/34-Cheat-Sheet.md) | Azure CLI quick reference |
| ❓ Interview Questions | [`02-Azure/Interview-Questions.md`](02-Azure/33-Interview-Questions.md) | Core Azure Q&A |

---

## 🏢 03 — Landing Zone

> Azure Landing Zone design, Cloud Adoption Framework (CAF), and enterprise-scale governance patterns.

### Architecture Fundamentals
| Topic | File | Description |
|-------|------|-------------|
| 🕸️ Hub-Spoke Theory | [`03-Landing-Zone/00-Architecture-Fundamentals/Hub-Spoke-Theory.md`](03-Landing-Zone/00-Architecture-Fundamentals/01-Hub-Spoke-Theory.md) | Hub-Spoke design deep dive |
| 🔒 Zero Trust Basics | [`03-Landing-Zone/00-Architecture-Fundamentals/Zero-Trust-Basics.md`](03-Landing-Zone/00-Architecture-Fundamentals/02-Zero-Trust-Basics.md) | Zero Trust principles |
| ❓ Architecture Q&A | [`03-Landing-Zone/00-Architecture-Fundamentals/Interview-Questions.md`](03-Landing-Zone/00-Architecture-Fundamentals/03-Interview-Questions.md) | Architecture interview Q&A |

### Landing Zone Topics
| Topic | File | Description |
|-------|------|-------------|
| 📖 Introduction | [`03-Landing-Zone/Introduction.md`](03-Landing-Zone/01-Introduction.md) | What is a Landing Zone |
| 🗺️ CAF Overview | [`03-Landing-Zone/CAF-Overview.md`](03-Landing-Zone/02-CAF-Overview.md) | CAF methodology, pillars |
| 🏛️ Enterprise Scale | [`03-Landing-Zone/Enterprise-Scale.md`](03-Landing-Zone/03-Enterprise-Scale.md) | ALZ reference architecture |
| 🏗️ Architecture | [`03-Landing-Zone/Architecture.md`](03-Landing-Zone/04-Architecture.md) | Design areas, components |
| 🗂️ Management Groups | [`03-Landing-Zone/Management-Groups.md`](03-Landing-Zone/05-Management-Groups.md) | MG hierarchy design |
| 📋 Subscription Strategy | [`03-Landing-Zone/Subscription-Strategy.md`](03-Landing-Zone/06-Subscription-Strategy.md) | Subscription models |
| 🏷️ Resource Organization | [`03-Landing-Zone/Resource-Organization.md`](03-Landing-Zone/07-Resource-Organization.md) | Naming, tagging standards |
| 🆔 Identity & Access | [`03-Landing-Zone/Identity-and-Access-Management.md`](03-Landing-Zone/08-Identity-and-Access-Management.md) | Entra ID, PIM, RBAC |
| 🌐 Network Topology | [`03-Landing-Zone/Network-Topology-and-Connectivity.md`](03-Landing-Zone/09-Network-Topology-and-Connectivity.md) | Hub-Spoke, WAN |
| 🛡️ Security | [`03-Landing-Zone/Security.md`](03-Landing-Zone/10-Security.md) | Defender, Sentinel, controls |
| 📜 Policies | [`03-Landing-Zone/Policies.md`](03-Landing-Zone/11-Policies.md) | Azure Policy, initiatives |
| 🏛️ Governance | [`03-Landing-Zone/Governance.md`](03-Landing-Zone/12-Governance.md) | Compliance, cost, tagging |
| 📊 Management | [`03-Landing-Zone/Management.md`](03-Landing-Zone/13-Management.md) | Ops management, patching |
| 👁️ Monitoring | [`03-Landing-Zone/Monitoring.md`](03-Landing-Zone/14-Monitoring.md) | ALZ monitoring baseline |
| 🤖 Platform Automation | [`03-Landing-Zone/Platform-Automation-and-DevOps.md`](03-Landing-Zone/15-Platform-Automation-and-DevOps.md) | IaC-driven LZ deployment |
| 💰 Billing & Entra | [`03-Landing-Zone/Azure-Billing-and-Entra-Tenant.md`](03-Landing-Zone/16-Azure-Billing-and-Entra-Tenant.md) | Tenant, EA, MCA setup |
| 🏗️ Modular Landing Zone | [`03-Landing-Zone/Terraform-Modular-Landing-Zone.md`](03-Landing-Zone/17-Terraform-Modular-Landing-Zone.md) | Terraform modular LZ pattern |
| ❓ Interview Questions | [`03-Landing-Zone/Interview-Questions.md`](03-Landing-Zone/18-Interview-Questions.md) | Landing Zone Q&A |

---

## 🔄 04 — CI/CD

> Pipeline design, GitOps workflows, and deployment automation for Azure-native and Kubernetes workloads.

### Pipeline Fundamentals
| Topic | File | Description |
|-------|------|-------------|
| 🌿 Branching Strategies | [`04-CI-CD/00-Pipeline-Fundamentals/Branching-Strategies.md`](04-CI-CD/00-Pipeline-Fundamentals/01-Branching-Strategies.md) | GitFlow, trunk-based dev |
| 🔁 GitOps Basics | [`04-CI-CD/00-Pipeline-Fundamentals/GitOps-Basics.md`](04-CI-CD/00-Pipeline-Fundamentals/02-GitOps-Basics.md) | ArgoCD, Flux fundamentals |

### CI/CD Topics
| Topic | File | Description |
|-------|------|-------------|
| 🔵 Azure DevOps | [`04-CI-CD/Azure-DevOps.md`](04-CI-CD/01-Azure-DevOps.md) | Pipelines, repos, boards |
| 🐙 GitHub Actions | [`04-CI-CD/GitHub-Actions.md`](04-CI-CD/02-GitHub-Actions.md) | Workflows, OIDC, runners |
| 🖥️ GitHub Actions Commands | [`04-CI-CD/GitHub-Actions-Commands-Reference.md`](04-CI-CD/03-GitHub-Actions-Commands-Reference.md) | Every YAML key, context, expression, and action used in pipelines |
| ☸️ AKS Deployment | [`04-CI-CD/AKS-Deployment.md`](04-CI-CD/04-AKS-Deployment.md) | Helm, manifests, rollouts |
| 🏗️ Terraform Pipeline | [`04-CI-CD/Terraform-Pipeline.md`](04-CI-CD/05-Terraform-Pipeline.md) | Plan/Apply gates, OIDC (Azure DevOps) |
| 🚀 GitHub Actions + Azure OIDC | [`04-CI-CD/GitHub-Actions-Terraform-OIDC.md`](04-CI-CD/06-GitHub-Actions-Terraform-OIDC.md) | Complete GitHub Actions Terraform CI/CD flow with OIDC — all 14 steps |
| 🔁 GitOps Fundamentals | [`04-CI-CD/GitOps-Fundamentals.md`](04-CI-CD/07-GitOps-Fundamentals.md) | GitOps principles & tools |
| 🚀 Release Strategy | [`04-CI-CD/Release-Strategy.md`](04-CI-CD/08-Release-Strategy.md) | Blue-Green, Canary, Ring |

---

## 🐧 05 — Linux

> Linux fundamentals, system administration, and Bash scripting for DevOps practitioners.

| Topic | File | Description |
|-------|------|-------------|
| 🖥️ File System Hierarchy | [`05-Linux/00-OS-Fundamentals/File-System-Hierarchy.md`](05-Linux/00-OS-Fundamentals/01-File-System-Hierarchy.md) | Linux FHS, mount points |
| ⚙️ Kernel Architecture | [`05-Linux/00-OS-Fundamentals/Kernel-Architecture.md`](05-Linux/00-OS-Fundamentals/02-Kernel-Architecture.md) | Kernel, processes, syscalls |
| ⌨️ Navigation & Files | [`05-Linux/01-Core-Commands/Navigation-and-Files.md`](05-Linux/01-Core-Commands/01-Navigation-and-Files.md) | ls, cd, find, cp, mv, rm |
| 🔍 Text Processing | [`05-Linux/01-Core-Commands/Text-Processing-Grep-Awk-Sed.md`](05-Linux/01-Core-Commands/02-Text-Processing-Grep-Awk-Sed.md) | grep, awk, sed patterns |
| 🔐 Users Groups Chmod | [`05-Linux/02-Permissions/Users-Groups-Chmod.md`](05-Linux/02-Permissions/01-Users-Groups-Chmod.md) | chmod, chown, ACLs, sudo |
| 🔑 SSH & Keys | [`05-Linux/03-Networking/SSH-and-Keys.md`](05-Linux/03-Networking/01-SSH-and-Keys.md) | SSH config, key pairs |
| 🌐 Troubleshooting | [`05-Linux/03-Networking/Troubleshooting-cURL-Ping.md`](05-Linux/03-Networking/02-Troubleshooting-cURL-Ping.md) | curl, ping, netstat, ss |
| ⏰ Cron Jobs | [`05-Linux/04-SysAdmin/Cron-Jobs.md`](05-Linux/04-SysAdmin/01-Cron-Jobs.md) | crontab, scheduling |
| 📦 Package Management | [`05-Linux/04-SysAdmin/Package-Management-Apt.md`](05-Linux/04-SysAdmin/02-Package-Management-Apt.md) | apt, dpkg, snap |
| 🔧 Systemd & Services | [`05-Linux/04-SysAdmin/Systemd-and-Services.md`](05-Linux/04-SysAdmin/03-Systemd-and-Services.md) | systemctl, journalctl |
| 📜 Automation Scripts | [`05-Linux/05-Bash-Scripting/Automation-Scripts.md`](05-Linux/05-Bash-Scripting/01-Automation-Scripts.md) | Real-world bash scripts |
| 🔡 Variables & Logic | [`05-Linux/05-Bash-Scripting/Variables-and-Logic.md`](05-Linux/05-Bash-Scripting/02-Variables-and-Logic.md) | if/else, loops, functions |
| 📝 Cheat Sheet | [`05-Linux/Cheat-Sheet.md`](05-Linux/02-Cheat-Sheet.md) | One-liner quick reference |

---

## 🏛️ 06 — Architecture Patterns

> Enterprise cloud architecture patterns applied to Azure workloads.

| Topic | File | Description |
|-------|------|-------------|
| 🏗️ 3-Tier Architecture | [`06-Architecture-Patterns/3-Tier-Architecture.md`](06-Architecture-Patterns/01-3-Tier-Architecture.md) | Web/App/DB tier design |
| 🕸️ Hub-Spoke | [`06-Architecture-Patterns/Hub-Spoke.md`](06-Architecture-Patterns/02-Hub-Spoke.md) | Hub-Spoke topology |
| 🌍 Multi-Region | [`06-Architecture-Patterns/Multi-Region.md`](06-Architecture-Patterns/03-Multi-Region.md) | Active-Active, geo-redundancy |
| 🔥 DR Strategy | [`06-Architecture-Patterns/DR-Strategy.md`](06-Architecture-Patterns/04-DR-Strategy.md) | RPO, RTO, failover design |
| 🔒 Zero Trust | [`06-Architecture-Patterns/Zero-Trust.md`](06-Architecture-Patterns/05-Zero-Trust.md) | Zero Trust architecture |
| 🏢 Enterprise Architecture | [`06-Architecture-Patterns/Enterprise-Architecture.md`](06-Architecture-Patterns/06-Enterprise-Architecture.md) | TOGAF, architecture views |
| 🤝 Shared Services | [`06-Architecture-Patterns/Shared-Services.md`](06-Architecture-Patterns/07-Shared-Services.md) | Centralized service design |
| 🔗 Service Mesh | [`06-Architecture-Patterns/Service-Mesh.md`](06-Architecture-Patterns/08-Service-Mesh.md) | Istio, mTLS, Envoy |

---

## 🎯 07 — Interview Prep

> Domain-specific interview questions and scenario-based walkthroughs for Azure/DevOps engineering roles.

| Topic | File | Description |
|-------|------|-------------|
| ☁️ Azure | [`07-Interview-Prep/Azure.md`](07-Interview-Prep/01-Azure.md) | Core Azure Q&A |
| 🏢 Landing Zone | [`07-Interview-Prep/Landing-Zone.md`](07-Interview-Prep/02-Landing-Zone.md) | LZ design questions |
| 🐧 Linux | [`07-Interview-Prep/Linux.md`](07-Interview-Prep/03-Linux.md) | Linux admin Q&A |
| 🌐 Networking | [`07-Interview-Prep/Networking.md`](07-Interview-Prep/04-Networking.md) | Azure networking deep-dives |
| 🎭 Scenario-Based | [`07-Interview-Prep/Scenario-Based.md`](07-Interview-Prep/10-Scenario-Based.md) | "What would you do if..." |
| 🛡️ Security | [`07-Interview-Prep/Security.md`](07-Interview-Prep/06-Security.md) | Security posture Q&A |
| 🏗️ Terraform | [`07-Interview-Prep/Terraform.md`](07-Interview-Prep/07-Terraform.md) | IaC interview scenarios |
| 🔄 CI/CD | [`07-Interview-Prep/CI-CD.md`](07-Interview-Prep/08-CI-CD.md) | Pipeline & GitOps Q&A |
| ☸️ Kubernetes & Docker | [`07-Interview-Prep/Kubernetes-Docker.md`](07-Interview-Prep/09-Kubernetes-Docker.md) | K8s & container Q&A |

---

## 🔨 08 — Real-World Projects

> End-to-end project implementations with architecture diagrams, code, and lessons learned.

| Project | File | Stack |
|---------|------|-------|
| ☸️ AKS Platform | [`08-Real-World-Projects/01-AKS-Platform.md`](08-Real-World-Projects/01-AKS-Platform.md) | AKS + ACR + Key Vault + OIDC |
| 🌐 Enterprise Network | [`08-Real-World-Projects/02-Enterprise-Network.md`](08-Real-World-Projects/02-Enterprise-Network.md) | Hub-Spoke + Firewall + VPN GW |
| 🏢 Landing Zone Deployment | [`08-Real-World-Projects/03-Landing-Zone-Deployment.md`](08-Real-World-Projects/03-Landing-Zone-Deployment.md) | Full ALZ via Terraform |
| 🔒 Secure Hub-Spoke | [`08-Real-World-Projects/04-Secure-Hub-Spoke.md`](08-Real-World-Projects/04-Secure-Hub-Spoke.md) | Zero-Trust Hub-Spoke topology |
| 🤖 Agentic AI Projects | [`08-Real-World-Projects/05-Agentic-AI-Industry-Projects.md`](08-Real-World-Projects/05-Agentic-AI-Industry-Projects.md) | ICU, Petroleum, Automotive (Interview Ready) |

---

## 📋 09 — Decision Logs

> Architecture Decision Records (ADRs) documenting key design choices, trade-offs, and rationale.

| ADR | File | Decision |
|-----|------|----------|
| 🕸️ Hub-Spoke | [`09-Decision-Logs/Hub-Spoke.md`](09-Decision-Logs/01-Hub-Spoke.md) | Why Hub-Spoke over flat VNet |
| 👥 RBAC Model | [`09-Decision-Logs/RBAC-Model.md`](09-Decision-Logs/02-RBAC-Model.md) | Custom vs built-in roles |
| 💾 Remote State | [`09-Decision-Logs/Remote-State.md`](09-Decision-Logs/03-Remote-State.md) | Azure Blob backend design |
| 🔒 Security Controls | [`09-Decision-Logs/Security-Controls.md`](09-Decision-Logs/04-Security-Controls.md) | Defender + Sentinel vs 3rd party |

---

## 🗺️ 10 — CAF Mapping

> Maps all vault topics to Cloud Adoption Framework pillars across strategy, govern, manage, and organize phases.

| File | Description |
|------|-------------|
| 📄 [`10-CAF-Mapping/CAF-Mapping.md`](10-CAF-Mapping/01-CAF-Mapping.md) | Cross-references workloads, services, and patterns against CAF methodology phases |

---

## 📅 11 — Weekly Learning

> Weekly study logs, goal tracking, and progress snapshots throughout the Batch 18 program.

| File | Description |
|------|-------------|
| 📅 [`11-Weekly-Learning/Progress-Tracker.md`](11-Weekly-Learning/01-Progress-Tracker.md) | Weekly entries with topics covered, blockers, and upcoming focus areas |

---

## 🤖 12 — Agentic AI

> The future of DevOps: Autonomous agents, tool calling, and LLM orchestration.

| Topic | File | Description |
|-------|------|-------------|
| 🗺️ Roadmap | [`12-Agentic-AI/00-Roadmap.md`](12-Agentic-AI/01-Roadmap.md) | Full Agentic AI for DevOps learning roadmap |
| 🧠 Introduction | [`12-Agentic-AI/01-Introduction.md`](12-Agentic-AI/02-Introduction.md) | Agents vs Gen AI, ReAct loop |
| 🛠️ Tool Calling | [`12-Agentic-AI/02-Tool-Calling.md`](12-Agentic-AI/03-Tool-Calling.md) | Function calling, guardrails |
| 🚀 DevOps Use Cases | [`12-Agentic-AI/03-DevOps-Use-Cases.md`](12-Agentic-AI/04-DevOps-Use-Cases.md) | Auto-remediation, IaC generation |
| ❓ Interview Questions | [`12-Agentic-AI/04-Interview-Questions.md`](12-Agentic-AI/05-Interview-Questions.md) | AI agent Q&A |
| 🐍 Step 1 — Python | [`12-Agentic-AI/05-Python-for-Agentic-AI.md`](12-Agentic-AI/06-Python-for-Agentic-AI.md) | Python skills for building agents |
| 🔗 Step 2 — Chains/RAG | [`12-Agentic-AI/06-LLM-Chains-n8n-RAG.md`](12-Agentic-AI/07-LLM-Chains-n8n-RAG.md) | LLM chains, n8n, vector DBs, RAG |
| 🤖 Step 3 — Frameworks | [`12-Agentic-AI/07-Agent-Frameworks.md`](12-Agentic-AI/08-Agent-Frameworks.md) | LangChain, LangGraph, CrewAI deep dive |
| 🔌 Step 4 — MCP & A2A | [`12-Agentic-AI/08-MCP-and-A2A.md`](12-Agentic-AI/09-MCP-and-A2A.md) | MCP protocol, A2A protocol |
| 🏆 Finish — Governance | [`12-Agentic-AI/09-AI-Governance-Cost-Observability.md`](12-Agentic-AI/10-AI-Governance-Cost-Observability.md) | Guardrails, cost, LangSmith observability |

---

## 🌿 13 — Git

> Git fundamentals, platform comparison, repository setup and the full PR workflow for DevOps teams.

| Topic | File | Description |
|-------|------|-------------|
| 🌐 Introduction | [`13-Git/01-Introduction.md`](13-Git/01-Introduction.md) | Git vs GitHub/GitLab/Azure Repos/Bitbucket |
| 📁 Repository Setup | [`13-Git/02-Repository-Setup.md`](13-Git/02-Repository-Setup.md) | Repo creation, .gitignore, branch protection, pre-commit hooks |
| 🔄 Core Workflow | [`13-Git/03-Core-Workflow.md`](13-Git/05-Core-Workflow.md) | Commit, Push, Pull Request, Code Review, branching strategies |
| 🖥️ Commands Reference | [`13-Git/04-Commands-Reference.md`](13-Git/04-Commands-Reference.md) | Every Git & GitHub CLI (`gh`) command — what it does, effects, before/after |

---

## 🔐 14 — Security Scanning

> IaC and secrets security scanning tools for production-grade Terraform pipelines.

| Topic | File | Description |
|-------|------|-------------|
| 🔧 Terraform Built-ins | [`14-Security-Scanning/01-Terraform-Built-ins.md`](14-Security-Scanning/01-Terraform-Built-ins.md) | terraform fmt & validate |
| 🔍 TFLint | [`14-Security-Scanning/02-TFLint.md`](14-Security-Scanning/02-TFLint.md) | Linting & provider-specific checks |
| 🛡️ Tfsec | [`14-Security-Scanning/03-Tfsec.md`](14-Security-Scanning/03-Tfsec.md) | Static security analysis for Terraform |
| ✅ Checkov | [`14-Security-Scanning/04-Checkov.md`](14-Security-Scanning/04-Checkov.md) | Policy-as-code & compliance scanning |
| 🔬 Trivy | [`14-Security-Scanning/05-Trivy.md`](14-Security-Scanning/05-Trivy.md) | All-in-one vulnerability scanner |
| 🐷 TruffleHog | [`14-Security-Scanning/06-TruffleHog.md`](14-Security-Scanning/06-TruffleHog.md) | Verified secrets scanning |
| 🔑 Gitleaks | [`14-Security-Scanning/07-Gitleaks.md`](14-Security-Scanning/07-Gitleaks.md) | Fast secrets detection & pre-commit hooks |

---

## 💰 15 — Cost & Governance

> Azure cost management, tagging strategy, naming conventions, RBAC and OpenCost for Kubernetes.

| Topic | File | Description |
|-------|------|-------------|
| 📊 OpenCost | [`15-Cost-Governance/01-OpenCost.md`](15-Cost-Governance/01-OpenCost.md) | Kubernetes cost monitoring on AKS |
| 🏷️ Resource Tagging | [`15-Cost-Governance/02-Resource-Tagging.md`](15-Cost-Governance/02-Resource-Tagging.md) | Azure tagging strategy & policy enforcement |
| 📛 Naming Convention | [`15-Cost-Governance/03-Naming-Convention.md`](15-Cost-Governance/03-Naming-Convention.md) | CAF-aligned naming patterns & Terraform locals |
| 💡 Cost Optimization | [`15-Cost-Governance/04-Cost-Optimization.md`](15-Cost-Governance/04-Cost-Optimization.md) | Reserved instances, spot VMs, AKS & storage savings |
| 🔐 Least Privilege RBAC | [`15-Cost-Governance/05-Least-Privilege-RBAC.md`](15-Cost-Governance/05-Least-Privilege-RBAC.md) | RBAC scopes, Managed Identity, PIM, OIDC |

---

## ❓ 16 — DI Interview Questions

> A comprehensive collection of DevOps interview questions gathered from real company interviews and organized by topic, courtesy of DevOps Insiders.

### Collections
| Topic | Path | Description |
|-------|------|-------------|
| 🏢 Companies | [`16-DI-Interview-Questions/companies`](16-DI-Interview-Questions/companies) | Questions asked by specific companies |
| 📚 Topics | [`16-DI-Interview-Questions/topics`](16-DI-Interview-Questions/topics) | Questions categorized by technology/topic |
| 📖 README | [`16-DI-Interview-Questions/README.md`](16-DI-Interview-Questions/README.md) | Original repository documentation |

---

## ⚡ Quick Reference — Cheat Sheets

> Jump directly to the most-used reference documents.

| Cheat Sheet | Link | Coverage |
|-------------|------|----------|
| 🏗️ Terraform CLI | [`01-Terraform/Cheat-Sheet.md`](01-Terraform/19-Cheat-Sheet.md) | init, plan, apply, import, state |
| ☁️ Azure CLI | [`02-Azure/Cheat-Sheet.md`](02-Azure/34-Cheat-Sheet.md) | az group, vm, network, aks |
| 🐧 Linux Commands | [`05-Linux/Cheat-Sheet.md`](05-Linux/02-Cheat-Sheet.md) | find, grep, awk, sed, systemctl |
| 🔑 RBAC Quick Ref | [`02-Azure/RBAC.md`](02-Azure/35-RBAC.md) | Built-in roles, scope hierarchy |
| 🛡️ NSG Rules | [`02-Azure/NSG.md`](02-Azure/36-NSG.md) | Priority, allow/deny patterns |
| 📜 KQL Queries | [`02-Azure/Log-Analytics.md`](02-Azure/37-Log-Analytics.md) | Top KQL patterns for ops |
| 🌿 Git Workflow | [`13-Git/03-Core-Workflow.md`](13-Git/05-Core-Workflow.md) | Commit, PR, review commands |
| 🔁 Terraform Loops | [`01-Terraform/13-Loops-Conditionals.md`](01-Terraform/20-Loops-Conditionals.md) | count, for_each, dynamic blocks |

---

## 🗺️ Learning Path

> Recommended study order for building from foundations to enterprise-grade expertise.

### Phase 1 — Foundations *(Weeks 1–2)*
| Step | Topics |
|------|--------|
| 1 | `05-Linux` — OS Fundamentals, Core Commands, Permissions |
| 2 | `02-Azure` — Azure Fundamentals, Architecture Fundamentals |
| 3 | `01-Terraform` — Introduction, Installation, Providers, Resources |

### Phase 2 — Core Skills *(Weeks 3–4)*
| Step | Topics |
|------|--------|
| 4 | `01-Terraform` — Variables, Locals, Outputs, State Management, Remote Backend |
| 5 | `02-Azure` — VNet, Subnets, NSG, Route Tables |
| 6 | `02-Azure` — RBAC, Managed Identity, Key Vault |
| 7 | `13-Git` — Git workflow, PRs, branching strategies |

### Phase 3 — Advanced IaC & Automation *(Weeks 5–6)*
| Step | Topics |
|------|--------|
| 8 | `01-Terraform` — Modules, Workspaces, Loops, Lifecycle, Best Practices |
| 9 | `04-CI-CD` — Azure DevOps, GitHub Actions, Terraform Pipeline |
| 10 | `14-Security-Scanning` — TFLint, tfsec, Checkov, Gitleaks |

### Phase 4 — Enterprise Architecture *(Weeks 7–8)*
| Step | Topics |
|------|--------|
| 11 | `03-Landing-Zone` — CAF Overview, Enterprise-Scale, Management Groups |
| 12 | `06-Architecture-Patterns` — Hub-Spoke, Zero-Trust, Multi-Region, DR |
| 13 | `15-Cost-Governance` — Tagging, Naming, Cost Optimization, RBAC |
| 14 | `08-Real-World-Projects` — All project implementations |

### Phase 5 — Interview & Certification Prep *(Weeks 9–10)*
| Step | Topics |
|------|--------|
| 15 | `07-Interview-Prep` — All domain Q&A files |
| 16 | [`07-Interview-Prep/Scenario-Based.md`](07-Interview-Prep/10-Scenario-Based.md) — Whiteboard scenarios |
| 17 | `09-Decision-Logs` — Review ADRs to articulate architectural decisions |
| 18 | All `Cheat-Sheet` files — Final revision sweep |

---

## 📊 Vault Stats

| Metric | Value |
|--------|-------|
| 📁 Total Sections | 16 |
| 📄 Total Notes | 174+ |
| 🏗️ Terraform Topics | 20 + 9 Resource Library |
| ☁️ Azure Services Covered | 33 |
| 🏢 Landing Zone Topics | 18 |
| 🔄 CI/CD Topics | 8 |
| 🐧 Linux Topics | 13 |
| 🎯 Interview Prep Domains | 9 |
| 🔨 Real-World Projects | 5 |
| 📋 Architecture Decision Records | 4 |
| 🤖 Agentic AI Topics | 10 |
| 🔐 Security Scanning Tools | 7 |
| 🌿 Git Topics | 4 |
| 💰 Cost & Governance Topics | 5 |

---

## 🔗 External Resources

| Resource | URL | Relevance |
|----------|-----|-----------|
| Azure Landing Zones Docs | [aka.ms/alz](https://aka.ms/alz) | ALZ reference architecture |
| Terraform AzureRM Registry | [registry.terraform.io](https://registry.terraform.io/providers/hashicorp/azurerm/latest) | Provider docs |
| CAF Documentation | [learn.microsoft.com/azure/cloud-adoption-framework](https://learn.microsoft.com/azure/cloud-adoption-framework/) | Full CAF guidance |
| Azure Architecture Center | [learn.microsoft.com/azure/architecture](https://learn.microsoft.com/azure/architecture/) | Reference patterns |
| Microsoft Learn | [learn.microsoft.com](https://learn.microsoft.com) | AZ-104, AZ-305 paths |
| Terraform Best Practices | [developer.hashicorp.com](https://developer.hashicorp.com/terraform/language) | Official HCL docs |
| ALZ Terraform Module | [github.com/Azure/terraform-azurerm-caf-enterprise-scale](https://github.com/Azure/terraform-azurerm-caf-enterprise-scale) | CAF ALZ Terraform |
| OpenCost | [opencost.io](https://www.opencost.io) | Kubernetes cost monitoring |

---

<div align="center">

**DevOps Insiders — Batch 18** &nbsp;|&nbsp; Built with ❤️ in Obsidian &nbsp;|&nbsp; Updated August 2026

*"The best time to build a knowledge system was when you started. The second best time is now."*

</div>

