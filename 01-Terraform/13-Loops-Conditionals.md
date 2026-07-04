---
category: Terraform
tags: [terraform, loops, conditionals, hcl, architecture, scaling]
type: fundamental
status: active
level: beginner
---

# Terraform Loops and Conditionals

---

## 📖 Before You Read

This topic involves some programming concepts. Make sure you're comfortable with:

- ✅ **Variables** in Terraform — named containers that hold values (like `var.location`)
- ✅ **Resource blocks** — the code blocks that create cloud infrastructure
- ✅ **Maps** — a data structure like a dictionary: `{ "key" = "value" }` pairs
- ✅ **What IaC means** — Infrastructure as Code (IaC) = writing code to build and manage your servers, networks, and cloud resources instead of clicking through a web interface manually
- ✅ Basic understanding of what a **subnet** is — a smaller subdivision of a network (like a neighborhood inside a city)

If variables or resources are new to you, review [[04-Resources]] and [[05-Variables]] first.

---

## 🤔 What Are Loops and Conditionals in Terraform?

### Plain English Definition

Imagine you're a teacher 👩‍🏫 and you need to create a name badge for each student in your class. You have 30 students. You could:

**Option A (No loops):** Write each name badge manually, 30 times. If a student joins or leaves, you update the list manually every time.

**Option B (With loops):** Write ONE template for a name badge, give Terraform a list of student names, and let Terraform automatically create all 30 badges. When a student leaves, just remove their name from the list — Terraform handles the rest.

**Loops in Terraform** work like Option B. Instead of writing the same resource block 10, 20, or 50 times, you write it **once** and tell Terraform to repeat it for each item in a list.

**Conditionals** are like answering "yes or no" questions. "Should we create a VPN Gateway? Only if it's production." Think of it like a light switch — on or off depending on a condition.

---

## 🧠 Why Do We Need Loops and Conditionals?

### The Problem Without Them

Without loops, your code quickly becomes a nightmare. Imagine needing 5 subnets (network subdivisions):

```hcl
# WITHOUT LOOPS — This is terrible! Copy-pasted 5 times 😱
resource "azurerm_subnet" "web" {
  name             = "snet-web"
  address_prefixes = ["10.0.1.0/24"]
  # ... more config
}
resource "azurerm_subnet" "db" {
  name             = "snet-db"
  address_prefixes = ["10.0.2.0/24"]
  # ... more config
}
resource "azurerm_subnet" "app" {
  name             = "snet-app"
  address_prefixes = ["10.0.3.0/24"]
  # ... more config
}
# ... and so on
```

