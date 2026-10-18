---
tags: [terraform, azure, security, azurerm_key_vault]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🔐 Terraform Resource: azurerm_key_vault

> "A Key Vault is a digital titanium safe. You put your most dangerous secrets inside, and Azure guards the door."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What a **Key Vault** actually is — see [[Key-Vault]]
- What **Azure RBAC** (Role-Based Access Control) is — see [[35-RBAC|RBAC]]
- What a **Data Source** is in Terraform — see [[12-Data-Sources]]

---

## 1. 🤔 What is `azurerm_key_vault`?

### 🤔 What is it?

In Azure, a **Key Vault** is a highly secure cloud service used to store "Secrets" (like database passwords), "Keys" (for encryption), and "Certificates" (for HTTPS websites). 

In Terraform, `azurerm_key_vault` is the resource block used to forge this titanium safe.

> 🏦 **Real-World Analogy:**
> Imagine a high-security bank vault. You don't just walk in and grab money. You have to show your ID to the guard (Authentication via Entra ID Tenant). The guard then checks a list to see if you are allowed to open Safety Deposit Box #42 (Authorization via RBAC). 
>
> The `azurerm_key_vault` creates the bank vault, hires the guard, and sets the rules.

---

## 2. 🧠 Why do we need it?

The #1 rule in DevOps is: **NEVER HARDCODE PASSWORDS IN YOUR CODE.** 

If you write `password = "SuperSecret123!"` in your Terraform or application code, anyone who reads the code can hack your database. 

Instead, you use Terraform to build an `azurerm_key_vault`, store the password inside it, and tell your Virtual Machines or Web Apps to "go ask the Key Vault for the password." If a hacker reads your code, all they see is a pointer to the Key Vault, which they cannot open.

---

## 3. ⚙️ How does it work?

To create a Key Vault, Terraform needs a few unique pieces of information:
1. `name`: What to call it. (Must be globally unique, 3-24 characters).
2. `tenant_id`: The ID of your company's Microsoft Entra ID (Azure AD). This tells the vault *which* company's employees are even allowed to approach the door.
3. `sku_name`: The pricing tier (`standard` is fine for almost everyone. `premium` involves physical hardware security modules/HSMs).
4. `enable_rbac_authorization`: A switch that tells the vault to use modern Azure RBAC instead of the old, messy "Access Policies" system.

---

## 4. 💡 Real Example (Line-by-Line)

Here is a secure, modern implementation of an Azure Key Vault. Notice how we use a `data` block to magically find our `tenant_id`!

### `variables.tf` (The Inputs)
```hcl
variable "key_vault_name" {
  type        = string
  description = "Name MUST be globally unique!"
  default     = "kv-myapp-prod-9988" # 'kv' = key vault
}

variable "resource_group_name" {
  type    = string
  default = "rg-security-prod"
}

variable "location" {
  type    = string
  default = "eastus"
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- DATA SOURCE ----
# We use a data block to ask Azure: "Who am I currently logged in as?"
# This automatically fetches our Tenant ID so we don't have to copy-paste a huge GUID.
data "azurerm_client_config" "current" {}

# ---- THE RESOURCE BLOCK ----
resource "azurerm_key_vault" "main" {
  name                        = var.key_vault_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  
  # Which company "owns" this vault? (Fetched automatically from the data block!)
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  
  # Standard pricing tier
  sku_name                    = "standard"

  # 🛡️ Modern Best Practice: Use Azure RBAC for permissions
  enable_rbac_authorization   = true
  
  # 🛡️ Security Feature: Purge Protection
  # If a hacker deletes a secret, this forces Azure to keep a hidden backup 
  # of it for 7 days before it is TRULY deleted forever.
  purge_protection_enabled    = true
  soft_delete_retention_days  = 7

  tags = {
    Environment = "Production"
  }
}
```

### `outputs.tf` (The Results)
```hcl
output "key_vault_id" {
  description = "The ID of the Key Vault."
  value       = azurerm_key_vault.main.id
}

output "key_vault_uri" {
  description = "The URI (web address) of the Key Vault. Apps use this to fetch secrets!"
  value       = azurerm_key_vault.main.vault_uri
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Hardcoding the Tenant ID:** Beginners often hardcode `tenant_id = "1234abcd-..."`. This breaks the code if you ever try to deploy it to a different Azure Tenant (like a client's environment). Always use `data.azurerm_client_config.current.tenant_id`.
2. **Using the Old Access Policies:** The Terraform documentation still shows `access_policy {}` blocks inside the Key Vault resource. This is the **old way**. It is messy and hard to manage. Always set `enable_rbac_authorization = true` and use the separate `azurerm_role_assignment` resource to give people access.
3. **Getting Locked Out of Your Own Vault:** If you use RBAC, simply creating the vault does NOT give you permission to read the secrets inside it! You must assign yourself the "Key Vault Secrets Officer" role after creating it, otherwise, you'll get an "Access Denied" error on your own vault.

---

## 6. 🎯 Key Takeaway

The `azurerm_key_vault` is critical for securing passwords and API keys. Always use the `azurerm_client_config` data source to grab your Tenant ID dynamically, enable `purge_protection` so you don't accidentally lose critical passwords forever, and use modern RBAC (`enable_rbac_authorization = true`) for managing access.

---

## 7. ❓ Beginner FAQ

**Q1: How do I actually put a password inside the vault using Terraform?**
> You use a second resource called `azurerm_key_vault_secret`. You point it at the `azurerm_key_vault.main.id` and pass in your secret value!

**Q2: Is a Key Vault expensive?**
> No, it is incredibly cheap. The "Standard" tier costs fractions of a penny per 10,000 requests. You only pay for what you use.

**Q3: What does `enabled_for_disk_encryption` do?**
> If you set this to `true`, it allows Azure Virtual Machines to use the keys stored inside this vault to encrypt their C: drives. This is a common requirement for enterprise security compliance.
