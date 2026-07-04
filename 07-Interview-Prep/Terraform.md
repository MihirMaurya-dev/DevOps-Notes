---
tags: [interview, prep, terraform, questions]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Terraform Interview Questions

A collection of common interview questions regarding Infrastructure as Code using Terraform.

---

## Q1: What is the `terraform state` file and why is it important?
**A:** The `terraform.tfstate` file is a JSON file that Terraform uses to map the real-world infrastructure (like an actual Azure VM) to the configuration written in your `.tf` files. It keeps track of metadata and dependencies. It is critical because without it, Terraform wouldn't know what it has already created, and running `terraform apply` again might attempt to recreate existing resources or fail.

---

## Q2: How do you handle Terraform state in a team environment?
**A:** You must configure a **Remote Backend**. In Azure, this means storing the state file in an Azure Storage Account container. This ensures that everyone on the team (and the CI/CD pipeline) is reading from and writing to the exact same state file. You also must enable **State Locking** (which Azure Blob Storage supports natively) to prevent two people from running `terraform apply` at the same time and corrupting the file.

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstate001"
    container_name       = "tfstate"
    key                  = "prod/terraform.tfstate"
  }
}
```

---

## Q3: What is the difference between a Variable and a Local in Terraform?
**A:** 
- **Variables (`variable`):** Are inputs to your Terraform module. Their values can be passed in by the user at runtime via `.tfvars` files, environment variables, or the CLI.
- **Locals (`locals`):** Are internal values defined within the Terraform code. They are used to reduce repetition (e.g., combining a prefix, environment name, and resource type into a single string). Users cannot override locals from the outside.

```hcl
variable "environment" {
  type    = string
  default = "dev"
}

locals {
  resource_prefix = "${var.project}-${var.environment}"
}
```

---

## Q4: How do you pass a sensitive password to Terraform without hardcoding it?
**A:** You can define a variable and mark it as `sensitive = true`. You then pass the value to Terraform at runtime using environment variables (e.g., `export TF_VAR_db_password="SuperSecret"`). Alternatively, in a CI/CD pipeline, you can use an Azure Key Vault data source to dynamically fetch the secret during the plan/apply phase so it never exists in the configuration files or pipeline logs.

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

# Or fetch directly from Key Vault
data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.main.id
}
```

---

## Q5: What is a Terraform Provider?
**A:** A provider is a plugin that Terraform uses to translate the HCL code into API calls for a specific platform. For example, the `azurerm` provider translates Terraform code into Azure Resource Manager API calls, while the `aws` provider translates code into Amazon Web Services API calls.

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
}
```

---

## Q6: How does `terraform import` work and when would you use it?
**A:** `terraform import` associates an **existing real-world resource** with a Terraform resource block in your configuration. Terraform reads the resource's current state from the cloud provider API and writes it into the state file — but it does **not** generate the HCL configuration for you (you must write that manually, or use `terraform plan -generate-config-out` in Terraform 1.5+).

**When to use it:**
- Resources were created manually in the Azure Portal before Terraform was adopted.
- Resources created by another team or tool that you now want to manage with Terraform.
- Recovering from state drift after manual changes.

```bash
# Syntax: terraform import <resource_address> <provider_resource_id>
terraform import azurerm_resource_group.main \
  /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-prod

# Terraform 1.5+ import block (declarative, preferred)
# In .tf file:
# import {
#   to = azurerm_resource_group.main
#   id = "/subscriptions/.../resourceGroups/rg-prod"
# }
```

> [!warning]
> After import, always run `terraform plan` to verify that Terraform's desired state matches the imported resource's actual state. Any diff will be applied on the next `apply`, potentially causing unintended changes.

---

## Q7: What is the difference between `terraform taint` and `terraform replace`?
**A:**
- **`terraform taint` (deprecated in v0.15.2):** Manually marked a resource in the state file as "tainted," signaling it should be destroyed and recreated on the next `terraform apply`. It was a two-step process (taint, then apply).
- **`terraform apply -replace` (current approach):** Does the same thing in a single step — it forces Terraform to destroy and recreate the specified resource in the current apply operation.

```bash
# Old way (deprecated)
terraform taint azurerm_virtual_machine.web

