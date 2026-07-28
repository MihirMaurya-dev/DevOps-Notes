---
tags: [devops, azure, cost-governance, tagging, terraform]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Azure Resource Tagging Strategy

## Basics
**Resource Tagging** in Azure involves assigning name-value pairs (tags) to Azure resources, resource groups, and subscriptions. Tags help logically organize resources for billing, management, and operational purposes.

## Why it matters
Tagging is the absolute foundation of cloud governance. Without tags:
- You cannot easily identify who owns a resource.
- You cannot accurately attribute cloud costs to specific departments or projects in Azure Cost Management.
- Automation scripts won't know which resources to target (e.g., shutting down all "Dev" VMs at night).
- Security audits become nightmare scenarios trying to find resource owners.

## How it works
Tags are applied as metadata to the Azure resource object. An Azure resource can have up to 50 tags. The tag names and values are strings. You can enforce tagging rules using Azure Policy so that resources cannot be created without required tags.

### Standard Tag Schema Design
A production-grade schema usually includes:
- `Environment`: dev, qa, uat, prod
- `Project`: web-portal, data-lake
- `Owner`: email address of the team lead
- `CostCenter`: finance code (e.g., CC-9982)
- `ManagedBy`: terraform, bicep, manual
- `CreatedDate`: 2026-07-28

## Azure implementation (with code/CLI)

### Terraform: Enforcing tags via locals
The best way to manage tags in Terraform is using a `local` variable block and merging it into every resource.

```hcl
# locals.tf
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner_email
    CostCenter  = "CC-12345"
    ManagedBy   = "Terraform"
  }
}

# main.tf
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = "eastus"
  tags     = local.common_tags
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-main"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
  
  # Merge common tags with specific tags
  tags = merge(local.common_tags, {
    Component = "Networking"
  })
}
```

### Azure Policy for Tag Enforcement
You can use Azure Policy to automatically append tags or deny resource creation if tags are missing.

```azurecli
# Assign a built-in policy to require a tag named 'CostCenter' on resource groups
az policy assignment create \
  --name 'require-costcenter-tag' \
  --policy "1e30110a-5ceb-460c-a204-c1c3969c6d62" \
  --params "{'tagName': {'value': 'CostCenter'}}"
```

## Production best practices
- **Inheritance**: Set tags at the Resource Group level and use Azure Policy to automatically inherit them down to the resources inside. This saves time and ensures consistency.
- **Lowercase standard**: Enforce lowercase for tag names to avoid duplicates like `Environment=dev` and `environment=dev`.
- **Do not store secrets**: Never store sensitive data (passwords, PII) in tags, as they are visible to anyone with Reader access.

## CI/CD integration
You should fail the CI pipeline if required tags are missing in the Infrastructure as Code.

Using **Checkov** or **TFLint** in CI/CD:
```yaml
# .github/workflows/tf-validate.yml
steps:
  - name: Run Checkov
    uses: bridgecrewio/checkov-action@master
    with:
      directory: ./terraform
      framework: terraform
      # Custom checkov rules can verify local.common_tags exists on all resources
```

## Interview Q&A

1. **How do you ensure every resource in Azure is tagged with a Cost Center?**
   *Answer*: Implement an Azure Policy with a "Deny" effect that prevents resource creation if the `CostCenter` tag is missing. Alternatively, use an "Append" or "Modify" policy to inherit the tag from the parent Resource Group.

2. **How do you handle tagging in Terraform to avoid repeating code?**
   *Answer*: Define a `locals` block with a map of common tags, and assign `tags = local.common_tags` to every resource.

3. **Can you tag everything in Azure?**
   *Answer*: No, some resource types do not support tags. It's important to rely on Resource Group tagging as a fallback and use Azure Policy to govern supported resources.
