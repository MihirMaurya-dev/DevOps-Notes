---
tags: [terraform, azure, monitoring, azurerm_log_analytics_workspace]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 📊 Terraform Resource: azurerm_log_analytics_workspace

> "A Log Analytics Workspace is the black box flight recorder for your entire cloud. Everything that happens gets sent here."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What **Logs and Metrics** are in the cloud. (Metrics are numbers like "CPU at 80%". Logs are text like "User Dave failed password at 12:05 PM").
- What **Azure Monitor** is — it's the umbrella service that uses the Log Analytics Workspace to build dashboards.

---

## 1. 🤔 What is `azurerm_log_analytics_workspace`?

### 🤔 What is it?

In Azure, a **Log Analytics Workspace (LAW)** is a massive, highly optimized database designed specifically to ingest and query millions of log lines per second. 

In Terraform, `azurerm_log_analytics_workspace` is the block you write to provision this central logging database.

> 🗄️ **Real-World Analogy:**
> Imagine a massive corporate office building with 5,000 security cameras, 50 door badge readers, and 20 fire alarms. 
> 
> If each of those devices stored its own data, security guards would have to run around the building to check them individually. Instead, every camera and alarm sends its data down a wire into a **Central Security Room** with giant monitors. 
> 
> The Log Analytics Workspace is that Central Security Room for your cloud infrastructure.

---

## 2. 🧠 Why do we need it?

If a Virtual Machine crashes or a web app throws a 500 Error, the local logs are often destroyed when the machine reboots. 

By having a central Log Analytics Workspace, you configure every Azure resource (VMs, Firewalls, Key Vaults) to stream their logs directly into it. If a server dies, the evidence of *why* it died is safely stored in the workspace.

Using Terraform is crucial because a workspace is a foundational resource. You build the workspace *first*, and then every time you build a new VM or database, your Terraform code automatically wires it up to send logs to the workspace.

---

## 3. ⚙️ How does it work?

To create the workspace, Terraform only requires a few basic parameters:
1. `name`: What to call the workspace.
2. `sku`: The billing tier. In modern Azure, this is almost always set to `"PerGB2018"` (which means you pay for exactly how much data you ingest, rather than a flat rate).
3. `retention_in_days`: How long should Azure keep the logs before deleting them to save you money? The default is 30 days.

---

## 4. 💡 Real Example (Line-by-Line)

Here is a standard Terraform implementation for a Log Analytics Workspace.

### `variables.tf` (The Inputs)
```hcl
variable "workspace_name" {
  type        = string
  description = "The name of the Log Analytics Workspace."
  default     = "law-monitoring-prod-eus" # 'law' = log analytics workspace
}

variable "resource_group_name" {
  type    = string
  default = "rg-monitoring-prod"
}

variable "location" {
  type    = string
  default = "eastus"
}

# We use a variable for retention so we can easily change it later
variable "retention_in_days" {
  type        = number
  description = "How many days to keep the logs."
  default     = 30
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- THE RESOURCE BLOCK ----
resource "azurerm_log_analytics_workspace" "main" {
  name                = var.workspace_name
  location            = var.location
  resource_group_name = var.resource_group_name
  
  # The standard Pay-As-You-Go pricing tier
  sku                 = "PerGB2018"
  
  # How long to keep the data
  retention_in_days   = var.retention_in_days

  tags = {
    Environment = "Production"
    Purpose     = "Central Security Logging"
  }
}

# (Bonus Example) - How to send Key Vault logs TO the workspace
# This uses the azurerm_monitor_diagnostic_setting resource
# resource "azurerm_monitor_diagnostic_setting" "kv_logs" {
#   name                       = "send-logs-to-law"
#   target_resource_id         = azurerm_key_vault.main.id
#   log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
#   ...
# }
```

### `outputs.tf` (The Results)
```hcl
output "workspace_id" {
  description = "The Azure Resource ID of the workspace. Used to connect other resources."
  value       = azurerm_log_analytics_workspace.main.id
}

output "workspace_workspace_id" {
  description = "The strange Customer ID (a GUID) used by VM monitoring agents."
  value       = azurerm_log_analytics_workspace.main.workspace_id
}

output "workspace_primary_shared_key" {
  description = "The password that Virtual Machines use to send logs here."
  value       = azurerm_log_analytics_workspace.main.primary_shared_key
  sensitive   = true # Do not print this to the screen!
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Creating Too Many Workspaces:** Beginners often create a separate Log Analytics Workspace for every single application (App A gets a workspace, App B gets a workspace). **This is an anti-pattern.** Best practice is to have ONE central workspace per environment. It's much easier to query the data if it's all in one place!
2. **Infinite Retention:** Setting the `retention_in_days` to 730 (2 years) without realizing that Azure charges you a daily fee to store that much data. Only keep logs as long as your compliance/security department requires (usually 30 to 90 days).
3. **Confusing `id` vs `workspace_id`:** `id` is the long Azure Resource Manager path (e.g., `/subscriptions/123/resourceGroups/...`). `workspace_id` is a shorter, unique GUID used specifically by internal monitoring agents. Make sure you pass the correct one to other Terraform modules!

---

## 6. 🎯 Key Takeaway

The `azurerm_log_analytics_workspace` is the central nervous system for cloud monitoring. You should create one central workspace per region/environment, set the SKU to `PerGB2018`, and configure your retention period carefully to manage costs.

---

## 7. ❓ Beginner FAQ

**Q1: How do I actually view the logs once they are in the workspace?**
> You use a special language called **KQL (Kusto Query Language)** in the Azure Portal. It's very similar to SQL. You can write a query like `SecurityEvent | where TimeGenerated > ago(1h)` to see all security alerts from the last hour.

**Q2: What happens when the `retention_in_days` expires?**
> Azure automatically purges the oldest data on a rolling basis. On day 31, the logs from day 1 are permanently deleted. 

**Q3: Is the workspace free?**
> No. You pay for "Data Ingestion" (how many Gigabytes you send to the workspace) and "Data Retention" (how long you keep it). If you send 5 GB of logs a day, it can cost a few hundred dollars a month.