# Modern way (Terraform >= 0.15.2)
terraform apply -replace="azurerm_virtual_machine.web"
```

**When to use:** When a resource is in a broken state that cannot be fixed in place (e.g., a VM whose OS is corrupted), and you need to force Terraform to rebuild it from scratch.

---

## Q8: Explain the `lifecycle` meta-argument and its options
**A:** The `lifecycle` block is a special meta-argument available on all Terraform resources that controls how Terraform handles resource creation, updates, and deletion. It overrides the default plan/apply behavior.

| Option | Purpose |
|---|---|
| `create_before_destroy` | Creates the replacement resource first before destroying the old one. Avoids downtime. |
| `prevent_destroy` | Raises an error if a `terraform destroy` or config change would delete this resource. Protects critical resources. |
| `ignore_changes` | Tells Terraform to ignore drift in specific attributes (e.g., tags managed externally). |
| `replace_triggered_by` | Forces replacement of this resource when another referenced resource changes. |

```hcl
resource "azurerm_linux_virtual_machine" "web" {
  # ... config ...

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
    ignore_changes        = [tags["LastModifiedBy"]]
  }
}
```

> [!tip]
> Use `prevent_destroy = true` on stateful resources like databases and storage accounts to act as a safety net against accidental `terraform destroy`. The plan will fail with a clear error message rather than silently queuing a deletion.

---

## Q9: How do you handle sensitive values in Terraform state?
**A:** This is a critical concern because **Terraform state always stores sensitive values in plaintext** — even variables marked `sensitive = true`. The `sensitive` flag only prevents values from being shown in CLI output; it does not encrypt the state file.

**Mitigations:**
1. **Remote Backend with Encryption at Rest**: Store state in Azure Storage Account with Storage Service Encryption (SSE) enabled. Enable versioning for recovery.
2. **Restrict Access to the State Backend**: Use Azure RBAC to allow only the service principal or Managed Identity running the pipeline to access the storage container — not individual developers.
3. **Avoid putting secrets in state**: Instead of creating a Key Vault secret *in* Terraform (which would write the value to state), reference secrets that were created out-of-band using a `data` source.

```hcl
# GOOD: Reference an existing secret - value NOT stored in Terraform state
data "azurerm_key_vault_secret" "db_conn" {
  name         = "db-connection-string"
  key_vault_id = data.azurerm_key_vault.main.id
}

# RISKY: Creating a secret in Terraform - value IS written to state
resource "azurerm_key_vault_secret" "db_conn" {
  name         = "db-connection-string"
  value        = var.db_password  # This goes into state plaintext
  key_vault_id = azurerm_key_vault.main.id
}
```

---

## Q10: What are the pros and cons of Terraform modules?
**A:** A Terraform module is a container of `.tf` files that groups related resources into a reusable, self-contained unit (e.g., a "vnet" module or an "aks-cluster" module).

**Pros:**
- **Reusability**: Define infrastructure patterns once and reuse them across environments or teams.
- **Abstraction**: Expose only necessary variables, hiding internal complexity.
- **Consistency**: Enforces standardized resource configurations organization-wide.
- **DRY Principle**: Eliminates copy-paste between dev/staging/prod environments.

**Cons:**
- **Complexity overhead**: Adds layers of abstraction that can make debugging harder.
- **Versioning discipline required**: Breaking changes to a module affect all consumers — requires proper semantic versioning via a module registry.
- **State management**: Modules don't have their own state; they share the calling root module's state, which can lead to very large state files.

```hcl
# Calling a module from Terraform Registry or local path
module "network" {
  source  = "Azure/network/azurerm"
  version = "~> 5.0"

  resource_group_name = azurerm_resource_group.main.name
  address_spaces      = ["10.0.0.0/16"]
  subnet_prefixes     = ["10.0.1.0/24", "10.0.2.0/24"]
}
```

---

## Q11: What is the difference between `count` and `for_each`?
**A:** Both are meta-arguments used to create multiple instances of a resource, but they behave differently and have different use cases.

| Feature | `count` | `for_each` |
|---|---|---|
| **Index type** | Integer index (0, 1, 2...) | Map key or set element (string) |
| **State address** | `azurerm_rg.main[0]` | `azurerm_rg.main["dev"]` |
| **Sensitivity to changes** | Deleting item `[0]` shifts all subsequent indexes, causing unnecessary re-creates | Deleting `"dev"` only affects that specific instance |
| **Use case** | Identical resources where order doesn't matter | Resources with distinct identities (names, environments) |
| **Input type** | Number | `map` or `set` |

```hcl
# count - creates 3 identical VMs, but removing one causes index shifts
resource "azurerm_resource_group" "rg" {
  count    = 3
  name     = "rg-${count.index}"
  location = "East US"
}

# for_each - each RG is tracked by a stable key, safe to add/remove
resource "azurerm_resource_group" "rg" {
  for_each = toset(["dev", "staging", "prod"])
  name     = "rg-${each.key}"
  location = "East US"
}
```

> [!important]
> Prefer **`for_each`** over `count` in almost all cases when creating named resources. The stable key-based addressing prevents destructive plan diffs when the list changes. Only use `count` for simple toggles (e.g., `count = var.create_resource ? 1 : 0`).

---

## Related Notes
- [[Azure]] — Azure platform concepts
- [[CI-CD]] — Running Terraform in pipelines
- [[Security]] — Securing Terraform state and secrets
