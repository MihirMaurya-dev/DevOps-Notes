---
category: Azure-Security
tags: [azure, security, key-vault, secrets, architecture, rbac, private-endpoint]
type: enterprise-architect-guide
source: devopsinsiders/batch-18
updated: 2026-10-17
status: active
---

# 🔑 Azure Key Vault — Enterprise Architect Guide & Deep Dive

---

## 📖 Before You Read

- You understand Azure Resource Groups, VNets, and Subnets → [[01-Azure-Fundamentals]], [[03-VNet]]
- You know how Managed Identities work → [[08-Managed-Identity]]
- You understand Infrastructure as Code with Terraform → [[01-Introduction]]

---

## 1. Introduction & Why Azure Key Vault Exists

**Azure Key Vault** is a centralized, cloud-hosted security service designed for safeguarding cryptographic keys, application secrets, and TLS/SSL certificates.

### 🛑 The Problem: Hardcoded Secrets Antipattern
Historically, developers stored database connection strings, API keys, VM admin credentials, and passwords directly in source code or local configuration files:

```hcl
# ❌ NEVER DO THIS: Hardcoded credentials committed to Git!
resource "azurerm_linux_virtual_machine" "app_vm" {
  name                = "vm-backend-prod"
  admin_username      = "adminuser"
  admin_password      = "P@ssw0rd1234!"  # Leak risk! Visible to anyone with repo access
}
```

If source control is compromised, credentials are leaked, or repositories become public, external attackers instantly gain administrative access to your servers and databases.

### 💡 The Solution: Abstracting Secrets
With Azure Key Vault:
1. Secrets are stored in a hardened, encrypted cloud vault.
2. Applications and CI/CD pipelines fetch credentials dynamically at runtime using authenticated identities.
3. Zero credentials ever touch source code, Git repositories, or developer laptops.

---

## 2. 🗄️ Storage Account vs. Azure Key Vault (Architectural Comparison)

A frequent point of confusion is when to use an Azure Storage Account versus an Azure Key Vault:

| Feature / Dimension | Azure Storage Account | Azure Key Vault |
|---------------------|-----------------------|-----------------|
| **Primary Purpose** | Bulk data storage (files, unstructured data, messages) | Cryptographic security & secret management |
| **Data Types** | **Blobs** (images, logs, backups), **File Shares** (SMB/NFS), **Queues** (FIFO messages), **Tables** (NoSQL key-value) | **Secrets** (text/passwords ≤ 25 KB), **Keys** (RSA/EC crypto keys), **Certificates** (x509 TLS/SSL) |
| **Access Protocols** | HTTP/HTTPS, SMB, NFS | REST API (HTTPS / TLS 1.3 only) |
| **Hardware Protection** | Standard server storage hardware | FIPS 140-2 Level 1 (Standard) / FIPS 140-2 Level 2/3 HSM (Premium) |
| **Typical DevOps Use** | Terraform remote `.tfstate` files, build artifacts, container logs | VM admin passwords, DB connection strings, API tokens, SSL certs |

---

## 3. 🏛️ Core Components of Azure Key Vault

