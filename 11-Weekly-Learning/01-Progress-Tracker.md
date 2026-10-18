---
tags: [learning, progress, tracker]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Weekly Learning Progress Tracker

This document tracks the progress through the DevOps Insiders Batch 18 curriculum.

## Phase 1: Linux & Fundamentals
- [ ] OS Architecture (Kernel vs User Space)
- [ ] File System Hierarchy (FHS)
- [ ] Core Navigation & File Commands
- [ ] Text Processing (Grep, Awk, Sed)
- [ ] Users, Groups, and Permissions (chmod, chown)
- [ ] Networking Basics (SSH, Keys, Ports)
- [ ] Network Troubleshooting (curl, ping, ss)
- [ ] Package Management (apt)
- [ ] Services and Daemons (systemd, journalctl)
- [ ] Task Scheduling (cron)
- [ ] Bash Scripting (Variables, Logic, Strict Mode)

## Phase 2: Cloud Fundamentals (Azure)
- [ ] Cloud Models vs On-Premises
- [ ] Virtualization Basics
- [ ] Networking Fundamentals (DNS, IP Addressing, Routing)
- [ ] Azure Hierarchy (Tenant -> Management Groups -> Subscriptions -> RG)
- [ ] Identity & Access Management (Microsoft Entra ID, RBAC)
- [ ] Managed Identities
- [ ] Compute (Virtual Machines, VMSS)
- [ ] Networking (VNet, Subnets, NSGs, Peering, Route Tables)
- [ ] Storage (Storage Accounts, Blob, Files)
- [ ] Security (Key Vault)
- [ ] Monitoring (Azure Monitor, Log Analytics)
- [ ] Container Orchestration (AKS Fundamentals)

## Phase 3: Infrastructure as Code
- [ ] Imperative vs Declarative approaches
- [ ] Terraform Introduction & Setup
- [ ] Providers and Authentication
- [ ] State Management & Remote Backends
- [ ] Resources and Data Sources
- [ ] Variables, Locals, and Outputs
- [ ] Loops and Conditionals (`count`, `for_each`)
- [ ] Modules (Creation and Usage)
- [ ] Workspaces (Dev/Prod isolation)
- [ ] CI/CD Pipeline Integration

## Phase 4: Enterprise Architecture & Landing Zones
- [ ] Cloud Adoption Framework (CAF) Overview
- [ ] Landing Zone Accelerator Design Principles
- [ ] Subscription Democratization Strategy
- [ ] Management Group Hierarchy Design
- [ ] Identity and Governance (Azure Policy)
- [ ] Networking Topologies (Hub & Spoke vs vWAN)
- [ ] Security and Monitoring baselines
- [ ] Architecture Patterns (Multi-Region, DR, Zero Trust)
- [ ] Real World Project Implementations

## Phase 5: CI/CD & DevOps Practices
- [ ] Git Branching Strategies (Trunk-Based, GitFlow)
- [ ] GitOps Principles
- [ ] Azure DevOps Pipelines
- [ ] GitHub Actions
- [ ] Release Strategies (Blue/Green, Canary, Rolling)
- [ ] Secrets Management in Pipelines
- [ ] Automated Testing integration
- [ ] DORA Metrics & DevOps KPIs

## Phase 6: Advanced Topics (Ongoing)
- [ ] Service Mesh Concepts (Istio, Linkerd, OSM)
- [ ] Enterprise Architecture Patterns (Shared Services, vWAN Global Transit)
- [ ] Kubernetes Security (OPA Gatekeeper, Pod Security Standards)
- [ ] GitOps with ArgoCD (Hands-on)
- [ ] Cost Management & FinOps in Azure
- [ ] Azure DevOps Self-Hosted Agents & Agent Pools
- [ ] Infrastructure Testing (Terratest, Checkov, tfsec)

---

## Key Milestones
| Date       | Achievement                                                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-06-08 | Vault created, Phases 1-5 content loaded                                                                                             |
| 2026-06-14 | All Phase 2 items completed (Key Vault, Monitor, AKS), vault expanded with Architecture Patterns, Real-World Projects, Decision Logs |
| 2026-10-02 | Integrated DI Interview Questions & Comprehensive Preparation Strategy with 5 Tailored Profile Introductions (Class 093)            |
| 2026-10-04 | Implemented Pipeline Parallelism & Parameterized Reusable YAML Templates (Classes 093 & 094)                                         |
| 2026-10-17 | Completed Azure Key Vault Deep Dive & Secrets Integration across Terraform and Azure Pipelines (Class 095)                           |
| 2026-10-18 | Deployed Flagship Axion 3-Tier Enterprise Infrastructure & Multi-Stage Deployment Platform (Project 06)                              |

## Notes & Reflections
- **Biggest insight:** VNet Peering is non-transitive. Always route inter-spoke traffic via Hub Firewall.
- **Common mistake:** Forgetting `-input=false` in Terraform pipelines causes the pipeline to hang forever.
- **Key pattern to remember:** Use Group-Based RBAC, never direct user assignments, to avoid the 4,000 role assignment limit.
- **Interview tip:** Structure interview introductions around Experience → Tools → Project → Responsibilities → Achievement, and lead with production-tested project stories.
- **Pipeline Optimization:** Run static security scans (TFLint, tfsec) and code validation in parallel (`dependsOn: []`) to cut pipeline execution time by ~50%.
- **Secret Zero Principle:** Never hardcode credentials in Terraform; dynamically fetch from Azure Key Vault using Managed Identities.

