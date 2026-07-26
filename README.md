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

> **Vault Engine:** [Obsidian](https://obsidian.md) | **Program:** DevOps Insiders Batch 18 | **Last Updated:** July 2026

---

## 📚 Table of Contents

| # | Section | Description | Notes |
|---|---------|-------------|-------|
| 🏗️ | [01 — Terraform](#-01--terraform) | IaC from zero to advanced | HCL, State, Modules, Workspaces |
| ☁️ | [02 — Azure](#️-02--azure) | Core Azure services & networking | AKS, VNet, RBAC, Key Vault |
| 🏢 | [03 — Landing Zone](#-03--landing-zone) | Azure Landing Zone & CAF | Enterprise-Scale, Governance |
| 🔄 | [04 — CI/CD](#-04--cicd) | Pipelines & GitOps automation | Azure DevOps, GitHub Actions |
| 🐧 | [05 — Linux](#-05--linux) | Linux mastery for DevOps | Commands, Bash, Networking |
| 🏛️ | [06 — Architecture Patterns](#️-06--architecture-patterns) | Enterprise design patterns | Hub-Spoke, Zero-Trust, DR |
| 🎯 | [07 — Interview Prep](#-07--interview-prep) | Curated Q&A by domain | Scenario-based, Security |
| 🔨 | [08 — Real-World Projects](#-08--real-world-projects) | Full project implementations | AKS Platform, Secure Hub-Spoke |
| 📋 | [09 — Decision Logs](#-09--decision-logs) | Architecture Decision Records | ADRs with rationale |
| 🗺️ | [10 — CAF Mapping](#️-10--caf-mapping) | Cloud Adoption Framework map | Workloads ↔ CAF pillars |
| 📅 | [11 — Weekly Learning](#-11--weekly-learning) | Progress tracker & goals | Weekly reviews |
| 🤖 | [12 — Agentic AI](#-12--agentic-ai) | AI in DevOps engineering | Tool calling, automation |
| 🔐 | [14 — Security Scanning](#-14--security-scanning) | IaC & secrets security scanning | TFLint, tfsec, Checkov, Gitleaks |

---

## 🏗️ 01 — Terraform

> Infrastructure as Code fundamentals through advanced enterprise patterns using HashiCorp Terraform.

| Topic                   | File                                  | Description                           |
| ----------------------- | ------------------------------------- | ------------------------------------- |
| 📖 Introduction         | [`01-Terraform/01-Introduction.md`](01-Terraform/01-Introduction.md)        | What is Terraform, why IaC            |
| ⚙️ Installation         | [`01-Terraform/02-Installation.md`](01-Terraform/02-Installation.md)        | Install, configure, tfenv             |
| 🔌 Providers            | [`01-Terraform/03-Providers.md`](01-Terraform/03-Providers.md)           | AzureRM, version locking              |
| 🧱 Resources            | [`01-Terraform/04-Resources.md`](01-Terraform/04-Resources.md)           | Resource blocks, meta-args            |
| 📥 Variables            | [`01-Terraform/05-Variables.md`](01-Terraform/05-Variables.md)           | Input vars, tfvars, env vars          |
| 🔧 Locals               | [`01-Terraform/06-Locals.md`](01-Terraform/06-Locals.md)              | Local values, expressions             |
| 📤 Outputs              | [`01-Terraform/07-Outputs.md`](01-Terraform/07-Outputs.md)             | Output blocks, sensitive values       |
| 💾 State Management     | [`01-Terraform/08-State-Management.md`](01-Terraform/08-State-Management.md)    | State file, locking, drift            |
| 🌐 Remote Backend       | [`01-Terraform/09-Remote-Backend.md`](01-Terraform/09-Remote-Backend.md)      | Azure Blob, state locking             |
| 📦 Modules              | [`01-Terraform/10-Modules.md`](01-Terraform/10-Modules.md)             | Module structure, registry            |
| 🌍 Workspaces           | [`01-Terraform/11-Workspaces.md`](01-Terraform/11-Workspaces.md)          | Multi-env with workspaces             |
| 🔍 Data Sources         | [`01-Terraform/12-Data-Sources.md`](01-Terraform/12-Data-Sources.md)        | Querying existing resources           |
| 🔁 Loops & Conditionals | [`01-Terraform/13-Loops-Conditionals.md`](01-Terraform/13-Loops-Conditionals.md)  | count, for_each, dynamic              |
| ♻️ Lifecycle            | [`01-Terraform/14-Lifecycle.md`](01-Terraform/14-Lifecycle.md)           | create_before_destroy, ignore_changes |
| ⭐ Best Practices        | [`01-Terraform/15-Best-Practices.md`](01-Terraform/15-Best-Practices.md)      | Naming, structure, security           |
| 📝 Cheat Sheet          | [`01-Terraform/Cheat-Sheet.md`](01-Terraform/Cheat-Sheet.md)         | Quick command reference               |
| ❓ Interview Questions   | [`01-Terraform/Interview-Questions.md`](01-Terraform/Interview-Questions.md) | Top interview Q&A                     |

---

## ☁️ 02 — Azure

> Core Azure services, networking fundamentals, and identity — the building blocks of every Azure deployment.

| Topic | File | Description |
|-------|------|-------------|
| 🧩 Azure Fundamentals | [`02-Azure/Azure-Fundamentals.md`](02-Azure/Azure-Fundamentals.md) | Regions, Resource Manager |
| 🏗️ Architecture Fundamentals | [`02-Azure/Azure-Architecture-Fundamentals.md`](02-Azure/Azure-Architecture-Fundamentals.md) | Availability Zones, pairs |
| 🌐 VNet | [`02-Azure/VNet.md`](02-Azure/VNet.md) | Virtual Networks, peering |
| 🔀 Subnets | [`02-Azure/Subnets.md`](02-Azure/Subnets.md) | Subnet design, delegation |
| 🛡️ NSG | [`02-Azure/NSG.md`](02-Azure/NSG.md) | Network Security Groups |
| 🗺️ Route Tables | [`02-Azure/Route-Tables.md`](02-Azure/Route-Tables.md) | UDR, BGP, forced tunneling |
| 🔑 RBAC | [`02-Azure/RBAC.md`](02-Azure/RBAC.md) | Roles, assignments, custom roles |
| 🪪 Managed Identity | [`02-Azure/Managed-Identity.md`](02-Azure/Managed-Identity.md) | System/User assigned MI |
| 🔒 Key Vault | [`02-Azure/Key-Vault.md`](02-Azure/Key-Vault.md) | Secrets, certs, access policies |
| 💾 Storage Account | [`02-Azure/Storage-Account.md`](02-Azure/Storage-Account.md) | Blob, tiers, lifecycle |
| 📊 Monitor | [`02-Azure/Monitor.md`](02-Azure/Monitor.md) | Metrics, Alerts, Dashboards |
| 📋 Log Analytics | [`02-Azure/Log-Analytics.md`](02-Azure/Log-Analytics.md) | Workspace, KQL queries |
| ☸️ AKS | [`02-Azure/AKS.md`](02-Azure/AKS.md) | Azure Kubernetes Service |
| 📁 Resource Groups | [`02-Azure/Resource-Groups.md`](02-Azure/Resource-Groups.md) | RG design patterns |
| 🖥️ VM | [`02-Azure/VM.md`](02-Azure/VM.md) | Virtual Machines, scale sets |
| ⚖️ VMSS | [`02-Azure/VMSS.md`](02-Azure/VMSS.md) | Virtual Machine Scale Sets |
| 🚪 Bastion | [`02-Azure/Bastion.md`](02-Azure/Bastion.md) | Secure RDP/SSH access |
| 🔌 NIC | [`02-Azure/NIC.md`](02-Azure/NIC.md) | Network Interfaces, IP forwarding |
| 🛡️ App Gateway | [`02-Azure/App-Gateway.md`](02-Azure/App-Gateway.md) | Layer 7 routing, WAF, AGIC |
| 🌍 Front Door | [`02-Azure/Front-Door.md`](02-Azure/Front-Door.md) | Global CDN, Edge WAF |
| 🔀 Traffic Manager | [`02-Azure/Traffic-Manager.md`](02-Azure/Traffic-Manager.md) | DNS-based global routing |
| ⚖️ Load Balancer | [`02-Azure/Load-Balancer.md`](02-Azure/Load-Balancer.md) | Layer 4 TCP/UDP load balancer |
| 🔗 Private Link | [`02-Azure/Private-Link.md`](02-Azure/Private-Link.md) | Private Endpoints, DNS |
| 🚢 ACR | [`02-Azure/ACR.md`](02-Azure/ACR.md) | Azure Container Registry |
| 🚇 VNet Gateway | [`02-Azure/Virtual-Network-Gateway.md`](02-Azure/Virtual-Network-Gateway.md) | VPN & ExpressRoute |
| 🛡️ Azure Policy | [`02-Azure/Azure-Policy.md`](02-Azure/Azure-Policy.md) | Governance & Compliance |
| 🔐 Entra ID | [`02-Azure/Entra-ID.md`](02-Azure/Entra-ID.md) | Identity and Access Management |
| 💾 Azure Backup | [`02-Azure/Azure-Backup.md`](02-Azure/Azure-Backup.md) | VM, SQL, Files backup |
| 🌩️ Azure DR | [`02-Azure/Azure-DR.md`](02-Azure/Azure-DR.md) | Site Recovery, Cross-Region DR |
| 🛡️ Azure Security | [`02-Azure/Azure-Security.md`](02-Azure/Azure-Security.md) | Defender for Cloud, CSPM |
| 📝 Cheat Sheet | [`02-Azure/Cheat-Sheet.md`](02-Azure/Cheat-Sheet.md) | Azure CLI quick reference |
| ❓ Interview Questions | [`02-Azure/Interview-Questions.md`](02-Azure/Interview-Questions.md) | Core Azure Q&A |

---

## 🏢 03 — Landing Zone

> Azure Landing Zone design, Cloud Adoption Framework (CAF), and enterprise-scale governance patterns.

| Topic | File | Description |
|-------|------|-------------|
| 📖 Introduction | [`03-Landing-Zone/Introduction.md`](03-Landing-Zone/Introduction.md) | What is a Landing Zone |
| 🗺️ CAF Overview | [`03-Landing-Zone/CAF-Overview.md`](03-Landing-Zone/CAF-Overview.md) | CAF methodology, pillars |
| 🏛️ Enterprise Scale | [`03-Landing-Zone/Enterprise-Scale.md`](03-Landing-Zone/Enterprise-Scale.md) | ALZ reference architecture |
| 🏗️ Architecture | [`03-Landing-Zone/Architecture.md`](03-Landing-Zone/Architecture.md) | Design areas, components |
| 🗂️ Management Groups | [`03-Landing-Zone/Management-Groups.md`](03-Landing-Zone/Management-Groups.md) | MG hierarchy design |
| 📋 Subscription Strategy | [`03-Landing-Zone/Subscription-Strategy.md`](03-Landing-Zone/Subscription-Strategy.md) | Subscription models |
| 🏷️ Resource Organization | [`03-Landing-Zone/Resource-Organization.md`](03-Landing-Zone/Resource-Organization.md) | Naming, tagging standards |
| 🆔 Identity & Access | [`03-Landing-Zone/Identity-and-Access-Management.md`](03-Landing-Zone/Identity-and-Access-Management.md) | Entra ID, PIM, RBAC |
| 🌐 Network Topology | [`03-Landing-Zone/Network-Topology-and-Connectivity.md`](03-Landing-Zone/Network-Topology-and-Connectivity.md) | Hub-Spoke, WAN |
| 🛡️ Security | [`03-Landing-Zone/Security.md`](03-Landing-Zone/Security.md) | Defender, Sentinel, controls |
| 📜 Policies | [`03-Landing-Zone/Policies.md`](03-Landing-Zone/Policies.md) | Azure Policy, initiatives |
| 🏛️ Governance | [`03-Landing-Zone/Governance.md`](03-Landing-Zone/Governance.md) | Compliance, cost, tagging |
| 📊 Management | [`03-Landing-Zone/Management.md`](03-Landing-Zone/Management.md) | Ops management, patching |
| 👁️ Monitoring | [`03-Landing-Zone/Monitoring.md`](03-Landing-Zone/Monitoring.md) | ALZ monitoring baseline |
| 🤖 Platform Automation | [`03-Landing-Zone/Platform-Automation-and-DevOps.md`](03-Landing-Zone/Platform-Automation-and-DevOps.md) | IaC-driven LZ deployment |
| 💰 Billing & Entra | [`03-Landing-Zone/Azure-Billing-and-Entra-Tenant.md`](03-Landing-Zone/Azure-Billing-and-Entra-Tenant.md) | Tenant, EA, MCA setup |
| ❓ Interview Questions | [`03-Landing-Zone/Interview-Questions.md`](03-Landing-Zone/Interview-Questions.md) | Landing Zone Q&A |

---

## 🔄 04 — CI/CD

> Pipeline design, GitOps workflows, and deployment automation for Azure-native and Kubernetes workloads.

| Topic | File | Description |
|-------|------|-------------|
| 🔵 Azure DevOps | [`04-CI-CD/Azure-DevOps.md`](04-CI-CD/Azure-DevOps.md) | Pipelines, repos, boards |
| 🐙 GitHub Actions | [`04-CI-CD/GitHub-Actions.md`](04-CI-CD/GitHub-Actions.md) | Workflows, OIDC, runners |
| ☸️ AKS Deployment | [`04-CI-CD/AKS-Deployment.md`](04-CI-CD/AKS-Deployment.md) | Helm, manifests, rollouts |
| 🏗️ Terraform Pipeline | [`04-CI-CD/Terraform-Pipeline.md`](04-CI-CD/Terraform-Pipeline.md) | Plan/Apply gates, OIDC |
| 🌿 Branching Strategies | [`04-CI-CD/Branching-Strategies.md`](04-CI-CD/Branching-Strategies.md) | GitFlow, trunk-based dev |
| 🚀 Release Strategy | [`04-CI-CD/Release-Strategy.md`](04-CI-CD/Release-Strategy.md) | Blue-Green, Canary, Ring |
| 🔁 GitOps Basics | [`04-CI-CD/GitOps-Basics.md`](04-CI-CD/GitOps-Basics.md) | ArgoCD, Flux fundamentals |

---

## 🐧 05 — Linux

> Linux fundamentals, system administration, and Bash scripting for DevOps practitioners.

| Topic | File | Description |
|-------|------|-------------|
| 🖥️ OS Fundamentals | [`05-Linux/00-OS-Fundamentals/`](05-Linux/00-OS-Fundamentals) | Kernel, processes, filesystems |
| ⌨️ Core Commands | [`05-Linux/01-Core-Commands/`](05-Linux/01-Core-Commands) | Essential CLI commands |
| 🔐 Permissions | [`05-Linux/02-Permissions/`](05-Linux/02-Permissions) | chmod, chown, ACLs, sudo |
| 🌐 Networking | [`05-Linux/03-Networking/`](05-Linux/03-Networking) | ip, ss, netstat, firewalld |
| 🔧 SysAdmin | [`05-Linux/04-SysAdmin/`](05-Linux/04-SysAdmin) | systemd, cron, logs, users |
| 📜 Bash Scripting | [`05-Linux/05-Bash-Scripting/`](05-Linux/05-Bash-Scripting) | Scripts, functions, automation |
| 📝 Cheat Sheet | [`05-Linux/Cheat-Sheet.md`](05-Linux/Cheat-Sheet.md) | One-liner quick reference |

---

## 🏛️ 06 — Architecture Patterns

> Enterprise cloud architecture patterns applied to Azure workloads.

| Topic | File | Description |
|-------|------|-------------|
| 🕸️ Hub-Spoke | [`06-Architecture-Patterns/Hub-Spoke.md`](06-Architecture-Patterns/Hub-Spoke.md) | Hub-Spoke topology |
| 🌍 Multi-Region | [`06-Architecture-Patterns/Multi-Region.md`](06-Architecture-Patterns/Multi-Region.md) | Active-Active, geo-redundancy |
| 🔥 DR Strategy | [`06-Architecture-Patterns/DR-Strategy.md`](06-Architecture-Patterns/DR-Strategy.md) | RPO, RTO, failover design |
| 🔒 Zero Trust | [`06-Architecture-Patterns/Zero-Trust.md`](06-Architecture-Patterns/Zero-Trust.md) | Zero Trust architecture |
| 🏢 Enterprise Architecture | [`06-Architecture-Patterns/Enterprise-Architecture.md`](06-Architecture-Patterns/Enterprise-Architecture.md) | TOGAF, architecture views |
| 🤝 Shared Services | [`06-Architecture-Patterns/Shared-Services.md`](06-Architecture-Patterns/Shared-Services.md) | Centralized service design |

---

## 🔐 14 — Security Scanning

> IaC and secrets security scanning tools for production-grade Terraform pipelines.

| Topic | File | Description |
|-------|------|-------------|
| 🔧 Terraform Built-ins | [`14-Security-Scanning/01-Terraform-Built-ins.md`](14-Security-Scanning/01-Terraform-Built-ins.md) | terraform fmt & validate |
| 🔍 TFLint | [`14-Security-Scanning/02-TFLint.md`](14-Security-Scanning/02-TFLint.md) | Linting & provider-specific checks |
| 🛡️ tfsec | [`14-Security-Scanning/03-Tfsec.md`](14-Security-Scanning/03-Tfsec.md) | Static security analysis for Terraform |
| ✅ Checkov | [`14-Security-Scanning/04-Checkov.md`](14-Security-Scanning/04-Checkov.md) | Policy-as-code & compliance scanning |
| 🔬 Trivy | [`14-Security-Scanning/05-Trivy.md`](14-Security-Scanning/05-Trivy.md) | All-in-one vulnerability scanner |
| 🐷 TruffleHog | [`14-Security-Scanning/06-TruffleHog.md`](14-Security-Scanning/06-TruffleHog.md) | Verified secrets scanning |
| 🔑 Gitleaks | [`14-Security-Scanning/07-Gitleaks.md`](14-Security-Scanning/07-Gitleaks.md) | Fast secrets detection & pre-commit hooks |

---

## 🎯 07 — Interview Prep

> Domain-specific interview questions and scenario-based walkthroughs for Azure/DevOps engineering roles.

| Topic             | File                                  | Description                 |
| ----------------- | ------------------------------------- | --------------------------- |
| ☁️ Azure          | [`07-Interview-Prep/Azure.md`](07-Interview-Prep/Azure.md)          | Core Azure Q&A              |
| 🏢 Landing Zone   | [`07-Interview-Prep/Landing-Zone.md`](07-Interview-Prep/Landing-Zone.md)   | LZ design questions         |
| 🐧 Linux          | [`07-Interview-Prep/Linux.md`](07-Interview-Prep/Linux.md)          | Linux admin Q&A             |
| 🌐 Networking     | [`07-Interview-Prep/Networking.md`](07-Interview-Prep/Networking.md)     | Azure networking deep-dives |
| 🎭 Scenario-Based | [`07-Interview-Prep/Scenario-Based.md`](07-Interview-Prep/Scenario-Based.md) | "What would you do if..."   |
| 🛡️ Security      | [`07-Interview-Prep/Security.md`](07-Interview-Prep/Security.md)       | Security posture Q&A        |
| 🏗️ Terraform     | [`07-Interview-Prep/Terraform.md`](07-Interview-Prep/Terraform.md)      | IaC interview scenarios     |

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
| 🕸️ Hub-Spoke | [`09-Decision-Logs/Hub-Spoke.md`](09-Decision-Logs/Hub-Spoke.md) | Why Hub-Spoke over flat VNet |
| 👥 RBAC Model | [`09-Decision-Logs/RBAC-Model.md`](09-Decision-Logs/RBAC-Model.md) | Custom vs built-in roles |
| 💾 Remote State | [`09-Decision-Logs/Remote-State.md`](09-Decision-Logs/Remote-State.md) | Azure Blob backend design |
| 🔒 Security Controls | [`09-Decision-Logs/Security-Controls.md`](09-Decision-Logs/Security-Controls.md) | Defender + Sentinel vs 3rd party |

---

## 🗺️ 10 — CAF Mapping

> Maps all vault topics to Cloud Adoption Framework pillars across strategy, govern, manage, and organize phases.

📄 `10-CAF-Mapping/` — Cross-references workloads, services, and patterns against the six CAF methodology phases.

---

## 📅 11 — Weekly Learning

> Weekly study logs, goal tracking, and progress snapshots throughout the Batch 18 program.

📄 `11-Weekly-Learning/` — Weekly entries with topics covered, blockers, and upcoming focus areas.

---

## 🤖 12 — Agentic AI

> The future of DevOps: Autonomous agents, tool calling, and LLM orchestration.

| Topic | File | Description |
|-------|------|-------------|
| 🗺️ Roadmap | [`12-Agentic-AI/00-Roadmap.md`](12-Agentic-AI/00-Roadmap.md) | Full Agentic AI for DevOps learning roadmap |
| 🧠 Introduction | [`12-Agentic-AI/01-Introduction.md`](12-Agentic-AI/01-Introduction.md) | Agents vs Gen AI, ReAct loop |
| 🛠️ Tool Calling | [`12-Agentic-AI/02-Tool-Calling.md`](12-Agentic-AI/02-Tool-Calling.md) | Function calling, guardrails |
| 🚀 DevOps Use Cases | [`12-Agentic-AI/03-DevOps-Use-Cases.md`](12-Agentic-AI/03-DevOps-Use-Cases.md) | Auto-remediation, IaC generation |
| ❓ Interview Questions | [`12-Agentic-AI/04-Interview-Questions.md`](12-Agentic-AI/04-Interview-Questions.md) | AI agent Q&A |
| 🐍 Step 1 — Python | [`12-Agentic-AI/05-Python-for-Agentic-AI.md`](12-Agentic-AI/05-Python-for-Agentic-AI.md) | Python skills for building agents |
| 🔗 Step 2 — Chains/RAG | [`12-Agentic-AI/06-LLM-Chains-n8n-RAG.md`](12-Agentic-AI/06-LLM-Chains-n8n-RAG.md) | LLM chains, n8n, vector DBs, RAG |
| 🤖 Step 3 — Frameworks | [`12-Agentic-AI/07-Agent-Frameworks.md`](12-Agentic-AI/07-Agent-Frameworks.md) | LangChain, LangGraph, CrewAI deep dive |
| 🔌 Step 4 — MCP & A2A | [`12-Agentic-AI/08-MCP-and-A2A.md`](12-Agentic-AI/08-MCP-and-A2A.md) | MCP protocol, A2A protocol |
| 🏆 Finish — Governance | [`12-Agentic-AI/09-AI-Governance-Cost-Observability.md`](12-Agentic-AI/09-AI-Governance-Cost-Observability.md) | Guardrails, cost, LangSmith observability |

---

## ⚡ Quick Reference — Cheat Sheets

> Jump directly to the most-used reference documents.

| Cheat Sheet | Link | Coverage |
|-------------|------|----------|
| 🏗️ Terraform CLI | [`01-Terraform/Cheat-Sheet.md`](01-Terraform/Cheat-Sheet.md) | init, plan, apply, import, state |
| ☁️ Azure CLI | [`02-Azure/Cheat-Sheet.md`](02-Azure/Cheat-Sheet.md) | az group, vm, network, aks |
| 🐧 Linux Commands | [`05-Linux/Cheat-Sheet.md`](05-Linux/Cheat-Sheet.md) | find, grep, awk, sed, systemctl |
| 🔑 RBAC Quick Ref | [`02-Azure/RBAC.md`](02-Azure/RBAC.md) | Built-in roles, scope hierarchy |
| 🛡️ NSG Rules | [`02-Azure/NSG.md`](02-Azure/NSG.md) | Priority, allow/deny patterns |
| 📜 KQL Queries | [`02-Azure/Log-Analytics.md`](02-Azure/Log-Analytics.md) | Top KQL patterns for ops |
| 🌿 Git Branching | [`04-CI-CD/Branching-Strategies.md`](04-CI-CD/Branching-Strategies.md) | GitFlow vs trunk-based |
| 🔁 Terraform Loops | [`01-Terraform/Loops-Conditionals.md`](01-Terraform/Loops-Conditionals.md) | count, for_each, dynamic blocks |

---

## 🗺️ Learning Path

> Recommended study order for building from foundations to enterprise-grade expertise.

### Phase 1 — Foundations *(Weeks 1–2)*

```
Linux Fundamentals  →  Azure Fundamentals  →  Terraform Introduction & Installation
```

| Step | Topics                                                            |
| ---- | ----------------------------------------------------------------- |
| 1    | `05-Linux` — OS Fundamentals, Core Commands, Permissions          |
| 2    | `02-Azure` — Azure Fundamentals, Architecture Fundamentals        |
| 3    | `01-Terraform` — Introduction, Installation, Providers, Resources |

---

### Phase 2 — Core Skills *(Weeks 3–4)*

```
Terraform Deep Dive  →  Azure Networking  →  Identity & Security
```

| Step | Topics |
|------|--------|
| 4 | `01-Terraform` — Variables, Locals, Outputs, State Management, Remote Backend |
| 5 | `02-Azure` — VNet, Subnets, NSG, Route Tables |
| 6 | `02-Azure` — RBAC, Managed Identity, Key Vault |

---

### Phase 3 — Advanced IaC & Automation *(Weeks 5–6)*

```
Terraform Modules & Patterns  →  CI/CD Pipelines  →  Linux SysAdmin
```

| Step | Topics |
|------|--------|
| 7 | `01-Terraform` — Modules, Workspaces, Loops, Lifecycle, Best Practices |
| 8 | `04-CI-CD` — Azure DevOps, GitHub Actions, Terraform Pipeline |
| 9 | `05-Linux` — Bash Scripting, SysAdmin, Networking |

---

### Phase 4 — Enterprise Architecture *(Weeks 7–8)*

```
Landing Zone Design  →  Architecture Patterns  →  Real-World Projects
```

| Step | Topics |
|------|--------|
| 10 | `03-Landing-Zone` — Introduction → CAF Overview → Enterprise-Scale |
| 11 | `03-Landing-Zone` — Management Groups, Subscription Strategy, Governance, Policies |
| 12 | `06-Architecture-Patterns` — Hub-Spoke, Zero-Trust, Multi-Region, DR |
| 13 | `08-Real-World-Projects` — All four project implementations |

---

### Phase 5 — Interview & Certification Prep *(Weeks 9–10)*

```
Interview Q&A Review  →  Scenario Practice  →  Mock Interviews
```

| Step | Topics |
|------|--------|
| 14 | `07-Interview-Prep` — All domain Q&A files |
| 15 | [`07-Interview-Prep/Scenario-Based.md`](07-Interview-Prep/Scenario-Based.md) — Whiteboard & scenario walkthroughs |
| 16 | `09-Decision-Logs` — Review ADRs to articulate architectural decisions |
| 17 | All `Cheat-Sheet` files — Final revision sweep |

---

## 🎯 Current Focus

> Actively being developed and studied — as of **July 2026**.

| Status | Area | Notes |
|--------|------|-------|
| 🔴 In Progress | `03-Landing-Zone` | Enterprise-Scale, Governance, Policies deep-dive |
| 🔴 In Progress | `04-CI-CD` | Terraform Pipeline with OIDC, GitHub Actions reusable workflows |
| 🟡 Reviewing | `01-Terraform` | Modules pattern refinement, Workspaces vs. directory structure |
| 🟡 Reviewing | `07-Interview-Prep` | Adding scenario-based questions from Batch 18 sessions |
| 🟢 Complete | `02-Azure` | 17-Point Enterprise Architect Master Format deployed! |
| 🟢 Complete | `05-Linux` | Commands, permissions, Bash scripting |
| ⚪ Queued | `06-Architecture-Patterns` | Multi-Region and DR Strategy |
| ⚪ Queued | `08-Real-World-Projects` | Secure Hub-Spoke implementation |

---

## 🛠️ Vault Setup & Tips

### Recommended Obsidian Plugins

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Query notes as a database — generate dynamic ToCs and status boards |
| **Templater** | Consistent frontmatter and note structure across all files |
| **Excalidraw** | Architecture diagrams embedded directly in notes |
| **Git** | Auto-backup vault to a GitHub repository |
| **Kanban** | Visual board for tracking active learning tasks |
| **Admonition** | Enhanced callout blocks for tips, warnings, and notes |

### Vault Conventions

- **YAML frontmatter** on every note (except this README)
- **Source field** always set to `devopsinsiders/batch-18`
- **Tags** use kebab-case: `terraform`, `azure-networking`, `landing-zone`
- **Cross-links** use Obsidian wikilinks: `[[Note-Name]]`
- **Code blocks** always include language identifier: ` ```hcl `, ` ```bash `, ` ```yaml `
- **Callouts** for critical info: `> [!warning]`, `> [!tip]`, `> [!important]`

### Standard Frontmatter Template

```yaml
---
tags: [topic, subtopic, azure/terraform/linux]
source: devopsinsiders/batch-18
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## 📊 Vault Stats

| Metric | Value |
|--------|-------|
| 📁 Total Sections | 13 |
| 📄 Estimated Notes | 85+ |
| 🏗️ Terraform Topics | 17 |
| ☁️ Azure Services Covered | 17 |
| 🏢 Landing Zone Design Areas | 17 |
| 🔄 CI/CD Topics | 7 |
| 🎯 Interview Prep Domains | 7 |
| 🔨 Real-World Projects | 4 |
| 📋 Architecture Decision Records | 4 |
| 🤖 Agentic AI Topics | 4 |
| 🔐 Security Scanning Tools | 7 |

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

---

<div align="center">

**DevOps Insiders — Batch 18** &nbsp;|&nbsp; Built with ❤️ in Obsidian &nbsp;|&nbsp; Updated July 2026

*"The best time to build a knowledge system was when you started. The second best time is now."*

</div>
