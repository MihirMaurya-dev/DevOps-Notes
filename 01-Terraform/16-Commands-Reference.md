---
category: Terraform
tags: [terraform, cli, commands, reference, workflow, state, workspace, fmt, init, plan, apply, destroy, import]
type: reference
status: active
level: beginner-to-intermediate
created: 2026-08-09
updated: 2026-08-09
---

# 🖥️ Terraform Commands — Complete Reference Guide

---

## 📖 Before You Read

This note covers **every Terraform CLI command** you will use — from the very first `terraform init` to advanced state surgery. Each command includes:
- ✅ What it does
- ⚙️ What effect it has on your system / cloud
- ⬅️ What comes before it
- ➡️ What comes after it
- ⚠️ Common mistakes

**Prerequisites:**
- You know what Terraform is → [[01-Introduction]]
- You know what a State File is → [[08-State-Management]]
- You know what a Remote Backend is → [[09-Remote-Backend]]

---

## 🗺️ The Complete Command Flow (Sequence Map)

This is the order in which commands are run in a real-world workflow:

```text
┌─────────────────────────────────────────────────────────────┐
│  SETUP PHASE (one time per project)                         │
│                                                             │
│  terraform init                                             │
│       ↓                                                     │
│  terraform workspace new <name>   (if multi-env)            │
│       ↓                                                     │
│  terraform workspace select <name>                          │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  DAILY DEVELOPMENT PHASE (every time you make changes)      │
│                                                             │
│  terraform fmt                                              │
│       ↓                                                     │
│  terraform validate                                         │
│       ↓                                                     │
│  terraform plan                  (preview)                  │
│       ↓                                                     │
│  terraform apply                 (create/update)            │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  STATE SURGERY PHASE (when things go wrong or you refactor) │
│                                                             │
│  terraform state list                                       │
│  terraform state show <addr>                                │
│  terraform state mv <old> <new>                             │
│  terraform state rm <addr>                                  │
│  terraform import <addr> <azure-id>                         │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  TEARDOWN PHASE (when you want to delete everything)        │
│                                                             │
│  terraform destroy                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Group 1 — Setup Commands

### `terraform init`

```bash
terraform init
```

**What it does:**
This is a **one-time (or as-needed) setup** command that performs three tasks:
1. **Downloads the required Providers** (e.g., the `azurerm` provider — the translator between Terraform and Azure)
2. **Downloads any Modules** referenced in your configuration
3. **Connects to the Remote Backend** (e.g., Azure Storage Account where the state file will be stored)

All downloaded files are saved inside the `.terraform/` directory.

**Effect on system:**
- Creates the `.terraform/` directory (providers and modules are stored here)
- Creates or updates `.terraform.lock.hcl` (locks exact provider versions — similar to `package-lock.json` in Node.js)
- **Nothing is created in Azure** — this is purely local setup

**Before it:**
- Terraform must be installed (`terraform --version` to verify)
- A `provider.tf` or `main.tf` file must exist in the working directory

**After it:**
- `terraform fmt` → `terraform validate` → `terraform plan`

**Common flags:**

| Flag | Purpose |
|------|---------|
| `terraform init -upgrade` | Upgrades providers to the latest allowed version |
| `terraform init -reconfigure` | Re-initializes after a backend configuration change |
| `terraform init -backend-config=backend.conf` | Provides backend config from a separate file (useful in pipelines) |

**Common mistakes:**
- ❌ Running `terraform plan` after a provider version update without running `terraform init -upgrade` first — causes a provider mismatch error
- ❌ Changing the backend configuration but not re-running `terraform init` — Terraform continues connecting to the old state

---

### `terraform workspace new <name>`

```bash
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod
```

**What it does:**
Creates a **new isolated workspace** (environment slot). Each workspace maintains its own separate **State File**, so changes in one environment do not affect another.

> 📦 Analogy: Think of one recipe book (the same Terraform code) and three separate kitchens (dev, staging, prod) — each with their own ingredients (cloud resources).

**Effect on system:**
- Creates a new State File path in the backend (e.g., `env:/dev/terraform.tfstate`)
- Automatically switches to the newly created workspace

**Before it:**
- `terraform init` must have been run

**After it:**
- `terraform workspace select <name>` → `terraform plan`

**Common mistake:**
- ❌ Creating a workspace but not verifying the active workspace with `terraform workspace show` before running `apply` — resources may be created in the wrong environment

---

### `terraform workspace select <name>`

```bash
terraform workspace select prod
```

**What it does:**
Switches to an existing workspace. All subsequent `plan` and `apply` commands will use the State File belonging to the selected workspace.

**Effect on system:**
- No resources are created or deleted
- Only the active workspace pointer is updated

**Before it:**
- The target workspace must already exist (verify with `terraform workspace list`)

**After it:**
- `terraform workspace show` (confirm the active workspace) → `terraform plan`

> ⚠️ **DANGER:** Never run `terraform destroy` immediately after switching to the `prod` workspace without carefully reviewing the plan first. This can wipe out the entire production environment.

---

### `terraform workspace list`

```bash
terraform workspace list
```

**Example output:**
```
  default
