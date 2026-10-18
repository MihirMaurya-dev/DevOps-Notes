---
tags: [decision-log, terraform, state]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Decision Log: Terraform Remote State Backend

## Context
As we move to deploying infrastructure via CI/CD pipelines, we can no longer store the Terraform state file (`terraform.tfstate`) locally. Local state is dangerous in a team environment for several reasons:
- **State Conflicts:** Two engineers running `terraform apply` simultaneously will overwrite each other's changes.
- **No Locking:** Local state provides no mechanism to prevent concurrent runs.
- **Secret Exposure:** Terraform state often contains sensitive values (passwords, connection strings) in plain text. Storing this locally on laptops is a major security risk.

## Options Considered
1. **Terraform Cloud:** HashiCorp's managed service for running Terraform and storing state.
2. **Azure Blob Storage:** Using a standard Azure Storage Account container as the backend.

## Decision
**Selected Option:** Azure Blob Storage with Azure AD Auth.

## Rationale
- **Data Sovereignty and Security:** Storing the state file in our own Azure subscription ensures that sensitive metadata about our infrastructure never leaves our controlled network boundary.
- **Cost:** Azure Blob Storage is incredibly cheap for the small size of state files.
- **Native Locking:** Azure Blob Storage natively supports state locking via Blob Leases. When a pipeline runs, it acquires a lease. If another pipeline starts, it sees the lease and fails immediately, preventing corruption.
- **Identity Integration:** Instead of managing static access keys, we configure Terraform to authenticate to the Storage Account using the CI/CD pipeline's Managed Identity (Azure AD/Entra ID).

## Terraform Implementation Block

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-mgmt"
    storage_account_name = "sttfstateprod001"
    container_name       = "tfstate"
    key                  = "platform.tfstate"
    use_oidc             = true  # Authenticate via Workload Identity Federation
    use_azuread_auth     = true  # Don't use storage account access keys
  }
}
```

## Security and Protection Mechanisms
To protect the state file from accidental deletion or corruption, the Storage Account is configured with:
- **Versioning:** Enabled, so every `terraform apply` creates a new version of the state blob. If state is corrupted, we can revert to a previous version.
- **Soft Delete:** Enabled with a 14-day retention period.
- **Resource Lock:** A `CanNotDelete` lock applied to the Storage Account.

## The Bootstrap Problem
A common challenge is that you need a Storage Account to store Terraform state, but you want to use Terraform to create the Storage Account.
**Solution:** We use a one-time Bash/Azure CLI script executed locally by a senior engineer to bootstrap the initial Resource Group, Storage Account, and Container. Once created, the backend configuration is added to the Terraform code, and Terraform "adopts" the infrastructure.
