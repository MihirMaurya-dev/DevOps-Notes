---
tags: [decision-log, security, rbac, identity]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Decision Log: RBAC Assignment Model

## Context
As we scale to multiple Azure Subscriptions, managing who has access to what resources is becoming a significant administrative burden. We need a standardized approach to Azure Role-Based Access Control (RBAC).

## Options Considered
1. **Direct User Assignment:** Assigning Azure roles (e.g., Contributor) directly to individual user accounts at the Resource Group or Subscription level.
2. **Group-Based Assignment:** Creating Entra ID Security Groups, assigning the Azure roles to the groups, and adding users to the groups.

## Decision
**Selected Option:** Group-Based Assignment.

## Rationale
- **Onboarding/Offboarding:** Group-based assignment drastically reduces the operational overhead. New engineers are added to the "DevOps Engineers" group and inherit access. Offboarding is a single click in Entra ID.
- **Auditability:** Much easier to audit a small set of groups rather than thousands of individual assignments.
- **Hard Limit Avoidance:** Azure has a hard limit of 4,000 role assignments per subscription. Group assignments prevent hitting this limit.

## Standard Group Naming Convention
We adopted a strict naming convention for Entra ID groups used for Azure RBAC:
`AZ-<ScopeLevel>-<ScopeName>-<RoleName>`

| Group Name | Scope Level | Scope Name | Assigned Azure Role |
|------------|-------------|------------|---------------------|
| `AZ-SUB-BillingApp-Contributor` | Subscription | BillingApp | Contributor |
| `AZ-SUB-BillingApp-Reader` | Subscription | BillingApp | Reader |
| `AZ-RG-CoreNet-NetworkContributor`| Resource Group| CoreNet | Network Contributor |
| `AZ-MG-Corp-PolicyContributor` | Management Grp| Corp | Resource Policy Contributor |

## Terraform Implementation Code
Infrastructure as Code manages the role assignments. The Entra ID groups are managed separately (or via the AzureAD Terraform provider).

```hcl
# Look up the Entra ID group by its display name
data "azuread_group" "app_contributors" {
  display_name     = "AZ-SUB-BillingApp-Contributor"
  security_enabled = true
}

# Assign the group to the Subscription
resource "azurerm_role_assignment" "sub_contributor" {
  scope                = data.azurerm_subscription.current.id
  role_definition_name = "Contributor"
  principal_id         = data.azuread_group.app_contributors.object_id
}
```

## Role Mapping Matrix
Built-in roles are preferred. Custom roles are only created if absolutely necessary.
- **Developers:** `Contributor` in Dev/Test Sandboxes. `Reader` in Production.
- **DevOps/Platform Team:** `Contributor` at the Landing Zone Management Group level.
- **Security Team:** `Security Reader` at the Root Management Group level.
- **CI/CD Pipelines:** Scoped `Contributor` or specific custom roles via Service Principals/Managed Identities.

## PIM Integration and Exceptions
- **Standing Access:** Nobody has standing `Owner` or `Contributor` access to Production subscriptions.
- **PIM:** Entra ID Privileged Identity Management (PIM) is used. Engineers are made *eligible* members of the Entra ID group (e.g., `AZ-SUB-ProdApp-Contributor`). 
- When an incident occurs, they activate the role in the Azure Portal, provide a ticket number, and gain access for a maximum of 4 hours before it auto-revokes.