* dev
  staging
  prod
```
(`*` marks the currently active workspace)

**What it does:** Lists all available workspaces. Run this before switching to confirm available options.

---

### `terraform workspace show`

```bash
terraform workspace show
```

**Example output:**
```
dev
```

**What it does:** Prints the name of the currently active workspace. Always run this before `plan` or `apply` to confirm you are in the correct environment.

---

## ✍️ Group 2 — Code Quality Commands

### `terraform fmt`

```bash
terraform fmt
```

**What it does:**
Automatically rewrites `.tf` files in the **canonical Terraform format** — fixing indentation, aligning equals signs, and standardizing whitespace across the codebase.

```bash
# Format only the current directory
terraform fmt

# Format all subdirectories recursively (including modules)
terraform fmt -recursive

# Check formatting without making changes (used in pipelines)
terraform fmt -check -recursive
```

**Effect on system:**
- `.tf` files are modified in-place
- **Nothing changes in Azure**
- Only whitespace and indentation changes appear in `git diff`

**Before it:**
- After writing or modifying `.tf` files, before committing to Git

**After it:**
- `terraform validate`

**Real-world use (before a commit):**
```bash
terraform fmt -recursive
git add .
git commit -m "feat: add vnet module"
```

**Pipeline use:**
```yaml
# Fail the pipeline if any file is not properly formatted
- run: terraform fmt -check -recursive
```

> 💡 The `-check` flag does **not** modify files. It exits with code `1` if formatting is incorrect — this is how pipelines enforce formatting standards without altering source files.

---

### `terraform validate`

```bash
terraform validate
```

**What it does:**
Checks the Terraform configuration for **syntax errors and internal consistency** — without connecting to Azure or any remote service.

It validates:
- ✅ HCL syntax is correct
- ✅ All required arguments are provided for each resource
- ✅ Variable types are consistent with their usage
- ✅ Resource references (e.g., `azurerm_resource_group.main.name`) point to valid resources

**Effect on system:**
- **Nothing changes in Azure**
- Only a local static analysis of the configuration is performed

**Before it:**
- `terraform init` must have been run (providers are needed for type-checking)
- `terraform fmt` (validate clean, well-formatted code)

**After it:**
- `terraform plan`

**Example output:**
```
Success! The configuration is valid.
```

**Common mistake:**
- ❌ `validate` passes but `plan` fails — this is expected and correct behaviour. `validate` only checks **syntax and structure**. If `location = var.location` is syntactically correct, it passes — even if the variable value is invalid or the Azure region does not exist. Only `plan` communicates with Azure and catches those runtime issues.

---

## 🔍 Group 3 — Planning Commands

### `terraform plan`

```bash
terraform plan
```

**What it does:**
Performs a **dry run** — Terraform calculates exactly what it would do if `apply` were run right now, without making any actual changes. The output uses symbols to indicate the type of each change:

```
+ resource will be CREATED   (green)
~ resource will be CHANGED   (yellow)
- resource will be DESTROYED (red)
```

Terraform determines this by comparing the current **State File** (what currently exists in Azure) with your **code** (what should exist).

**Effect on system:**
- **Nothing changes in Azure**
- **Nothing changes in the State File**
- A local execution plan is generated and displayed

**Before it:**
- `terraform init` ✅
- `terraform validate` ✅

**After it:**
- Review the output carefully — confirm every change is expected
- `terraform apply` (proceed if the plan looks correct)

**Important flags:**

| Flag | Purpose |
|------|---------|
| `terraform plan -out=tfplan` | Saves the plan to a binary file (essential for CI/CD) |
| `terraform plan -var="location=eastus"` | Overrides a single variable value inline |
| `terraform plan -var-file="prod.tfvars"` | Loads variable values from a specific `.tfvars` file |
| `terraform plan -target=azurerm_resource_group.main` | Generates a plan for only one specific resource |
| `terraform plan -refresh-only` | Detects infrastructure drift without proposing code changes |
| `terraform plan -destroy` | Previews what would be deleted if `terraform destroy` were run |

**Why `-out=tfplan` is critical:**

```bash
# Without -out: a NEW internal plan is generated at apply time
terraform plan
terraform apply   # Generates a brand-new plan — state could have changed in between

