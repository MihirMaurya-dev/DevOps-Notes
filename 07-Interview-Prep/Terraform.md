---
tags: [interview, prep, terraform, questions]
source: devopsinsiders/batch-18
updated: 2026-07-26
---

# Terraform Interview Questions

A collection of comprehensive interview questions regarding Infrastructure as Code using Terraform, ranging from basics to scenario-based.

---

## Basics

### Q1: What is Terraform and what problem does it solve?
**A:** Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp. It allows you to define, provision, and manage cloud infrastructure using a declarative configuration language (HCL). It solves the problem of manual infrastructure management by making deployments reproducible, version-controllable, scalable, and self-documenting.

### Q2: What are the core stages of the Terraform workflow?
**A:** 
1. **Write:** Authoring infrastructure configuration in `.tf` files.
2. **Init:** Running `terraform init` to download required providers and initialize the backend.
3. **Plan:** Running `terraform plan` to generate an execution plan showing what resources will be created, updated, or deleted.
4. **Apply:** Running `terraform apply` to execute the plan and provision real resources.

### Q3: What is a Terraform Provider?
**A:** A provider is a plugin that Terraform uses to interact with cloud platforms and other APIs. It translates Terraform HCL code into API calls for the target platform. For this course, we use the `azurerm` provider which translates configuration into Azure Resource Manager (ARM) API calls to create and manage Azure resources like VNets, VMs, and AKS clusters.

### Q4: What is the `terraform.tfstate` file?
**A:** The state file is a JSON file where Terraform maps your configured resources to the real-world infrastructure instances. It tracks metadata, resource dependencies, and configuration parameters. Terraform uses this state to determine what changes need to be made during the next `apply` operation.

### Q5: What is the difference between a Variable and a Local in Terraform?
**A:** 
- **Variables (`variable`):** Are dynamic inputs to a Terraform module. Their values can be provided by users at runtime via `.tfvars` files, environment variables, or CLI arguments.
- **Locals (`locals`):** Are internal variables defined within the code to reduce repetition and complex expressions. They are scoped locally and cannot be overridden by users at runtime.

### Q6: How do you pass inputs to Terraform without user interaction?
**A:** You can use a `.tfvars` file (e.g., `terraform apply -var-file="prod.tfvars"`), or use environment variables prefixed with `TF_VAR_` (e.g., `export TF_VAR_location="eastus"`). You can also pass variables directly in the CLI using the `-var` flag.

### Q7: What are Terraform Modules?
**A:** Modules are self-contained packages of Terraform configurations that are managed as a group. They enable reusability, allowing you to define a standard pattern (like an AKS cluster setup) and instantiate it multiple times across different environments by simply changing the input variables.

---

## Intermediate

### Q8: How do you handle Terraform state in a multi-developer team?
**A:** You configure a **Remote Backend** to store the state file centrally in an **Azure Storage Account blob container**. This ensures all team members and CI/CD pipelines use the exact same state. Crucially, Azure Blob Storage natively supports **State Locking** via blob lease — it prevents two concurrent `terraform apply` executions from running simultaneously and corrupting the state.

### Q9: What is the difference between `count` and `for_each`?
**A:** Both create multiple instances of a resource. 
- **`count`** uses an integer index (0, 1, 2...). If an item is removed from the middle of the list, indexes shift, causing Terraform to destroy and recreate subsequent resources unnecessarily.
- **`for_each`** uses a map key or set string as an identifier. Adding or removing elements only impacts that specific key, making it far safer for named infrastructure resources.

### Q10: How do you handle sensitive values in Terraform without hardcoding them?
**A:** You declare a variable and mark it with `sensitive = true`, preventing its value from displaying in CLI logs. You then provide the value dynamically via environment variables or CI/CD secrets. Better yet, you can use data sources like `data "azurerm_key_vault_secret"` to dynamically retrieve the secret during runtime.

### Q11: Explain the `lifecycle` meta-argument and its common options.
**A:** The `lifecycle` block controls how Terraform creates, updates, and deletes resources, overriding default behaviors.
- `create_before_destroy`: Creates the replacement resource before deleting the old one, minimizing downtime.
- `prevent_destroy`: Returns an error if a plan attempts to delete the resource, protecting critical assets like databases.
- `ignore_changes`: Tells Terraform to ignore drift on specific attributes (e.g., tags updated by a different process).

### Q12: What is the difference between `terraform taint` and `terraform apply -replace`?
**A:** Both are used to force Terraform to destroy and recreate a specific resource. 
- `terraform taint` is an older, deprecated command that manually marked a resource as tainted in the state file, requiring a subsequent `apply`.
- `terraform apply -replace="<resource>"` is the modern, single-step approach to force replacement without permanently modifying the state first.

### Q13: What are Terraform Data Sources?
**A:** Data sources allow Terraform to fetch data computed elsewhere or infrastructure created outside of the current Terraform configuration. For example, you can use a data source to fetch the ID of an existing Virtual Network to deploy new VMs into it, without having Terraform manage the Virtual Network itself.

