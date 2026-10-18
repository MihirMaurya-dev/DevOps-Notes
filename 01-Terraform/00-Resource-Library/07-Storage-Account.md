---
tags: [terraform, azure, storage, azurerm_storage_account]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🗄️ Terraform Resource: azurerm_storage_account

> "A Storage Account is Microsoft's giant, infinitely expanding hard drive. You can dump files, logs, and backups into it without ever worrying about running out of space."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What a **Storage Account** is in Azure — see [[Storage-Account]]
- The concept of **Globally Unique Names** in Azure (DNS)
- The difference between **LRS** (Local) and **GRS** (Global) replication

---

## 1. 🤔 What is `azurerm_storage_account`?

### 🤔 What is it?

In Azure, a **Storage Account** is a fundamental service that provides massively scalable cloud storage. It holds "Blobs" (files like images or CSVs), "Files" (shared network drives), "Queues", and "Tables".

In Terraform, `azurerm_storage_account` is the resource block used to create this storage container.

> 📦 **Real-World Analogy:**
> Imagine renting a giant warehouse (Storage Account). Inside this warehouse, you can set up different areas: one for stacking random boxes of old paperwork (Blobs), one for a filing cabinet where multiple employees can pull documents at the same time (Files), and one for an assembly line conveyor belt (Queues). 
>
> `azurerm_storage_account` is you signing the lease for the warehouse.

---

## 2. 🧠 Why do we need it?

Storage Accounts are used *everywhere*. 
- Where do Virtual Machines save their diagnostic logs? The Storage Account.
- Where do you store the `terraform.tfstate` file so your team can work together? The Storage Account.
- Where does your web app save user profile pictures? The Storage Account.

Creating it via Terraform ensures you apply strict security settings (like enforcing HTTPS) perfectly every time. If you click through the portal, it's very easy to accidentally leave your storage public to the internet!

---

## 3. ⚙️ How does it work?

To create a Storage Account in Terraform, you must provide:
1. `name`: The name of the storage account. **WARNING: It must be GLOBALLY UNIQUE across all of Azure.** You cannot name it "mystorage" because someone else in the world already took it. It also must be 3-24 characters, **lowercase letters and numbers only**.
2. `resource_group_name`: Where it lives.
3. `location`: The Azure region.
4. `account_tier`: Standard (cheap, spinning hard drives) or Premium (expensive, fast SSDs).
5. `account_replication_type`: How many backup copies Microsoft makes (e.g., LRS = 3 copies in one building, GRS = 6 copies across two different cities).

---

## 4. 💡 Real Example (Line-by-Line)

Here is a secure, production-ready example of deploying a Storage Account.

### `variables.tf` (The Inputs)
```hcl
variable "storage_account_name" {
  type        = string
  description = "Name MUST be globally unique, lowercase, no dashes."
  default     = "stmyappprod12345" # 'st' = storage, 'myapp' = app, 'prod' = env, '12345' = random numbers for uniqueness
}

variable "resource_group_name" {
  type    = string
  default = "rg-storage-prod"
}

variable "location" {
  type    = string
  default = "eastus"
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- THE RESOURCE BLOCK ----
resource "azurerm_storage_account" "main" {
  
  # 1. Basic properties
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  
  # 2. Performance and Replication
  account_tier             = "Standard" # Good for 99% of use cases
  account_replication_type = "LRS"      # Locally Redundant Storage (3 copies in one datacenter)

  # 3. 🛡️ Security Best Practices
  # Force modern encryption
  min_tls_version          = "TLS1_2"
  
  # Force encrypted transit (reject normal HTTP)
  https_traffic_only_enabled = true
  
  # CRITICAL: Prevent anyone from making a file public to the internet!
  allow_nested_items_to_be_public = false

  tags = {
    Environment = "Production"
  }
}
```

### `outputs.tf` (The Results)
```hcl
# We output the Primary Access Key. 
# Think of this as the "master password" to the warehouse.
output "storage_account_primary_access_key" {
  description = "The primary access key for the storage account."
  value       = azurerm_storage_account.main.primary_access_key
  
  # We MUST mark this as sensitive, otherwise Terraform will print it 
  # to the console screen where anyone looking over your shoulder can see it!
  sensitive   = true
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Naming Errors:** The most common Terraform error is `storage_account_name is invalid`. Beginners try to use dashes (`st-myapp-prod`), capital letters (`StMyApp`), or names that are already taken (`teststorage`). Remember: **Lowercase letters and numbers only, globally unique!**
2. **Leaving Public Access On:** By default, Azure used to allow you to make Blob containers public. Many data breaches happen this way. Always set `allow_nested_items_to_be_public = false` to physically prevent anyone from making data public.
3. **Printing the Key:** If you output the `primary_access_key` without setting `sensitive = true`, it gets stored in plaintext logs in your CI/CD pipeline (like GitHub Actions) where anyone can steal it.

---

## 6. 🎯 Key Takeaway

The `azurerm_storage_account` resource creates the most fundamental data storage mechanism in Azure. The trickiest part is guaranteeing the `name` is globally unique and formatted correctly. Always explicitly define your security arguments (`min_tls_version`, `https_traffic_only_enabled`, and `allow_nested_items_to_be_public`) to ensure enterprise-grade safety.

---

## 7. ❓ Beginner FAQ

**Q1: How do I make the name globally unique automatically using Terraform?**
> A very popular trick is to use the `random_string` or `random_integer` Terraform provider to generate 5 random characters, and append them to your storage account name! Example: `name = "stmyapp${random_string.suffix.result}"`

**Q2: What is LRS vs GRS?**
> **LRS (Locally Redundant Storage):** Microsoft makes 3 copies of your data on 3 different server racks in the SAME building. If the building burns down, your data is gone.
> **GRS (Geo-Redundant Storage):** Microsoft makes 3 copies in your building (East US), and 3 copies in a building 500 miles away (West US). If East US is destroyed by a hurricane, your data survives.

**Q3: Is the Storage Account encrypted?**
> Yes! By default, Azure encrypts all Storage Accounts "at rest" using Microsoft-managed keys. You don't have to write any code to enable basic encryption.