# With -out: the exact reviewed plan is applied — no surprises
terraform plan -out=tfplan
terraform apply tfplan   # Applies precisely what was reviewed and approved
```

> 💡 **Production rule:** Always use `-out=tfplan`, especially in CI/CD pipelines. This ensures the plan the reviewer approved is exactly what gets executed.

---

## 🚀 Group 4 — Apply Commands

### `terraform apply`

```bash
terraform apply
```

**What it does:**
Executes the Terraform plan — this **actually creates, modifies, or deletes resources in Azure**.

By default, Terraform displays the plan and prompts for explicit confirmation:
```
Do you want to perform these actions? (yes/no)
```

**Effect on system:**
- ✅ Resources are created, updated, or deleted in Azure
- ✅ The State File is updated to reflect the new infrastructure state
- ✅ Adding `-auto-approve` skips the confirmation prompt (required for unattended pipeline execution)

**Before it:**
- `terraform plan` — always review the plan before applying

**After it:**
- `terraform state list` — confirm all resources are correctly tracked
- `az resource list` — optionally verify directly in Azure

**Important flags:**

| Flag | Purpose |
|------|---------|
| `terraform apply tfplan` | Applies a previously saved plan file (recommended approach) |
| `terraform apply -auto-approve` | Skips the interactive confirmation prompt (for pipelines) |
| `terraform apply -var-file="prod.tfvars"` | Loads variable values from a specific file |
| `terraform apply -target=resource.name` | Applies changes to only one specific resource |
| `terraform apply -parallelism=5` | Sets how many resources are processed in parallel (default: 10) |

**Standard CI/CD pipeline pattern:**
```bash
# In the Plan job:
terraform plan -out=tfplan

