---
category: Terraform
tags: [terraform, data-sources, hcl, fundamentals, data-flow]
type: fundamental
status: active
level: beginner
---

# Terraform Data Sources

---

## 📖 Before You Read

To get the most out of this note, you should already be familiar with:

- ✅ What a Terraform **resource block** is — a block of code that tells Terraform to **create** something in the cloud (like a server or a network)
- ✅ What **HCL (HashiCorp Configuration Language)** is — the language you write Terraform code in (it's the language inside `.tf` files)
- ✅ What an **API (Application Programming Interface)** is — basically a way for programs to ask each other questions (e.g., "Hey Azure, what's the ID of this resource?")
- ✅ What a **variable** is — a named placeholder that holds a value you can change (like `var.location`)

If any of these feel shaky, check out [[04-Resources]] and [[05-Variables]] first.

---

## 🤔 What is a Data Source?

### Plain English Definition

Think of a Terraform **resource block** like going to IKEA and **buying** a new bookshelf. You own it. You assemble it. You can take it apart later. Terraform manages its entire lifecycle.

A **Data Source**, on the other hand, is like going to a **library** 📚 to **look up information** about a bookshelf that already exists. You don't buy it. You don't own it. You just read the information about it and use that information elsewhere.

> 💬 **In simple words:** A Data Source is Terraform's way of asking "Hey cloud, does this thing exist? If yes, tell me its details." It **reads** information — it never **creates, updates, or deletes** anything.

### The Read vs. Write Distinction

| Concept         | HCL Block Used   | What It Does                          | Terraform Manages It? |
| --------------- | ---------------- | ------------------------------------- | --------------------- |
| **Resource**    | `resource "..."` | Creates/Updates/Destroys cloud things | ✅ Yes                 |
| **Data Source** | `data "..."`     | Reads existing cloud things           | ❌ No                  |

This is one of the most important distinctions in Terraform. Resources are "write" operations. Data sources are "read-only" operations.

---

## 🧠 Why Do We Need Data Sources?

### The Problem They Solve

Imagine your company has a large Azure cloud environment:
- The **networking team** owns and manages the Hub Virtual Network (VNet) — a private network in Azure that connects everything.
- The **app team** needs to deploy their application inside that network.

The app team doesn't have permission to touch the networking team's resources. But they need to **know the ID and properties** of that network to connect to it.

Without Data Sources, the app team would have to:
1. Ask the networking team to send them the VNet ID via email 📧
2. Hardcode (manually type) that ID into their Terraform code
3. Update it every time the networking team makes changes

That's messy, error-prone, and doesn't scale. 😤

### The Data Source Solution

With Data Sources, the app team can write code like this:

> "Hey Azure API, look up the existing VNet called 'vnet-hub-prod'. Tell me its ID and location."

Terraform fetches that information automatically at runtime (when you run Terraform commands). No emails needed! No hardcoding! 🎉

### Other Common Use Cases

1. **Dynamic Image Lookups**: Instead of hardcoding "Ubuntu 20.04 image version XYZ123", you ask Azure "What's the latest Ubuntu version?" This way you never use an outdated image.
2. **Cross-State Communication**: One Terraform project (e.g., the networking team's) stores its outputs. Another project (the app team's) uses a special data source called `terraform_remote_state` to read those outputs.
3. **Existing Resources Not Managed by Terraform**: Maybe a database was created manually 2 years ago through the Azure Portal (the web UI). You can query it with a data source and reference its properties — without importing it into Terraform's state.

---

## ⚙️ How Does It Work?

### The Syntax (Structure of the Code)

A data source block looks like this:

```
data "<provider_resource_type>" "<local_name>" {
  <filter or lookup criteria>
}
```

- `data` — The keyword that tells Terraform "this is a read-only query"
- `"<provider_resource_type>"` — What type of resource you're looking up (e.g., `"azurerm_resource_group"` = an Azure Resource Group)
- `"<local_name>"` — A nickname you give this query so you can reference its results later in your code
- Inside the `{}` — The details Terraform needs to find the right resource (like a name or ID)

### When Does Terraform Run the Query?

Terraform executes data source queries during the **`terraform plan`** phase. 

**`terraform plan`** is the command that makes Terraform show you what it *would* do — like a preview before actually making changes. If a data source can't find what it's looking for during plan, **the entire plan fails immediately**. This is actually a safety feature — it stops you from deploying broken infrastructure.

### How to Reference the Results

After defining a data source, you reference its attributes (properties) using this pattern:

```
data.<resource_type>.<local_name>.<attribute>
```

For example: `data.azurerm_resource_group.existing_hub.location`

This reads: "From the data source of type `azurerm_resource_group`, the one I named `existing_hub`, give me its `location` value."

---

## 💡 Real Example

```hcl
# ─────────────────────────────────────────────
# DATA SOURCE 1: Look up an existing Resource Group
# ─────────────────────────────────────────────

# "data" keyword tells Terraform this is READ-ONLY
# "azurerm_resource_group" is the type of Azure resource we're looking up
# "existing_hub" is just a nickname we give this query (we choose this name)
data "azurerm_resource_group" "existing_hub" {

  # We tell Terraform exactly which resource group to find — by its name
  # This resource group already exists in Azure; Terraform did NOT create it
  name = "rg-enterprise-hub-eus"
}

# ─────────────────────────────────────────────
# DATA SOURCE 2: Find the latest Kubernetes (container orchestration platform) version
# ─────────────────────────────────────────────

# Kubernetes (K8s) is a system for running and managing containers (packaged apps)
# This data source asks Azure: "What's the latest stable Kubernetes version available?"
data "azurerm_kubernetes_service_versions" "current" {

  # We want versions available in this specific Azure region (location)
  location = var.location
  # var.location is a variable — its value is defined elsewhere (e.g., "eastus")

  # include_preview = false means: only give us stable versions, not experimental preview versions
  include_preview = false
}

# ─────────────────────────────────────────────
# RESOURCE: Create a new Virtual Network (VNet)
# ─────────────────────────────────────────────

# A Virtual Network (VNet) is like a private road system in the cloud
# Only your Azure resources can use this road system
# "spoke" means this is a branch network connected to a central "hub" network
resource "azurerm_virtual_network" "spoke" {

  # The name of our new VNet
  name = "vnet-spoke-app"

  # Instead of hardcoding "eastus", we READ the location from our data source
  # This means: "put this VNet in the same region as the existing hub resource group"
  # data.azurerm_resource_group.existing_hub.location = the location we looked up earlier
  location = data.azurerm_resource_group.existing_hub.location

  # Also READ the resource group name from our data source
  # This puts our new VNet INSIDE the existing resource group
  resource_group_name = data.azurerm_resource_group.existing_hub.name

  # address_space defines the range of private IP addresses this VNet can use
  # "10.1.0.0/16" means roughly 65,536 private IP addresses are available
  # IP = Internet Protocol address — like a postal address for network devices
  address_space = ["10.1.0.0/16"]
}
```

### What Happens When You Run `terraform plan`?

1. Terraform sees the `data` blocks and immediately calls the Azure API (Azure's programming interface) to fetch the information
2. If `rg-enterprise-hub-eus` exists → Terraform stores its properties (location, ID, name) in memory
3. If `rg-enterprise-hub-eus` does NOT exist → **Plan fails immediately** with a clear error message
4. The `resource` block then uses those fetched values to build the new VNet

---

## ⚠️ Common Mistakes Beginners Make

### ❌ Mistake 1: Confusing `data` and `resource` Blocks

Beginners sometimes accidentally write `resource` when they mean `data`, or vice versa. Remember:
- `resource` = **CREATE** something new in the cloud
- `data` = **READ** something that already exists

If you write `resource "azurerm_resource_group" "hub"` instead of `data "azurerm_resource_group" "hub"`, Terraform will try to **create** a brand new resource group — not look up the existing one!

### ❌ Mistake 2: Querying a Resource That Doesn't Exist Yet

If your data source references a resource that was just created in the same Terraform run (by a `resource` block in the same project), timing can be tricky. Use `depends_on` to tell Terraform to create that resource FIRST before running the data query.

### ❌ Mistake 3: Hardcoding Values That Could Be Dynamic

Beginners often hardcode things like image IDs or resource names. Use data sources to look these up dynamically instead:

```hcl
# ❌ BAD: Hardcoded image ID — what if this version gets deprecated?
source_image_id = "/subscriptions/.../images/ubuntu-20-04-OLD"

# ✅ GOOD: Look up the latest image dynamically using a data source
source_image_id = data.azurerm_image.latest_ubuntu.id
```

### ❌ Mistake 4: Not Realizing the Plan Fails if Data Source Fails

If the resource you're querying doesn't exist yet (maybe it's being created by a different Terraform project that hasn't run yet), your plan will fail. Make sure the resource exists BEFORE running your data source query.

---

## 🎯 Key Takeaway

> A **Data Source** is Terraform's "read-only" lookup tool. It lets you query existing cloud resources and use their properties in your code — without Terraform managing (or accidentally destroying) those resources. It's the safe, automated way to connect different parts of your cloud infrastructure.

---

## ❓ Beginner FAQ

**Q1: Can a data source accidentally delete or change a resource I'm querying?**
> Absolutely not! Data sources are **100% read-only**. Terraform will never modify or delete a resource that was fetched via a `data` block. The worst that can happen is the query fails (if the resource doesn't exist).

**Q2: What's the difference between `data "azurerm_resource_group"` and `resource "azurerm_resource_group"`?**
> `data "azurerm_resource_group"` says "go find an EXISTING resource group and tell me its details." `resource "azurerm_resource_group"` says "CREATE a brand new resource group." One reads, one writes. Same resource type, completely different intent.

**Q3: A database was created manually 2 years ago through the Azure Portal. I need its connection string in my Terraform code. How?**
> Use a `data` block! For example:
> ```hcl
> data "azurerm_sql_database" "old_db" {
>   name                = "my-old-database"
>   server_name         = "my-sql-server"
>   resource_group_name = "rg-production"
> }
> # Then reference: data.azurerm_sql_database.old_db.connection_string
> ```
> Terraform reads the database details without touching it.

**Q4: What happens if my data source queries a resource that doesn't exist?**
> `terraform plan` fails immediately with an error. This is actually a **good thing** — it acts like a safety check. You find out early that something is missing, before any changes are made to your cloud environment.

**Q5: Can I use data sources across different Terraform projects?**
> Yes! There's a special data source called `terraform_remote_state` that lets you read the **outputs** (exported values) from a completely different Terraform project's State File. This is how the networking team's VNet ID can be shared with the app team's project without any manual copy-pasting.

---

## 🔗 Links to Related Notes
- [[04-Resources]]
- [[07-Outputs]]
- [[VNet]]
- [[Hub-Spoke]]