---
category: Terraform
tags: [terraform, workspaces, environments, state, architecture]
type: fundamental
status: active
level: beginner
---

# Terraform Workspaces (CLI)

---

## 📖 Before You Read

Before diving into Workspaces, make sure you're comfortable with these ideas:

- ✅ You know what Terraform is (a tool that lets you write code to build cloud infrastructure)
- ✅ You understand what a **State File** is — the file Terraform uses to remember what it already created (like a receipt for your cloud resources)
- ✅ You've seen at least one `.tf` file (a Terraform configuration file written in a language called HCL — HashiCorp Configuration Language)
- ✅ You know what "dev", "qa", and "prod" environments mean (different copies of your app: one for development, one for testing, one for real users)

If any of those are unfamiliar, check out [[08-State-Management]] and [[09-Remote-Backend]] first.

---

## 🤔 What is a Terraform Workspace?

### Plain English Definition

Imagine you work at a coffee shop ☕. You have **one recipe book** for making coffee. But you have **three separate kitchens**:
- Kitchen 1 = where you experiment with new recipes (Development / "dev")
- Kitchen 2 = where you test before opening to the public (Quality Assurance / "qa")
- Kitchen 3 = the real kitchen serving actual customers (Production / "prod")

All three kitchens use **the exact same recipe book**, but they each have **their own separate ingredients, equipment, and inventory lists**.

**Terraform Workspaces work the same way.** You have one set of Terraform configuration files (your "recipe book"), but each workspace keeps its own separate **State File** (its own "inventory list"). This means you can use the **same code** to create separate, isolated environments (dev, qa, prod) without them interfering with each other.

> 💬 **In simple words:** A Workspace is like a named slot that holds a separate "memory" (State File) for your Terraform code.

### The Default Workspace

When you first start using Terraform, you're already inside a workspace — it's called **`default`**. You didn't create it; Terraform creates it automatically. Think of it as the "unnamed kitchen" that's always been there.

---

## 🧠 Why Do We Need Workspaces?

### The Problem Without Workspaces

Imagine you're building a house 🏠. You want to:
1. Build a **test version** of the house first (to check if everything looks right)
2. Then build the **real version** for your family to live in

Without workspaces, Terraform only has one memory (State File). So it would **confuse** your test house with your real house! If you deleted the test house, Terraform might think you want to delete the real house too. 😱

### What Workspaces Solve

Workspaces give each environment (dev, qa, prod) **its own separate State File**. This means:

- ✅ Changes in `dev` won't accidentally affect `prod`
- ✅ You can test infrastructure changes safely before promoting them to production
- ✅ You use **the same code** for all environments (no copy-pasting!)
- ✅ Each environment can have different sizes/configurations using the workspace name as a variable

---

## ⚙️ How Does It Work?

### The Key Commands

Here are the **CLI (Command Line Interface) commands** you'll use. CLI means you type these into a terminal (the black window with text — like PowerShell or Bash):

```bash
# Create a brand new workspace called "dev"
terraform workspace new dev

# See a list of ALL workspaces you have
terraform workspace list

# Switch to an existing workspace called "prod"
terraform workspace select prod

# See which workspace you're currently in
terraform workspace show
```

### What Happens Behind the Scenes?

