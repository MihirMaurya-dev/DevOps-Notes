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
- [x] Cloud Models vs On-Premises
- [x] Virtualization Basics
- [x] Networking Fundamentals (DNS, IP Addressing, Routing)
- [x] Azure Hierarchy (Tenant -> Management Groups -> Subscriptions -> RG)
- [x] Identity & Access Management (Microsoft Entra ID, RBAC)
- [x] Managed Identities
- [x] Compute (Virtual Machines, VMSS)
- [x] Networking (VNet, Subnets, NSGs, Peering, Route Tables)
- [x] Storage (Storage Accounts, Blob, Files)
- [x] Security (Key Vault)
- [x] Monitoring (Azure Monitor, Log Analytics)
- [x] Container Orchestration (AKS Fundamentals)

## Phase 3: Infrastructure as Code
- [x] Imperative vs Declarative approaches
- [x] Terraform Introduction & Setup
- [x] Providers and Authentication
- [x] State Management & Remote Backends
- [x] Resources and Data Sources
- [x] Variables, Locals, and Outputs
- [x] Loops and Conditionals (`count`, `for_each`)
- [x] Modules (Creation and Usage)
- [x] Workspaces (Dev/Prod isolation)
- [x] CI/CD Pipeline Integration

## Phase 4: Enterprise Architecture & Landing Zones
- [x] Cloud Adoption Framework (CAF) Overview
- [x] Landing Zone Accelerator Design Principles
- [x] Subscription Democratization Strategy
- [x] Management Group Hierarchy Design
- [x] Identity and Governance (Azure Policy)
- [x] Networking Topologies (Hub & Spoke vs vWAN)
- [x] Security and Monitoring baselines
- [x] Architecture Patterns (Multi-Region, DR, Zero Trust)
- [x] Real World Project Implementations

## Phase 5: CI/CD & DevOps Practices
- [x] Git Branching Strategies (Trunk-Based, GitFlow)
- [x] GitOps Principles
- [x] Azure DevOps Pipelines
- [x] GitHub Actions
- [x] Release Strategies (Blue/Green, Canary, Rolling)
- [x] Secrets Management in Pipelines
- [x] Automated Testing integration
- [x] DORA Metrics & DevOps KPIs

## Phase 6: Advanced Topics (Ongoing)
- [x] Service Mesh Concepts (Istio, Linkerd, OSM)
- [x] Enterprise Architecture Patterns (Shared Services, vWAN Global Transit)
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

## Notes & Reflections
- **Biggest insight:** VNet Peering is non-transitive. Always route inter-spoke traffic via Hub Firewall.
- **Common mistake:** Forgetting `-input=false` in Terraform pipelines causes the pipeline to hang forever.
- **Key pattern to remember:** Use Group-Based RBAC, never direct user assignments, to avoid the 4,000 role assignment limit.
- **Interview tip:** For every security question, structure the answer around Identity → Network → Data layers (Zero Trust model).