Key Vault manages three distinct categories of security artifacts:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          Azure Key Vault                               │
├────────────────────┬────────────────────┬──────────────────────────────┤
│    1. Secrets      │      2. Keys       │       3. Certificates        │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ • Passwords        │ • RSA / EC Keys    │ • x509 SSL/TLS Certs         │
│ • Connection str   │ • Disk Encryption  │ • Auto-enrollment            │
│ • API tokens       │ • SQL TDE CMK      │ • DigiCert / GlobalSign      │
│ • Any text ≤ 25 KB │ • Never exportable │ • Auto-rotation before expiry│
└────────────────────┴────────────────────┴──────────────────────────────┘
```

1. **Secrets:** Plaintext strings (up to 25 KB) encrypted at rest using Microsoft-managed master keys. Perfect for database connection strings, third-party API keys, and VM passwords.
2. **Keys:** Asymmetric or symmetric cryptographic keys used for data encryption (e.g., Azure Disk Encryption, Transparent Data Encryption with Customer-Managed Keys). In Premium vaults, keys are backed by physical Hardware Security Modules (HSM) and can never be exported in plaintext.
3. **Certificates:** End-to-end management of SSL/TLS certificates. Key Vault can generate Certificate Signing Requests (CSRs), partner with trusted CAs (DigiCert, GlobalSign), and automatically push renewed certificates to Azure Application Gateways.

---

## 4. 🔐 Access Models: Entra ID RBAC vs. Vault Access Policies

Azure Key Vault supports two authorization models. Understanding the difference is crucial for interviews and architecture design:

```
Comparison of Authorization Models:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ Feature                               │ Azure RBAC (Modern & Recommended)     │ Vault Access Policies (Legacy)        │
├───────────────────────────────────────┼───────────────────────────────────────┼───────────────────────────────────────┤
│ Scope Level                           │ Management Group, Subscription, RG,   │ Vault level only                      │
│                                       │ or specific Key / Secret              │                                       │
│ Granularity                           │ Per-secret role assignment possible   │ All-or-nothing per vault               │
│ PIM Integration                       │ Full Privileged Identity Management   │ No native PIM support                 │
│ Limit                                 │ Up to 4,000 role assignments / sub    │ Maximum 1,024 access policy entries   │
│ Microsoft Recommendation              │ ✅ Default for all new vaults         │ ⚠️ Legacy, maintenance only           │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

### Key RBAC Roles for Key Vault

- **`Key Vault Administrator`:** Complete control over both the management plane and data plane.
- **`Key Vault Secrets Officer`:** Can create, update, delete, and read secrets (ideal for CI/CD pipelines provisioning secrets).
- **`Key Vault Secrets User`:** Read-only access to secret contents (ideal for applications running on VMs or AKS).
- **`Key Vault Crypto Officer` / `User`:** Manages or consumes cryptographic keys.
- **`Key Vault Certificates Officer` / `User`:** Manages or consumes x509 certificates.

---

## 5. 🌐 Network Isolation & Zero-Trust Architecture

By default, an Azure Key Vault has a public internet endpoint (`<vault-name>.vault.azure.net`). In an enterprise environment, public access must be strictly forbidden:

```
Secure Enterprise VNet Topology:
┌────────────────────────────────────────────────────────────────────────┐
│ Azure Virtual Network (10.0.0.0/16)                                    │
│                                                                        │
│  ┌───────────────────────┐          ┌────────────────────────────────┐ │
│  │ backend-subnet        │          │ private-endpoint-subnet        │ │
│  │ (10.0.2.0/24)         │          │ (10.0.4.0/24)                  │ │
│  │                       │          │                                │ │
│  │  ┌─────────────────┐  │ Private  │  ┌──────────────────────────┐  │ │
│  │  │ App VM / VMSS   │──┼─────────►│  │ Private Endpoint (NIC)   │  │ │
│  │  │ (10.0.2.4)      │  │ Traffic  │  │ (10.0.4.10)              │  │ │
│  │  └─────────────────┘  │ (TLS 1.3)│  └─────────────┬────────────┘  │ │
│  └───────────────────────┘          └────────────────┼───────────────┘ │
│                                                      │                 │
│                                                      ▼                 │
│                                           ┌──────────────────────┐     │
│                                           │   Azure Key Vault    │     │
│                                           │  (Public Access OFF) │     │
│                                           └──────────────────────┘     │
└────────────────────────────────────────────────────────────────────────┘
```

### Essential Security Configurations
1. **Disable Public Access:** Set `public_network_access_enabled = false`.
2. **Azure Private Endpoint:** Deploy a Private Endpoint into a dedicated subnet. Key Vault receives a private IP address (`10.0.4.10`) inside your VNet.
3. **Private DNS Zone:** Link `privatelink.vaultcore.azure.net` to your VNet so queries to `myvault.vault.azure.net` resolve internally to `10.0.4.10`.
4. **Soft Delete & Purge Protection:** 
   - Soft Delete retains deleted vaults/secrets for a retention period (default 90 days).
   - Purge Protection ensures even a Subscription Owner cannot prematurely wipe the vault, preventing ransomware and accidental deletion disasters.