# In the Apply job (using the exact same reviewed plan):
terraform apply -auto-approve tfplan
```

**Common mistakes:**
- ❌ Running `terraform apply` without first reviewing a `plan` — unexpected resource deletions can occur
- ❌ Forgetting `-auto-approve` in a pipeline — the pipeline hangs indefinitely waiting for interactive input
- ❌ Applying to the wrong environment because the workspace was not verified beforehand

---

## 🗂️ Group 5 — State Commands

> ⚠️ **Warning:** State commands directly modify Terraform's infrastructure memory. Always create a backup before proceeding:
> ```bash
> terraform state pull > backup.tfstate
> ```

### `terraform state list`

```bash
terraform state list
```

**What it does:**
Displays a list of **all resources currently tracked** in the State File.

**Example output:**
```
azurerm_resource_group.main
azurerm_virtual_network.hub
module.vnet.azurerm_subnet.main
module.vm.azurerm_linux_virtual_machine.this
```

**Effect on system:**
- Read-only — nothing is modified
- Azure and the State File remain unchanged

**When to use:**
- After `apply`, to confirm all resources were successfully registered in state
- Before state surgery, to find the exact resource address to target
- After `import`, to verify the resource was added correctly

**Before it:** `terraform apply` (typically)
**After it:** `terraform state show <address>` for a detailed view of a specific resource

---

### `terraform state show <address>`

```bash
terraform state show azurerm_resource_group.main
```

**What it does:**
Displays the **complete details of one specific resource** exactly as stored in the State File — including the Azure resource ID, all attributes, and metadata.

**Example output:**
```hcl
# azurerm_resource_group.main:
resource "azurerm_resource_group" "main" {
    id       = "/subscriptions/xxxx/resourceGroups/rg-myapp"
    location = "eastus"
    name     = "rg-myapp"
    tags     = {}
}
```

**Effect on system:** Read-only — nothing is modified

**When to use:**
- To retrieve the exact Azure resource ID (required for `terraform import`)
- To verify a resource's tracked state matches its real state in Azure
- For debugging when `plan` shows unexpected changes

---

### `terraform state mv <old-address> <new-address>`

```bash
terraform state mv azurerm_resource_group.old_name azurerm_resource_group.new_name
```

**What it does:**
**Renames a resource's address in the State File** — without deleting or recreating anything in Azure.

**Real-world scenario:**

Your code previously had:
```hcl
resource "azurerm_resource_group" "rg" { ... }
```
You renamed it in code to:
```hcl
resource "azurerm_resource_group" "main" { ... }
```

If you run `terraform plan` now, Terraform interprets this as:
- Delete `azurerm_resource_group.rg`
- Create `azurerm_resource_group.main`

But you want to keep the existing Azure resource — only the local name in code changed. The fix:

```bash
# Inform Terraform that this is the same resource under a new name
terraform state mv azurerm_resource_group.rg azurerm_resource_group.main
```

**Effect on system:**
- The resource's address is updated in the State File
- **Nothing changes in Azure** — the resource remains exactly as it is
- The next `terraform plan` will show no changes for this resource

**Before it:** `terraform state list` — find the exact current address
**After it:** `terraform plan` — confirm no unexpected changes remain

---

### `terraform state rm <address>`

```bash
terraform state rm azurerm_resource_group.main
```

**What it does:**
**Removes a resource's entry from the State File** — it does **NOT delete the resource from Azure**.

**When to use:**
- You want to stop managing a resource with Terraform and switch to manual management
- A state entry is corrupted or stuck and needs to be cleared for a fresh start
- You are restructuring modules and need to temporarily remove and re-import entries

**Effect on system:**
- The resource entry is removed from the State File
- The actual resource in Azure remains **completely intact and operational**
- On the next `terraform plan`, Terraform will treat this as a new resource and propose creating it (if it still exists in code)

> 💡 `state rm` ≠ `destroy`. The Azure resource is never modified or deleted.

**Before it:** `terraform state list` — confirm the exact resource address
**After it:** `terraform plan` — review the impact of the removal

---

### `terraform import <address> <azure-resource-id>`

```bash
terraform import azurerm_resource_group.main \
  /subscriptions/xxxx/resourceGroups/rg-existing
```

**What it does:**
**Brings an existing Azure resource under Terraform management** — without deleting or recreating it.

**Real-world scenario:**
- A Resource Group was created manually in the Azure Portal
- You want Terraform to manage it going forward

**Step-by-step process:**
```bash
# Step 1: Write the resource block in your .tf file first
# main.tf:
# resource "azurerm_resource_group" "main" {
#   name     = "rg-existing"
#   location = "eastus"
# }

# Step 2: Retrieve the Azure resource ID
az group show --name rg-existing --query id -o tsv
# Output: /subscriptions/xxxx/resourceGroups/rg-existing

# Step 3: Import the existing resource into state
terraform import azurerm_resource_group.main \
  /subscriptions/xxxx/resourceGroups/rg-existing

# Step 4: Verify it was imported correctly
terraform state show azurerm_resource_group.main