This violates the **DRY principle** (Don't Repeat Yourself) — a fundamental rule in software engineering. The more you copy-paste, the more places you have to update when something changes. And the more bugs you introduce.

### What Loops and Conditionals Solve

- **Loops** = Write once, apply many times. Change the list, Terraform creates/destroys accordingly.
- **Conditionals** = Feature toggles. "Deploy this expensive resource only in prod, skip it in dev to save money."

---

## ⚙️ How Does It Work?

There are **three looping mechanisms** in Terraform and **one conditional syntax**. Let's cover each:

---

### 🔄 Loop Method 1: `count`

`count` is the simplest loop. You say "create THIS resource X times." Terraform creates `X` copies, numbered `[0]`, `[1]`, `[2]`, etc.

**When to use:** When all your resources are basically **identical** and you don't care about their individual identities (like 5 identical worker VMs behind a load balancer).

**⚠️ The `count` Index Problem:**
This is critical to understand. With `count = 3`, resources are identified by their position in a numbered list:
```
azurerm_subnet.example[0]  ← position 0
azurerm_subnet.example[1]  ← position 1
azurerm_subnet.example[2]  ← position 2
```

If you **remove item at position 0**, Terraform shifts the whole list:
- Old `[1]` becomes new `[0]` → Terraform destroys and recreates it
- Old `[2]` becomes new `[1]` → Terraform destroys and recreates it

This cascade of accidental recreations can cause **massive outages**. This is why `count` is dangerous for anything with a unique identity.

---

### 🔄 Loop Method 2: `for_each` (The Safer Choice)

`for_each` loops over a **map** (a set of key-value pairs, like a dictionary) or a **set of strings** (a collection of unique text values). Each resource gets identified by its **key** (a named label), not its position number.

**When to use:** For resources with unique identities like subnets, databases, firewall rules — basically anything where each item has a distinct name.

**Why `for_each` is safer:**
```
azurerm_subnet.example["web-tier"]  ← identified by name "web-tier"
azurerm_subnet.example["db-tier"]   ← identified by name "db-tier"
```

If you remove `"web-tier"`, only that specific subnet gets destroyed. `"db-tier"` is completely untouched. No cascade. No outage. ✅

---

### 🔄 Loop Method 3: `dynamic` Blocks

Sometimes a single resource has **repeating sections inside it**. For example, a Network Security Group (NSG — a firewall that controls what network traffic is allowed) can have dozens of security rules. Without `dynamic`, you'd have to hardcode each rule.

`dynamic` blocks let you loop over a list to generate these nested sections automatically.

---

### ❓ Conditional: Ternary Expression

A **ternary expression** (or ternary operator) is a compact way to write "if this is true, use this value; otherwise use that value."

The syntax is: `condition ? value_if_true : value_if_false`

Think of it like a vending machine choice: "Is it cold outside? ☁️ Yes → Hot cocoa. No → Iced coffee."

Combined with `count`, it becomes a powerful feature toggle:
```hcl
count = var.is_production ? 1 : 0
# "if is_production is true, create 1 copy; otherwise create 0 copies (don't create it)"
```

---

## 💡 Real Example

```hcl
# ─────────────────────────────────────────────────────────────────
# EXAMPLE 1: for_each — Create multiple subnets from a map variable
# ─────────────────────────────────────────────────────────────────

# First, define a variable that holds a map of subnet names and their IP ranges
variable "subnets" {
  # type = map(string) means this is a dictionary where both keys and values are text (strings)
  type = map(string)

  # default is the value used if you don't specify one when running Terraform
  default = {
    # "key" = "value"
    # key   = subnet name (used as identifier)
    # value = CIDR range (the IP address range for this subnet — "10.0.1.0/24" means
    #         addresses from 10.0.1.0 to 10.0.1.255, giving 256 addresses)
    "web" = "10.0.1.0/24"   # Subnet for web servers
    "db"  = "10.0.2.0/24"   # Subnet for database servers
  }
}

# Now create one subnet for EACH entry in the map
resource "azurerm_subnet" "spoke" {

  # for_each tells Terraform to loop over var.subnets (our map)
  # For each iteration, Terraform provides:
  #   each.key   = the key   (e.g., "web" or "db")
  #   each.value = the value (e.g., "10.0.1.0/24" or "10.0.2.0/24")
  for_each = var.subnets

  # each.key is the subnet name from our map ("web" or "db")
  # "snet-" is a prefix (short for "subnet-") following Azure naming conventions
  # Result: "snet-web" or "snet-db"
  name = "snet-${each.key}"

  # Reference the resource group that should already be created
  # azurerm_resource_group.main.name means "use the name of the resource group
  # called 'main' that we defined earlier in our code"
  resource_group_name = azurerm_resource_group.main.name

  # Reference the virtual network this subnet belongs to
  virtual_network_name = azurerm_virtual_network.main.name

  # each.value is the IP range from our map
  # address_prefixes expects a list (that's why it's wrapped in [ ])
  # Result: ["10.0.1.0/24"] or ["10.0.2.0/24"]
  address_prefixes = [each.value]
}

# ─────────────────────────────────────────────────────────────────
# EXAMPLE 2: count + conditional — Only deploy VPN Gateway in prod
# ─────────────────────────────────────────────────────────────────

# A VPN Gateway (Virtual Private Network Gateway) allows encrypted connections
# from your on-premises (physical office) network to Azure
# It's expensive — we only want it in production, not dev (to save money)

# First, a variable to control whether we deploy the VPN Gateway
variable "deploy_vpn_gateway" {
  type    = bool        # bool = boolean = true or false
  default = false       # By default, don't deploy it
  description = "Set to true only in production to deploy the VPN Gateway"
}

# A Public IP address is needed by the VPN Gateway to be reachable from the internet
resource "azurerm_public_ip" "vpn" {

  # THE MAGIC LINE: Conditional count
  # If deploy_vpn_gateway is true  → count = 1 → create 1 public IP
  # If deploy_vpn_gateway is false → count = 0 → create ZERO (don't deploy anything)
  count = var.deploy_vpn_gateway ? 1 : 0

  # Name for this public IP resource
  name = "pip-vpn-gateway"
  # "pip" = public IP, following Azure naming conventions

  # Where to create this resource
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  # allocation_method = "Static" means the IP address won't change over time
  # (as opposed to "Dynamic" which can change after restarts)
  allocation_method = "Static"
}

# ─────────────────────────────────────────────────────────────────
# EXAMPLE 3: dynamic block — Multiple firewall rules in one resource
# ─────────────────────────────────────────────────────────────────

# NSG = Network Security Group — Azure's built-in firewall for controlling network traffic
# Without dynamic blocks, you'd hardcode each security_rule block separately
resource "azurerm_network_security_group" "main" {
  name                = "nsg-app"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  # dynamic block generates repeating nested blocks automatically
  # "security_rule" is the name of the block we're generating (must match the resource's expected block name)
  dynamic "security_rule" {

    # for_each here loops over our list of rules (defined in locals)
    # local.nsg_rules would be a list of maps, each map describing one firewall rule
    for_each = local.nsg_rules

    # content {} defines what each generated "security_rule" block looks like
    content {
      # security_rule.value is one item from local.nsg_rules
      # .name, .priority, .direction, etc. are fields within that item
      name                       = security_rule.value.name
      priority                   = security_rule.value.priority
      direction                  = security_rule.value.direction
      access                     = security_rule.value.access
      protocol                   = security_rule.value.protocol
      source_port_range          = "*"         # * means any port
      destination_port_range     = security_rule.value.port
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
  }
}
```

---

## ⚠️ Common Mistakes Beginners Make

### ❌ Mistake 1: Using `count` for Resources That Have Unique Identities

As explained above, `count` uses integer indexes. Removing an item from the middle causes Terraform to shift and recreate everything after it. **Use `for_each` whenever your resources have meaningful names** (subnets, databases, storage accounts, etc.).

### ❌ Mistake 2: Passing a List to `for_each` (Requires a Map or Set)

`for_each` only accepts **maps** or **sets of strings**. If you try to pass a regular list (like `["web", "db"]`), it will error. To convert a list to a set, use the `toset()` function:

```hcl
for_each = toset(["web", "db"])
# toset() converts a list to a set, which for_each accepts
```

### ❌ Mistake 3: Trying to Use `count` and `for_each` Together

You cannot use both `count` and `for_each` on the same resource block. Pick one. Terraform will give you an error if you try both.

### ❌ Mistake 4: Forgetting That `count = 0` Means "Don't Create This"

Beginners sometimes panic when they see `count = 0` thinking it's a bug. It's intentional! `count = 0` is how you tell Terraform "create zero copies of this resource" — effectively not creating it at all. Combined with a conditional, this is how you implement optional/toggleable resources.

---

## 🎯 Key Takeaway

> Use `for_each` (not `count`) for resources with unique names to avoid dangerous cascade-recreations. Use `count = condition ? 1 : 0` to conditionally create or skip a resource. Use `dynamic` blocks to loop over repeating sections inside a single resource. These three tools transform copy-paste infrastructure code into clean, scalable, professional Terraform.

---

## ❓ Beginner FAQ

**Q1: When should I use `count` vs `for_each`?**
> Simple rule: Use `count` only for **identical, interchangeable resources** where position doesn't matter (like 5 identical worker VMs behind a load balancer, where they're truly interchangeable). Use `for_each` for **anything with a unique name or identity** (subnets named "web", "db", "app"; databases; storage accounts; etc.). When in doubt, use `for_each` — it's safer.