When you use a **Remote Backend** (a place in the cloud where Terraform stores its State Files — like Azure Blob Storage, which is Microsoft's cloud file storage), Terraform automatically creates separate State Files for each workspace:

```
env:/dev/terraform.tfstate     <- State file for the "dev" workspace
env:/qa/terraform.tfstate      <- State file for the "qa" workspace
env:/prod/terraform.tfstate    <- State file for the "prod" workspace
```

Think of these like three separate filing cabinets 🗄️ — each labeled for a different environment, each storing information only about the resources in that environment.

### Using the Workspace Name Inside Your Code

The magic trick with workspaces is the `terraform.workspace` variable. This is a **built-in variable** (a value Terraform automatically knows) that tells you which workspace is currently active.

You can use it directly in your resource names so each environment gets its own uniquely named resources!

---

## 💡 Real Example

```hcl
# This creates an Azure Resource Group (a folder in Azure that holds related cloud resources)
resource "azurerm_resource_group" "main" {

  # The name of the resource group includes the workspace name automatically
  # terraform.workspace will be "dev", "qa", or "prod" depending on the active workspace
  # So this becomes: "rg-app-dev-eus" or "rg-app-prod-eus"
  name = "rg-app-${terraform.workspace}-eus"
  # The ${...} syntax is called "string interpolation" — it inserts a variable's value into a string

  # All resources in this group will be in the "eastus" (East US) Azure region (data center location)
  location = "eastus"

  # Tags are like sticky labels you put on resources to organize and identify them
  tags = {
    # This tag records which environment this resource belongs to
    # It will automatically say "dev", "qa", or "prod"
    Environment = terraform.workspace
  }
}
```

**What this looks like in practice:**

| Active Workspace | Resource Group Name Created |
|---|---|
| `default` | `rg-app-default-eus` |
| `dev` | `rg-app-dev-eus` |
| `qa` | `rg-app-qa-eus` |
| `prod` | `rg-app-prod-eus` |

### Bonus: Using Workspaces for Different Sizes Per Environment

You can also use workspaces to give dev smaller (cheaper) resources and prod larger (powerful) resources — all in the same code file:

```hcl
# locals is a block where you define values you want to reuse in your code
# Think of locals like "shortcut variables" defined inside your Terraform file
locals {

  # This is a "map" (like a dictionary/lookup table) that maps workspace name to a VM size
  # "VM" = Virtual Machine (a computer running in the cloud)
  vm_sizes = {
    dev  = "Standard_B1s"    # Small, cheap VM — good enough for development
    qa   = "Standard_B2s"    # Medium VM — enough for testing
    prod = "Standard_D4s_v3" # Large, powerful VM — needed for real users
  }

  # This looks up the VM size for the CURRENT workspace
  # So if you're in "dev", vm_size = "Standard_B1s"
  vm_size = local.vm_sizes[terraform.workspace]
}
```

---

## ⚠️ Common Mistakes Beginners Make

### ❌ Mistake 1: Using CLI Workspaces for Production Without Caution

This is the **biggest anti-pattern** (a solution that seems good but causes problems) in Terraform.

Imagine you're working in the `dev` workspace and you've been destroying and recreating resources all day. Now you run:

```bash
terraform workspace select prod   # Oops — you meant to type "qa"
terraform destroy                 # 💀 You just destroyed PRODUCTION
```

Because everything lives in the same directory with the same code, **one wrong command can wipe out production**. This is called a large **"Blast Radius"** — meaning, how much damage a mistake can cause.

### ❌ Mistake 2: Forgetting Which Workspace You're In

Always run `terraform workspace show` before running `plan` or `apply`. It only takes 2 seconds and can save you from disaster.

### ❌ Mistake 3: Using `default` Workspace for Everything

Many beginners just leave everything in the `default` workspace because they don't know workspaces exist. This means all their environments share one State File, which leads to chaos.

---

## 🏗️ The Better Alternative: Directory Separation

Because CLI workspaces have that dangerous blast radius problem, most professional DevOps teams prefer a **Directory Separation** approach instead. This means creating separate folders for each environment:

```
environments/
├── dev/
│   ├── main.tf           <- Dev-specific Terraform config
│   └── terraform.tfvars  <- Dev-specific variable values
├── qa/
│   ├── main.tf           <- QA-specific Terraform config
│   └── terraform.tfvars
└── prod/
    ├── main.tf           <- Prod-specific Terraform config
    └── terraform.tfvars
```

Each folder has its **own backend config**, its **own State File**, and it's **physically impossible** to accidentally run prod commands from the dev folder. See [[10-Modules]] to learn how to share common code between these folders using modules.

---

## 🎯 Key Takeaway

> A Terraform Workspace lets you use the **same `.tf` code** to manage **multiple isolated environments** (dev, qa, prod), each with its own separate State File. But for production systems, consider using **directory separation** instead — it's safer and harder to accidentally destroy things.

---

## ❓ Beginner FAQ

**Q1: Do I have to use workspaces? Can I just have one environment?**
> Absolutely! If you're just learning or building a personal project, the `default` workspace is perfectly fine. Workspaces are designed for teams that need multiple copies of the same infrastructure (like dev vs prod environments).

**Q2: What exactly IS a State File? I keep hearing about it.**
> A State File (usually named `terraform.tfstate`) is a JSON file (a structured text file) that Terraform uses to remember what it has already created. It's like a receipt — it records every cloud resource Terraform manages. Without it, Terraform wouldn't know what exists and what doesn't. See [[08-State-Management]] for a deep dive.

**Q3: What's the difference between Terraform CLI Workspaces and Terraform Cloud Workspaces?**
> Great question! They share a name but are very different:
> - **CLI Workspaces** = Just separate State Files in the same directory/backend. Simple, but dangerous (shared code = shared blast radius).
> - **Terraform Cloud Workspaces** = Fully isolated environments, each with their own Git repository, their own set of variables (like passwords and settings), and their own pipeline (automation) history. Much safer for enterprise use.

**Q4: How do I pass different variable values to different workspaces?**
> Use `terraform.workspace` in a `locals` map lookup! For example:
> ```hcl
> locals {
>   db_size = {
>     dev  = "small"
>     prod = "large"
>   }[terraform.workspace]
> }
> ```
> This picks the right value based on which workspace is active.

**Q5: Will Terraform mess up my prod environment if I run commands from dev workspace?**
> No — as long as you're in the `dev` workspace, Terraform only reads/writes the dev State File. It won't touch prod resources. The danger is only if you **accidentally switch** to the prod workspace before running `terraform destroy`. That's why directory separation (separate folders per environment) is often safer.

---

## 🔗 Links to Related Notes
- [[08-State-Management]]
- [[09-Remote-Backend]]
- [[06-Locals]]
- [[10-Modules]]