# Step 5: Run plan — it should show zero differences
terraform plan
```

**Effect on system:**
- A new entry is added to the State File linking the Azure resource to the code
- The resource in Azure remains **completely unchanged**
- If the properties in your code do not exactly match the real Azure resource, `plan` will show the differences as proposed changes

**Before it:** The resource block must exist in your `.tf` files before running import
**After it:** `terraform plan` — verify there are no unexpected differences

**Common mistake:**
- ❌ Not checking `plan` after import — if code properties mismatch the real resource, the next `apply` may delete and recreate it

---

## 💥 Group 6 — Destroy Commands

### `terraform destroy`

```bash
terraform destroy
```

**What it does:**
**Permanently deletes all resources tracked in the State File from Azure**.

```
Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure,
  as shown above. There is no undo. Only 'yes' will be accepted.

  Enter a value: yes
```

**Effect on system:**
- ✅ All resources listed in the State File are permanently deleted from Azure
- ✅ The State File becomes empty
- ❌ **There is no undo** — deleted resources cannot be recovered

**Targeted destroy (delete only one specific resource):**
```bash
terraform destroy -target=azurerm_resource_group.dev_rg
```

**Before it:**
- `terraform plan -destroy` — always preview what will be deleted before confirming

**After it:**
- All managed infrastructure has been permanently removed

**When to use:**
- Cleaning up dev or test environments after use
- Reducing costs by tearing down non-production resources outside business hours
- Complete decommissioning of a project or environment

> 🚨 **Never run `terraform destroy` against production** without an explicit, deliberate decision and a thorough review of the destroy plan output.

---

## 🔧 Group 7 — Utility Commands

### `terraform output`

```bash
terraform output
terraform output resource_group_name
```

**What it does:**
Prints the **output values defined in `outputs.tf`**, reading them directly from the State File — no Azure API call is made.

**Example:**
```bash
terraform output vnet_id
# /subscriptions/xxxx/resourceGroups/rg-main/providers/Microsoft.Network/virtualNetworks/vnet-main
```

**When to use:**
- Passing Azure resource IDs to other modules or external scripts
- Transferring data between CI/CD pipeline stages (e.g., passing a VNet ID from a networking job to an AKS job)
- Manual verification that the correct resources were created after `apply`

**Effect on system:** Read-only — nothing is modified

---

### `terraform refresh` *(Deprecated — do not use)*

```bash
# DEPRECATED — avoid this command
terraform refresh

# Use these instead:
terraform plan -refresh-only
terraform apply -refresh-only
```

**What it did:** Synced the State File with the actual live state of Azure resources.

**Why it was deprecated:** It silently applied changes to the State File without showing a preview first, which could introduce unexpected behaviour. The replacement (`-refresh-only`) shows a plan of the detected drift before you decide whether to accept it.

---

### `terraform force-unlock <lock-id>`

```bash
terraform force-unlock abc123def456
```

**What it does:**
Manually releases a **stuck state lock**. This is needed when a pipeline crashes mid-execution and fails to release the lock it acquired.

**When to use:**
When `terraform plan` or `terraform apply` returns:
```
Error: Error locking state: Error acquiring the state lock
```

```bash
# The lock ID is printed in the error message — copy it from there
terraform force-unlock <lock-id-from-error>
```

> ⚠️ Only use this command when you are absolutely certain no other process is actively reading or writing the state. Forcing an unlock while another operation is in progress can corrupt the State File.

---

### `terraform version`

```bash
terraform version
```

**Example output:**
```
Terraform v1.9.5
on windows_amd64
```

**When to use:** Confirm the installed Terraform version — useful when troubleshooting compatibility issues with providers or pipeline environments.

---

## 📋 Quick Reference Table — All Commands at a Glance

| Command | Phase | Azure Effect | State Effect |
|---------|-------|-------------|--------------|
| `terraform init` | Setup | ❌ None | Downloads providers/modules |
| `terraform workspace new` | Setup | ❌ None | New state slot created |
| `terraform workspace select` | Setup | ❌ None | Active workspace pointer updated |
| `terraform workspace list` | Info | ❌ None | ❌ None |
| `terraform workspace show` | Info | ❌ None | ❌ None |
| `terraform fmt` | Code Quality | ❌ None | ❌ None |
| `terraform validate` | Code Quality | ❌ None | ❌ None |
| `terraform plan` | Preview | ❌ None | ❌ None |
| `terraform apply` | Execute | ✅ Creates / Updates / Deletes | ✅ Updated |
| `terraform destroy` | Teardown | ✅ Deletes ALL | ✅ Emptied |
| `terraform state list` | State Ops | ❌ None | Read-only |
| `terraform state show` | State Ops | ❌ None | Read-only |
| `terraform state mv` | State Ops | ❌ None | ✅ Address renamed |
| `terraform state rm` | State Ops | ❌ None | ✅ Entry removed |
| `terraform import` | State Ops | ❌ None | ✅ Entry added |
| `terraform output` | Info | ❌ None | Read-only |
| `terraform force-unlock` | Emergency | ❌ None | ✅ Lock released |

---

## 🔁 Full Real-World Flow — Feature Branch to Production

```bash
# ─── LOCAL: First-time setup ───
git clone https://github.com/org/repo.git
cd repo
git checkout -b feature/add-vnet