**Q2: What does `each.key` and `each.value` mean?**
> When you use `for_each`, Terraform loops over your map. For each iteration, `each.key` gives you the KEY (the label/name) and `each.value` gives you the VALUE (the associated data). For example, if your map is `{ "web" = "10.0.1.0/24" }`, then `each.key = "web"` and `each.value = "10.0.1.0/24"`.

**Q3: How do I conditionally deploy a resource?**
> Use `count` with a ternary expression:
> ```hcl
> count = var.is_production ? 1 : 0
> ```
> When `is_production = true`, Terraform creates 1 copy. When `is_production = false`, count is 0 — Terraform doesn't create it. Simple as a light switch!

**Q4: What is a `dynamic` block and when do I need it?**
> A `dynamic` block is used when a **single resource** has a section that needs to repeat. For example, an NSG (Network Security Group / firewall) can have many security rules. Instead of copy-pasting the `security_rule { }` block 20 times, you use a `dynamic "security_rule" { }` block to loop over a list and generate all the rules automatically.

**Q5: I got an error: "Invalid for_each argument — must be a map or set of strings." What went wrong?**
> You probably tried to pass a regular list to `for_each`. Lists are ordered by position (like `count`) but `for_each` needs named keys. Wrap your list in `toset()` to convert it: `for_each = toset(var.my_list)`. Or better yet, convert your variable type from `list(string)` to `set(string)` or `map(string)`.

---

## 🔗 Links to Related Notes
- [[04-Resources]]
- [[05-Variables]]
- [[06-Locals]]
- [[NSG]]