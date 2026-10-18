---
tags: [architecture, patterns, enterprise, alz]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Architecture Pattern: Enterprise Architecture

Enterprise Architecture in Azure is built upon the **Azure Landing Zone Accelerator** (formerly Enterprise-Scale Landing Zone). It is a strategic design that scales automatically without hitting subscription limits or creating security loopholes.

## The Three Pillars of Enterprise Architecture

1. **Democratization of Subscriptions:**
   - In a small business, everything might live in 1-2 subscriptions.
   - In an Enterprise Architecture, subscriptions are treated as disposable containers. Every new major workload or application gets its own subscription. This contains the "blast radius" if something goes wrong and prevents hitting Azure's hard resource limits.

2. **Policy-Driven Governance:**
   - Enterprises cannot rely on manual approvals for every resource creation.
   - Guardrails are established using Azure Policy at the Management Group level. If a developer tries to do something insecure (like opening port 3389 to the public internet), Azure Policy blocks it automatically.
   - This allows developers to work fast (agile) while keeping the security team happy (governance).

3. **Centralized Platform Control vs Decentralized Workloads:**
   - **Centralized:** Identity (Entra ID), Hub Networking (Firewalls, ExpressRoute), and Security logging (Sentinel, Log Analytics) are tightly controlled by the central Cloud Center of Excellence (CCoE) team.
   - **Decentralized:** Application development, VM creation, and database management within the Spoke subscriptions are handled entirely by the individual product teams.

## Management Group Hierarchy

The core of ALZ is the Management Group (MG) structure. It allows you to assign policies and RBAC roles that automatically inherit down to the subscriptions beneath them.

```hcl
# Terraform Example: Core Hierarchy
resource "azurerm_management_group" "tenant_root" {
  display_name = "Contoso"
  name         = "contoso-root"
}

resource "azurerm_management_group" "platform" {
  display_name               = "Platform"
  name                       = "contoso-platform"
  parent_management_group_id = azurerm_management_group.tenant_root.id
}

resource "azurerm_management_group" "landing_zones" {
  display_name               = "Landing Zones"
  name                       = "contoso-lz"
  parent_management_group_id = azurerm_management_group.tenant_root.id
}

# Sub-groups for different workload archetypes
resource "azurerm_management_group" "corp" {
  display_name               = "Corp"
  name                       = "contoso-lz-corp" # Internal only, no public IPs
  parent_management_group_id = azurerm_management_group.landing_zones.id
}

resource "azurerm_management_group" "online" {
  display_name               = "Online"
  name                       = "contoso-lz-online" # Public facing allowed
  parent_management_group_id = azurerm_management_group.landing_zones.id
}
```

## Subscription Archetypes

- **Platform Subscriptions:** Managed by the CCoE. Usually split into `Connectivity` (Networking), `Management` (Logging/Security), and `Identity` (Domain Controllers).
- **Landing Zone Subscriptions:** Where actual applications live.
- **Sandbox Subscriptions:** Highly restricted but autonomous subscriptions for developers to experiment. Often disconnected from the corporate network and have aggressive budget caps.

## Cloud Center of Excellence (CCoE)
The CCoE is a cross-functional team responsible for the cloud platform.
- **Responsibilities:** Platform architecture, baseline security policies, IAM/RBAC models, hybrid networking, and providing "vending machine" templates for application teams to request new Landing Zones.
- **Anti-pattern:** The CCoE should *not* be a bottleneck deploying application resources. They manage the "plumbing" and guardrails; app teams deploy their own code.

## FinOps Integration
Enterprise architecture requires cost accountability.
- Assign Azure Policies to enforce `CostCenter` and `Project` tags on every resource.
- Map Subscriptions directly to business units for clear chargeback models.
- Use Azure Budgets at the Subscription scope to trigger alerts to the specific app owners, not just central IT.

## Real-World Implementation Checklist
- [ ] Entra ID Tenant configured with MFA and Conditional Access.
- [ ] Management Group hierarchy deployed via IaC (Terraform/Bicep).
- [ ] Central Log Analytics workspace deployed and diagnostic setting policies assigned at root.
- [ ] Azure Policies applied for tagging, allowed regions, and denied resource types.
- [ ] Hub network deployed with Azure Firewall and ExpressRoute/VPN.
- [ ] Subscription vending process established for new app teams.
