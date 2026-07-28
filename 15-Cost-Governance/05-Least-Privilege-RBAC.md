---
tags: [devops, azure, security, rbac, iam]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Least Privilege & RBAC in Azure

## Basics
**Role-Based Access Control (RBAC)** is Azure's authorization system built on Azure Resource Manager (ARM). 
The **Principle of Least Privilege** means giving a user, application, or pipeline exactly the minimum level of access required to perform its job, and nothing more.

## Why it matters
If a CI/CD pipeline has "Owner" access to a Subscription, and a hacker compromises the pipeline, they can delete the entire cloud infrastructure or mine crypto. Enforcing least privilege limits the blast radius of any security breach.

## How it works
Azure RBAC consists of three elements:
1. **Security Principal**: WHO needs access? (User, Group, Service Principal, Managed Identity).
2. **Role Definition**: WHAT can they do? (Owner, Contributor, Reader, or Custom Roles).
3. **Scope**: WHERE can they do it? (Management Group → Subscription → Resource Group → Specific Resource).

### Built-in Roles
- **Owner**: Can manage everything, including assigning access to others.
- **Contributor**: Can manage everything, but *cannot* assign access to others.
- **Reader**: Can view resources, but cannot make changes or view secrets.

## Azure implementation (with code/CLI)

### Terraform: Assigning a Role
```hcl
data "azurerm_client_config" "current" {}

# Create a User Assigned Managed Identity
resource "azurerm_user_assigned_identity" "app_id" {
  name                = "id-backend-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

# Assign Storage Blob Data Contributor to the Identity, scoped ONLY to a specific storage account
resource "azurerm_role_assignment" "storage_access" {
  scope                = azurerm_storage_account.sa.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.app_id.principal_id
}
```

## Production best practices
- **Use Managed Identities over Service Principals**: Whenever Azure resources need to talk to each other (e.g., VM to Key Vault), use Managed Identities. You don't have to manage or rotate credentials—Azure handles it securely.
- **Privileged Identity Management (PIM)**: For human administrators, do not assign permanent "Owner" or "Contributor" roles. Use Entra ID PIM to provide Just-in-Time (JIT) access that requires approval and expires after a few hours.
- **Scope granularly**: Never assign Contributor at the Subscription level if the user only needs access to a single Resource Group.
- **Deny Assignments**: Use Azure Blueprints or Deployment Stacks to create Deny Assignments, which prevent even an Owner from modifying or deleting critical resources.

## CI/CD integration
Stop using long-lived Client Secrets (Passwords) for GitHub Actions or Azure DevOps service connections.

Use **Workload Identity Federation (OIDC)**. This establishes a trust relationship between GitHub and Azure. GitHub requests a short-lived token from Azure Entra ID to run the pipeline, eliminating the need to store secrets as GitHub repository variables.

## Interview Q&A

1. **What is the difference between Contributor and Owner in Azure?**
   *Answer*: Both can create, update, and delete resources. However, only the Owner can modify RBAC assignments (grant access to other users).

2. **Why should you use a Managed Identity instead of a Service Principal?**
   *Answer*: A Service Principal requires you to generate a secret/certificate, store it securely (e.g., in Key Vault), and rotate it before it expires. A Managed Identity eliminates credential management completely because Azure infrastructure natively authenticates the resource.

3. **How do you give a developer read access to everything in a subscription, but allow them to restart only a specific VM?**
   *Answer*: I would assign the "Reader" role at the Subscription scope, and assign the "Virtual Machine Contributor" role (or a custom role with `Microsoft.Compute/virtualMachines/restart/action`) scoped specifically to that single VM resource.
