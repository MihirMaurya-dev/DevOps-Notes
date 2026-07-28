---
tags: [devops, azure, cost-governance, naming, caf]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Azure Naming Conventions (CAF-aligned)

## Basics
An **Azure Naming Convention** is a standardized set of rules used to name cloud resources. Microsoft provides the Cloud Adoption Framework (CAF) which outlines best practices for consistent resource naming.

## Why it matters
- **Identification**: You can look at a resource name and immediately know its type, purpose, environment, and region.
- **Uniqueness**: Many Azure resources (like Storage Accounts, Key Vaults) require globally unique names across all of Azure.
- **Limitations**: Different Azure resources have different naming rules (e.g., Storage Accounts allow only lowercase letters and numbers, max 24 chars; VMs max 15 chars in Windows).
- **Automation**: Predictable names allow scripts and CI/CD pipelines to easily target resources.

## How it works
The standard CAF-recommended naming format is:
`<resource-type>-<workload/project>-<environment>-<region>-<instance>`

### Resource Type Abbreviations Table
| Resource Type | Abbreviation | Example |
| :--- | :--- | :--- |
| Resource Group | `rg` | `rg-myapp-prod-eastus-01` |
| Virtual Network | `vnet` | `vnet-myapp-prod-eastus-01` |
| Subnet | `snet` | `snet-frontend-prod-eastus-01` |
| Virtual Machine | `vm` | `vmmyappprdeus01` (Windows limited to 15 chars) |
| Storage Account | `st` | `stmyappprodeastus01` (no dashes allowed) |
| Key Vault | `kv` | `kv-myapp-prod-eastus-01` |
| AKS Cluster | `aks` | `aks-myapp-prod-eastus-01` |
| Public IP | `pip` | `pip-myapp-prod-eastus-01` |

## Azure implementation (with code/CLI)

### Terraform: Implementing naming via locals
To ensure consistency and enforce limitations, generate names dynamically in Terraform using `locals`.

```hcl
variable "project" { default = "crm" }
variable "environment" { default = "prod" }
variable "location_abbr" { default = "eus" } # East US

locals {
  # Standard CAF prefix: crm-prod-eus
  base_name = "${var.project}-${var.environment}-${var.location_abbr}"
  
  # Remove dashes for storage accounts
  base_name_nodash = replace(local.base_name, "-", "")
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${local.base_name}-01" # Result: rg-crm-prod-eus-01
  location = "eastus"
}

resource "azurerm_storage_account" "sa" {
  # Result: stcrmprodeus01
  name                     = "st${local.base_name_nodash}01"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

## Production best practices
- **Global Uniqueness**: For resources that require global uniqueness (like Storage Accounts), append a short random string to the end of the name to prevent deployment failures if the name is taken.
- **Short location codes**: Use custom short codes for regions (e.g., `eus` for eastus, `weu` for westeurope) to save characters.
- **Instance numbers**: Always include a 2-digit instance number (e.g., `-01`, `-02`) even if you only have one resource. It makes scaling easier later.

## CI/CD integration
Enforce naming conventions during the PR process using **TFLint**.

```hcl
# .tflint.hcl
rule "azurerm_resource_group_naming" {
  enabled = true
  # Regex to enforce rg-<project>-<env>-<region>-<instance>
  regex   = "^rg-[a-z0-9]+-(dev|qa|prod)-(eus|weu)-[0-9]{2}$"
}
```

## Interview Q&A

1. **Why do we remove hyphens when naming an Azure Storage Account?**
   *Answer*: Azure Storage Account names must be between 3 and 24 characters in length and can contain only numbers and lowercase letters. Hyphens and special characters are explicitly forbidden.

2. **What are the naming constraints for an Azure Windows Virtual Machine?**
   *Answer*: A Windows VM name in Azure cannot exceed 15 characters because of the NetBIOS naming restriction in Windows OS.

3. **How do you ensure global uniqueness for resources like Key Vault via automation?**
   *Answer*: I use the `random_string` or `random_id` resource in Terraform to generate a short, predictable unique suffix (e.g., 4 characters) and append it to the standard naming convention.
