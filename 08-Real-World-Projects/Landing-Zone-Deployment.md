---
tags: [project, landing-zone, alz, architecture]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Project: Azure Landing Zone Deployment

## Overview
Implement a foundational Azure Landing Zone following Microsoft's Enterprise-Scale architecture principles to support a portfolio of 50+ applications.

## Management Group Hierarchy
The environment is structured using Management Groups to apply governance boundaries at scale:
- **Tenant Root Group**
  - **Contoso Root** (Baseline Policies applied here)
    - **Platform**
      - Identity
      - Management
      - Connectivity
    - **Landing Zones**
      - Corp (Internal-facing apps)
      - Online (Public-facing apps)
    - **Sandboxes** (Dev experimentation)
    - **Decommissioned**

### Terraform Implementation
```hcl
resource "azurerm_management_group" "root" {
  display_name = "Contoso Root"
  name         = "contoso-root"
}

resource "azurerm_management_group" "platform" {
  display_name               = "Platform"
  name                       = "contoso-platform"
  parent_management_group_id = azurerm_management_group.root.id
}

resource "azurerm_management_group" "landing_zones" {
  display_name               = "Landing Zones"
  name                       = "contoso-landing-zones"
  parent_management_group_id = azurerm_management_group.root.id
}

# Assign subscription to Management Group
resource "azurerm_management_group_subscription_association" "prod_app" {
  management_group_id = azurerm_management_group.landing_zones.id
  subscription_id     = "/subscriptions/00000000-0000-0000-0000-000000000000"
}
```

## Azure Policy Assignments
We use "Policy-Driven Governance" to enforce rules instead of manual review.

```hcl
# Example: Require Resource Tag
resource "azurerm_management_group_policy_assignment" "require_cost_center" {
  name                 = "require-costcenter-tag"
  management_group_id  = azurerm_management_group.root.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/1e30110a-5ceb-460c-a204-c1c3969c6d62"
  
  parameters = jsonencode({
    tagName = {
      value = "CostCenter"
    }
  })
}
```

## Centralized Logging
- Deployed a central **Log Analytics Workspace** in the `Management` subscription.
- Applied a `DeployIfNotExists` Azure Policy at the Root Management Group to automatically configure Diagnostic Settings for all newly created resources (Key Vaults, NSGs, App Services) to send their logs to this central workspace.

## GitHub Actions Pipeline Structure
The Landing Zone is deployed via "Platform as Code":
1. **Repository:** `azure-platform-lz`
2. **Workflow:** 
   - `Pull Request`: Runs `terraform fmt`, `tflint`, `tfsec`, and `terraform plan`. Plan is output to PR comments.
   - `Merge to Main`: Runs `terraform apply -auto-approve`. Uses OIDC authentication (Workload Identity Federation) for zero-secret deployment.

## Onboarding Checklist for Workload Teams
When a new team needs a landing zone:
- [ ] Create a new Subscription via Enterprise Agreement billing profile.
- [ ] Move Subscription under `Landing Zones -> Corp` or `Online` Management Group.
- [ ] Provision Spoke VNet.
- [ ] Peer Spoke VNet to Hub VNet.
- [ ] Configure Route Table (UDR) pointing to Hub Firewall and associate with Spoke subnets.
- [ ] Create Azure AD Groups for RBAC (`AppX-Admins`, `AppX-Readers`) and assign at Subscription scope.
- [ ] Hand over to the workload team.
