---
category: Terraform
tags: [terraform, cheat-sheet, reference, cli, hcl, commands]
type: fundamental
status: active
---

# Terraform Enterprise Cheat Sheet

## The Core Concept
This is the operational quick-reference guide for Terraform. It aggregates the most heavily utilized CLI commands, state manipulation operations, and foundational HCL structural blocks required for daily DevOps engineering and pipeline management.

## Under the Hood (The Commands & Syntax)

### 1. The Core CLI Workflow
```bash
terraform init                  # Initialize the working directory, download providers/modules
terraform init -upgrade         # Force update of providers and modules to latest allowed versions
terraform fmt                   # Reformat HCL code to standard canonical style
terraform validate              # Verify syntax and internal consistency of the code
terraform plan -out=tfplan      # Create and save an execution plan
terraform apply tfplan          # Execute the saved plan
terraform destroy               # Destroy all resources managed by the state
```


### 2. State Manipulation (Advanced)

_Warning: Always backup state or ensure remote backend leasing is active before running these._

Bash

```
terraform state list            # List all resources tracked in the current state
terraform state show <address>  # View the full JSON attributes of a specific tracked resource
terraform state rm <address>    # Remove a resource from state without destroying it in Azure
terraform state mv <old> <new>  # Rename a resource in state to match refactored code
terraform import <addr> <id>    # Bind an existing Azure resource ID to your HCL code
```

### 3. Core HCL Architecture Blocks

Terraform

```
# 1. The Terraform Block (Engine & Backend)
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.73.0"
    }
  }
  backend "azurerm" {
    # Populated dynamically via pipeline variables
  }
}

# 2. The Provider Block (Authentication)
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# 3. Resources & Data Sources (CRUD & Read)
resource "azurerm_resource_group" "main" {
  name     = var.rg_name
  location = var.location
}

data "azurerm_virtual_network" "hub" {
  name                = "vnet-hub"
  resource_group_name = "rg-hub"
}
```

### 4. Enterprise Scaling (Loops)

Terraform

```
# for_each (Iterating over a map or set)
resource "azurerm_subnet" "spoke" {
  for_each             = var.subnets # map(string)
  name                 = each.key
  address_prefixes     = [each.value]
  # ...
}

# dynamic block (Iterating nested blocks inside a resource)
dynamic "security_rule" {
  for_each = local.nsg_rules
  content {
    name                       = security_rule.value.name
    priority                   = security_rule.value.priority
    direction                  = security_rule.value.direction
    # ...
  }
}
```

## Why We Care in DevOps

1. **Incident Response:** During an active production outage (e.g., a locked state file or a corrupted index), engineers do not have time to read documentation. A centralized cheat sheet reduces Mean Time to Recovery (MTTR).
    
2. **Pipeline Standardization:** The core CLI workflow commands listed above form the exact `run` steps inside your standard [[02-GitHub-Actions|GitHub-Actions]] runner.
    
3. **Onboarding:** A standardized cheat sheet aligned to your specific Landing Zone architecture accelerates the onboarding process for new platform engineers.
    

## Interview Questions

- **Q: What is the purpose of `terraform plan -out=tfplan` followed by `terraform apply tfplan` instead of just running `terraform apply`?**
    
    - _A:_ Running `terraform apply` directly performs a new plan and prompts for human approval, which is impossible in an automated CI/CD pipeline. Saving the plan to a file (`-out`) guarantees that the exact execution calculated during the plan phase is what gets applied, eliminating race conditions or unexpected drift between the two steps.
        
- **Q: How do you format all Terraform files in a directory recursively?**
    
    - _A:_ `terraform fmt -recursive`
        
- **Q: You need to inject a variable from the command line that contains a sensitive database password. What is the syntax?**
    
    - _A:_ `terraform plan -var="db_password=SuperSecretPassword123!"` (Though in enterprise pipelines, this should be passed natively as an environment variable via `TF_VAR_db_password` to avoid logging the command).
        

## Links to Implementation

- [[02-Introduction|01-Introduction]]: Return to the beginning.
    
- [[08-State-Management]]: Deep dive into the state manipulation commands.
    
- [[20-Loops-Conditionals|13-Loops-Conditionals]]: Deep dive into `for_each` and `dynamic`.
    
- [[05-Terraform-Pipeline|Terraform-Pipeline]]: Translating these CLI commands into YAML actions.