### Q14: How does `terraform import` work?
**A:** `terraform import` allows you to bring existing, manually created infrastructure under Terraform management. You provide the Terraform resource address and the cloud provider ID. Terraform will fetch the current state from the cloud provider and add it to the state file. You still need to manually write the matching HCL configuration block (unless using the newer `import` blocks in TF 1.5+).

### Q15: What is a Provisioner in Terraform?
**A:** Provisioners (like `local-exec` or `remote-exec`) execute scripts on a local or remote machine as part of resource creation or destruction. HashiCorp considers them a "last resort." It's generally better to use native cloud configuration tools like cloud-init, Ansible, or Packer instead.

---

## Advanced

### Q16: How do you structure a complex multi-environment Terraform project?
**A:** A common best practice is to separate environments into different directories (e.g., `environments/dev`, `environments/prod`), each with its own remote state file backend configuration. These root configurations then call versioned, shared modules stored in a separate `modules/` directory or a private module registry. This ensures strict isolation of state between environments.

### Q17: What is Terraform Workspaces and when should you use them?
**A:** Workspaces allow you to manage multiple distinct state files from the same working directory and configuration files. Running `terraform workspace new dev` creates a separate state environment. While useful for local testing, they are generally discouraged for separating production from development in large teams; directory-based separation provides clearer isolation and visibility.

### Q18: Are sensitive values encrypted in the Terraform state file?
**A:** **No.** Terraform state stores all values, including those marked as `sensitive`, in plain text. This is a critical security consideration. To mitigate this, you must store the state file in a secure remote backend with encryption at rest (like an Azure Storage Account) and strictly limit RBAC access to the backend to only the CI/CD pipeline identity.

### Q19: What is a dynamic block in Terraform?
**A:** A `dynamic` block allows you to programmatically generate nested configuration blocks (like `ingress` rules in a security group) based on an iterable collection (like a list or map). It prevents you from having to hardcode repetitive blocks inside a resource definition.

### Q20: How do you upgrade a major Terraform provider version safely?
**A:** First, read the provider's upgrade guide for deprecations and breaking changes. Update the `required_providers` version constraint and run `terraform init -upgrade` to download the new plugin. Carefully review `terraform plan`; if there are unexpected changes, you may need to update your `.tf` configuration or use the `terraform state mv` command to align with syntax changes before applying.

### Q21: What is the `null_resource` and the newer `terraform_data` resource?
**A:** `null_resource` was historically used to run provisioners or orchestrate triggers without creating a physical cloud asset. In modern Terraform (1.4+), `terraform_data` replaces it as a built-in resource. It is useful for triggering actions when a variable changes or storing data that forces a lifecycle event on another resource.

### Q22: What happens if a Terraform apply fails midway?
**A:** Terraform tracks everything it successfully created in the state file before the failure occurred. Running `terraform plan` again will compare the partially applied state with your configuration and attempt to pick up where it left off, creating the remaining resources or highlighting configuration errors.

---

## Scenario-Based

### Q23: Scenario: A developer manually changed a security group rule in the Azure Portal. What happens on the next `terraform plan`?
**A:** Terraform will detect "configuration drift." During the refresh phase of the plan, it reads the real-world infrastructure and compares it against the `.tf` configuration. It will propose an update to modify the security group back to the state defined in the code, reverting the manual change.

### Q24: Scenario: Your Terraform state file lock gets stuck after a pipeline crash. How do you resolve it?
**A:** 
First, ensure that no other processes or pipelines are actively running Terraform. Then, obtain the lock ID from the error message. You can use the `terraform force-unlock <LOCK_ID>` command to forcefully remove the lock. In Azure Storage, you can also manually break the lock lease on the blob file via the Azure Portal or CLI.

### Q25: Scenario: You need to rename a resource in your HCL code without destroying and recreating the actual cloud resource. How?
**A:** 
You use the `terraform state mv` command to update the address of the resource in the state file to match the new name in your code. 
Example: `terraform state mv azurerm_resource_group.old_name azurerm_resource_group.new_name`. 
In TF 1.1+, you can use the declarative `moved` block directly in your `.tf` files to achieve this safely within version control.

### Q26: Scenario: Your CI/CD pipeline failed because it says a resource already exists, but it's not in your state file. What do you do?
**A:** 
This means the resource was created out-of-band (e.g., via the portal) but has the same name as the one Terraform is trying to create. You should run `terraform import` to pull the existing resource into your state file. Then, ensure your `.tf` configuration perfectly matches the existing resource attributes so that a subsequent `terraform plan` shows zero changes.

### Q27: Scenario: You want to deploy infrastructure to multiple regions simultaneously while reusing the same modules. How?
**A:** 
I would declare multiple provider blocks in the root configuration, setting a distinct `alias` for each (e.g., `alias = "westus"`). When invoking the modules, I would explicitly pass the aliased provider into the module block using the `providers` argument (e.g., `providers = { azurerm = azurerm.westus }`).

### Q28: Scenario: The state file was accidentally deleted from the remote backend. How do you recover?
**A:** 
First, I would attempt to recover the state file from the remote backend's backup or versioning system (e.g., Blob Storage versioning). If versions are not enabled, recovery is highly manual. I would need to write matching configuration code and run `terraform import` for every single deployed resource to rebuild the state file from scratch. This highlights the absolute necessity of enabling versioning on state storage containers.