# ─── TERRAFORM SETUP ───
terraform init
terraform workspace new dev        # or use select if it already exists
terraform workspace select dev
terraform workspace show           # confirm active workspace is: dev

# ─── CODE QUALITY ───
terraform fmt -recursive
terraform validate

# ─── PREVIEW ───
terraform plan -out=tfplan
# Review every + / ~ / - line in the output before proceeding

# ─── APPLY (dev environment) ───
terraform apply tfplan

# ─── VERIFY ───
terraform state list
terraform output

# ─── GIT ───
git add .
git commit -m "feat: add VNet module"
git push origin feature/add-vnet

# ─── PR raised → reviewed → approved → merged to main ───

# ─── CI/CD PIPELINE RUNS AUTOMATICALLY ON MAIN ───
# terraform init
# terraform fmt -check -recursive
# terraform validate
# terraform plan -out=tfplan
# [Manual Approval Gate — reviewer inspects the plan output]
# terraform apply -auto-approve tfplan
```

---

## 🎤 Interview Answers

**Q: What is the basic Terraform workflow?**
> *"The standard Terraform workflow has three core steps — `init`, which downloads providers and connects to the remote backend; `plan`, which generates a preview of all proposed changes without modifying any infrastructure; and `apply`, which executes those changes in the cloud. Best practice is to always save the plan with `-out=tfplan` and then apply that exact file, ensuring that what was reviewed and approved is precisely what gets deployed."*

**Q: What is the difference between `terraform state rm` and `terraform destroy`?**
> *"`terraform destroy` permanently deletes the actual resource from Azure. `terraform state rm` only removes the resource's entry from Terraform's State File — the resource itself remains completely untouched in Azure. It is used when you want to stop managing a resource with Terraform, or when performing state surgery during a module refactoring."*

**Q: When would you use `terraform import`?**
> *"When a resource was created manually in the Azure Portal or via CLI and you want Terraform to manage it going forward. You first write the corresponding resource block in your `.tf` files, then run `terraform import` with the resource's Azure resource ID to link the existing infrastructure to your code — without destroying and recreating it."*

**Q: Why use `terraform plan -out=tfplan` instead of just running `terraform apply`?**
> *"Running `terraform apply` directly generates a new internal plan at apply time, which means infrastructure state could have changed between when you reviewed the plan and when execution actually runs. Saving the plan with `-out=tfplan` and then running `terraform apply tfplan` guarantees that exactly the plan that was reviewed and approved is what gets applied — no surprises, no drift between review and execution."*

---

## 🔗 Related Notes

- [[01-Introduction]] — What is Terraform?
- [[08-State-Management]] — State file deep dive
- [[09-Remote-Backend]] — Azure remote backend setup
- [[11-Workspaces]] — Workspace commands in detail
- [[Cheat-Sheet]] — Ultra-quick command reference card
- [[Terraform-Pipeline]] — How these commands are used in a CI/CD pipeline (Azure DevOps)
- [[GitHub-Actions-Terraform-OIDC]] — How these commands are used in GitHub Actions with Azure OIDC
