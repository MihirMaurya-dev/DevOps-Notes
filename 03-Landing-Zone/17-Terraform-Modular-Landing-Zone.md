---
tags: [terraform, landing-zone, modules, enterprise, for_each]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🏗️ Terraform Modular Landing Zone

This guide explains how to structure Terraform code at enterprise scale — using **reusable child modules**, **dynamic resource creation**, and **environment separation** to deploy a complete Azure Landing Zone.

---

## 1. Why Modular Terraform?

A **monolithic** `main.tf` works for small projects but becomes impossible to manage at enterprise scale:

| Problem (Monolithic) | Solution (Modular) |
|---|---|
| 1 huge file, 500+ lines | Root module calls small, focused modules |
| Copy-paste for each environment | One module, many environments via `tfvars` |
| Change in dev breaks prod | Separate state per environment |
| Hard to reuse for other teams | Module published to internal Terraform Registry |

---

## 2. Directory Structure

```
terraform-landing-zone/
│
├── modules/                        # Reusable child modules
│   ├── resource-group/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── virtual-network/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── subnet/
│   ├── nsg/
│   ├── virtual-machine/
│   └── key-vault/
│
├── environments/                   # One folder per environment
│   ├── dev/
│   │   ├── main.tf                 # Calls modules
│   │   ├── variables.tf
│   │   ├── terraform.tfvars        # Dev-specific values
│   │   └── backend.tf              # Dev state backend
│   ├── qa/
│   ├── preprod/
│   └── prod/
│       ├── main.tf
│       ├── terraform.tfvars        # Prod-specific values (larger SKUs etc.)
│       └── backend.tf
│
└── README.md
```

---

## 3. Root Module — Calling Child Modules

The root `main.tf` in each environment is a clean, readable map of the infrastructure:

```hcl
# environments/prod/main.tf

module "resource_groups" {
  source   = "../../modules/resource-group"
  rg_name  = var.rg_name
  location = var.location
  tags     = var.tags
}

module "virtual_network" {
  source              = "../../modules/virtual-network"
  vnet_name           = var.vnet_name
  vnet_address_space  = var.vnet_address_space
  location            = module.resource_groups.location
  resource_group_name = module.resource_groups.name
  tags                = var.tags
}

module "subnets" {
  source               = "../../modules/subnet"
  subnets              = var.subnets
  virtual_network_name = module.virtual_network.name
  resource_group_name  = module.resource_groups.name
}

module "virtual_machines" {
  source              = "../../modules/virtual-machine"
  vms                 = var.vms
  resource_group_name = module.resource_groups.name
  location            = module.resource_groups.location
  tags                = var.tags
}
```

---

## 4. Dynamic Resource Creation with `for_each`

Instead of copy-pasting resource blocks, use `for_each` with a variable map:

```hcl
# modules/virtual-machine/main.tf

resource "azurerm_linux_virtual_machine" "vm" {
  for_each            = var.vms
  name                = each.value.vm_name
  resource_group_name = var.resource_group_name
  location            = var.location
  size                = each.value.vm_size
  admin_username      = each.value.admin_username

  # Fetch the subnet dynamically using a data source
  network_interface_ids = [azurerm_network_interface.nic[each.key].id]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = each.value.disk_type
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  tags = var.tags
}
```

Define multiple VMs in `terraform.tfvars` — zero code duplication:

```hcl
# environments/prod/terraform.tfvars

vms = {
  web = {
    vm_name        = "vm-web-prod"
    vm_size        = "Standard_D2s_v3"
    admin_username = "adminuser"
    disk_type      = "Premium_LRS"
    nic_subnet_name = "web-subnet"
  }
  app = {
    vm_name        = "vm-app-prod"
    vm_size        = "Standard_D4s_v3"
    admin_username = "adminuser"
    disk_type      = "Premium_LRS"
    nic_subnet_name = "app-subnet"
  }
  db = {
    vm_name        = "vm-db-prod"
    vm_size        = "Standard_E8s_v3"
    admin_username = "adminuser"
    disk_type      = "UltraSSD_LRS"
    nic_subnet_name = "db-subnet"
  }
}
```

---

## 5. Data Sources for Dependency Decoupling

Modules use `data` blocks to look up existing resources instead of creating hard dependencies:

```hcl
# modules/virtual-machine/data.tf

# Look up the subnet by name — decouples VM module from subnet module
data "azurerm_subnet" "subnet" {
  for_each             = var.vms
  name                 = each.value.nic_subnet_name
  virtual_network_name = each.value.nic_vnet_name
  resource_group_name  = each.value.rg_name
}

# Look up the Key Vault to fetch admin credentials
data "azurerm_key_vault_secret" "admin_password" {
  name         = "vm-admin-password"
  key_vault_id = data.azurerm_key_vault.kv.id
}
```

---

## 6. Remote State Backend Per Environment

Each environment has **its own state file** in Azure Blob Storage — isolated blast radius:

```hcl
# environments/prod/backend.tf

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstateprod"
    container_name       = "tfstate"
    key                  = "prod/landing-zone.tfstate"
  }
}
```

```hcl
# environments/dev/backend.tf

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstatedev"
    container_name       = "tfstate"
    key                  = "dev/landing-zone.tfstate"  # Separate state!
  }
}
```

---

## 7. CI/CD Pipeline for Modular LZ

```yaml
# .github/workflows/deploy-lz.yml
name: Landing Zone Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TF_ENV: prod                    # Change per environment branch
  WORKING_DIR: environments/prod

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init
        working-directory: ${{ env.WORKING_DIR }}

      - name: Terraform Validate
        run: terraform validate
        working-directory: ${{ env.WORKING_DIR }}

      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: ${{ env.WORKING_DIR }}

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
        working-directory: ${{ env.WORKING_DIR }}
```

---

## 8. Production Best Practices

> [!important]
> Never run `terraform apply` directly on production. Always go through a PR → Plan → Review → Apply workflow.

- ✅ **One state per environment** — isolates blast radius
- ✅ **Modules versioned** — use `source = "git::...?ref=v1.2.0"` to pin module versions
- ✅ **`terraform.tfvars` never committed** — use CI/CD secrets or Azure Key Vault
- ✅ **`required_providers` version locked** — prevents provider upgrades from breaking code
- ✅ **`terraform fmt` + `tflint` + `checkov`** run in PR checks before apply
- ✅ **State file encrypted** — Azure Blob Storage with encryption at rest enabled

---

## 9. Module Versioning Example

```hcl
# Pin to a specific git tag for stability
module "virtual_network" {
  source  = "git::https://github.com/your-org/terraform-modules.git//virtual-network?ref=v2.1.0"
  # ...
}
```