---

## 6. 🛠️ Hands-on Implementation: Terraform Key Vault + Secure VM

Here is the production Terraform implementation showing how to deploy a secure Key Vault, generate a random VM password, store it in Key Vault, and configure a Virtual Machine without exposing secrets.

### Key Vault Child Module (`modules/azurerm_key_vault/main.tf`)

```hcl
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = var.key_vault_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  
  # Security Controls
  enable_rbac_authorization   = true    # Use modern RBAC
  soft_delete_retention_days  = 90
  purge_protection_enabled    = true
  public_network_access_enabled = true   # Set false once Private Endpoint is bound

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
    ip_rules       = var.allowed_admin_ips
  }

  tags = var.tags
}

# Generate random secure password for VMs
resource "random_password" "vm_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Store VM password securely in Key Vault
resource "azurerm_key_vault_secret" "vm_admin_password" {
  name         = "vm-admin-password"
  value        = random_password.vm_password.result
  key_vault_id = azurerm_key_vault.kv.id

  lifecycle {
    ignore_changes = [value]
  }
}
```

### Consuming Secrets in Virtual Machine (`modules/azurerm_virtual_machine/main.tf`)

```hcl
# Read secret dynamically from Key Vault
data "azurerm_key_vault_secret" "vm_password" {
  name         = "vm-admin-password"
  key_vault_id = var.key_vault_id
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                            = var.vm_name
  resource_group_name             = var.resource_group_name
  location                        = var.location
  size                            = "Standard_D2s_v5"
  admin_username                  = "azureuser"
  admin_password                  = data.azurerm_key_vault_secret.vm_password.value
  disable_password_authentication = false
  network_interface_ids           = [azurerm_network_interface.nic.id]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  # Assign System-Assigned Managed Identity to VM for Key Vault secret fetching
  identity {
    type = "SystemAssigned"
  }
}

# Grant VM Managed Identity permission to read secrets
resource "azurerm_role_assignment" "vm_kv_secrets_user" {
  scope                = var.key_vault_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_virtual_machine.vm.identity[0].principal_id
}
```

---

## 7. 🎯 Top Interview Q&A (DevOps Insiders Real Scenarios)

### Q1: What is the difference between Access Policies and Azure RBAC in Key Vault?
**Answer:** Access Policies are the legacy authorization model applied strictly at the vault level (all-or-nothing access to all secrets in that vault, capped at 1,024 entries). Azure RBAC is the modern, enterprise-recommended model that integrates with Entra ID, supports inheritance from Management Groups down to individual secret objects, and works seamlessly with Privileged Identity Management (PIM).

### Q2: How do you eliminate passwords from application code that accesses Key Vault?
**Answer:** By assigning a **System-Assigned or User-Assigned Managed Identity** to the computing resource (VM, App Service, or AKS Pod via Workload Identity). The application uses the Azure SDK (`DefaultAzureCredential`), which requests an Entra ID token from the local Azure Instance Metadata Service (IMDS). The token is verified by Key Vault without requiring any hardcoded secrets.

### Q3: An application encounters HTTP 403 Forbidden when calling Key Vault. How do you troubleshoot?
**Answer:** 
1. **Identity Layer:** Check if the caller identity has the `Key Vault Secrets User` role assigned at the vault or secret scope.
2. **Network Layer:** Check if Key Vault has public access disabled or firewall rules active. If the app is hosted on an App Service or VM, verify VNet integration and ensure traffic flows through an Azure Private Endpoint or allowed IP range.
3. **Soft-Deleted State:** Verify if the secret was soft-deleted or expired.

---

## 🔗 Related Notes

- [[08-Managed-Identity]] — Azure Managed Identities (System vs User Assigned)
- [[15-VM]] — Azure Virtual Machine Architecture
- [[03-VNet]] — Azure Virtual Networks and Subnets
- [[05-Terraform-Pipeline]] — Multi-stage Terraform CI/CD Pipelines
- [[06-Axion-3-Tier-Enterprise-Project]] — Axion 3-Tier Enterprise Infrastructure