---

## From Recent Interviews (July 2026)

### Q29: What is the `moved` block in Terraform and when would you use it?
**A:** The `moved` block (introduced in TF 1.1) is a declarative way to rename a resource or move it into a module without destroying and recreating the actual cloud resource. You add it directly in your `.tf` files so the rename is tracked in version control.
```hcl
moved {
  from = azurerm_resource_group.old_name
  to   = azurerm_resource_group.new_name
}
```
Unlike `terraform state mv` (which is a one-time CLI command), the `moved` block documents the change for the whole team.

### Q30: What is linting in Terraform? Name a tool and what it catches.
**A:** Linting statically analyzes `.tf` code before it is applied. **TFLint** is the most common tool. It catches:
- Provider-specific errors (e.g., invalid Azure VM sizes like `Standard_ZZZ`).
- Deprecated syntax or arguments.
- Unused variables and declarations.
- Missing required variables.
It does NOT require cloud credentials and runs in the CI Validate stage before `terraform plan`.

### Q31: What is the difference between `variable.tf` and `terraform.tfvars`?
**A:**
- `variables.tf` (or `variable.tf`): **Declares** variables — their name, type, description, and optional default value. It's the schema.
- `terraform.tfvars`: **Assigns values** to declared variables. It's the data. You can have multiple `.tfvars` files (e.g., `dev.tfvars`, `prod.tfvars`) and pass them using `terraform apply -var-file="prod.tfvars"`.

### Q32: What is a pattern module vs a resource module in Terraform?
**A:**
- **Resource Module**: Provisions one specific cloud resource type (e.g., a module that creates only a Storage Account). Thin, reusable, and single-purpose.
- **Pattern Module** (also called an Architecture or Composition Module): Orchestrates multiple resource modules together to deploy a complete architecture (e.g., a "Web App" pattern that calls the VNet module + App Service module + Key Vault module). It represents a business-level template.

### Q33: What logging levels does Terraform support, and how do you enable them?
**A:** Set the `TF_LOG` environment variable to one of: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`. `TRACE` is the most verbose and is used for deep debugging of provider API calls. Logs are written to stderr by default, or to a file using `TF_LOG_PATH`.
```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log
terraform apply
```

### Q34: After which Terraform command is the state file first created?
**A:** The state file is created after the first successful **`terraform apply`**. `terraform init` creates the `.terraform/` directory and downloads providers. `terraform plan` reads state but does not write to it. Only `apply` actually creates/modifies the `terraform.tfstate`.

### Q35: At what stage does Terraform download modules and providers?
**A:** During **`terraform init`**. It reads the `required_providers` block and the `module` source blocks, downloads providers into `.terraform/providers/`, and downloads modules into `.terraform/modules/`.

### Q36: If a variable is marked as `sensitive = true`, can it still appear in `terraform state`?
**A:** Yes. `sensitive = true` only masks the value from **CLI plan/apply output logs**. The value is still stored in **plain text** in the state file. This is why state files must be encrypted at rest and access-controlled via RBAC. To truly protect it, retrieve it from Azure Key Vault via a data source at runtime instead of storing it in state.

### Q37: If you pass a value hardcoded in a resource (e.g., a VM password), will it show in `terraform plan`?
**A:** Yes, hardcoded sensitive values in resource blocks will appear in `terraform plan` output in plain text (unless the argument itself is marked sensitive by the provider). This is a security risk. Always use `variable` with `sensitive = true` or a Key Vault data source instead.

### Q38: What is the purpose of Terraform Workspaces, and when should you avoid them?
**A:** Workspaces create isolated state files from the same configuration directory (e.g., `dev` and `staging` workspaces). They are useful for testing changes in a parallel, ephemeral environment. **Avoid for Production separation**: Using `terraform.workspace` as conditionals in code leads to complex, error-prone configurations. Directory-based separation (`environments/dev/`, `environments/prod/`) is safer and clearer for distinct production environments.

### Q39: How do you create 10 Storage Accounts across 10 different subscriptions with a single pipeline?
**A:** Use a matrix/loop strategy in the pipeline (e.g., `strategy: matrix` in GitHub Actions or a `foreach` loop in ADO). Each iteration passes a different subscription ID as an environment variable. The Terraform code uses `provider "azurerm"` with the `subscription_id` passed via `TF_VAR_subscription_id`. Alternatively, use `for_each` with a map of subscription IDs in Terraform if managed with the `azurerm` provider aliasing pattern.

### Q40: What are the `lifecycle` block arguments that can be used inside a resource block?
**A:** The main arguments are:
- `create_before_destroy = true`: Creates replacement before deleting the old resource (for zero-downtime updates).
- `prevent_destroy = true`: Throws an error if `plan` includes destroying this resource (protects databases).
- `ignore_changes = [tags, some_attribute]`: Ignores drift on specific attributes managed by other processes.
- `replace_triggered_by = [resource.other]`: Forces replacement if another referenced resource changes.
