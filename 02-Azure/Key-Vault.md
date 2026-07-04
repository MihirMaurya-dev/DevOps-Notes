---
category: Azure-Security
tags: [azure, security, key-vault, secrets, architecture]
type: enterprise-architect-guide
status: active
---

# 🔑 Azure Key Vault - Enterprise Architect Guide

## 1. Introduction
Azure Key Vault is a centralized, secure cloud service for safeguarding cryptographic keys, application secrets, and certificates. By using Key Vault, you eliminate the need to hardcode sensitive information into your application source code, drastically reducing the risk of accidental exposure via version control (e.g., GitHub).

## 2. Why This Service Exists
Historically, developers stored database connection strings, API keys, and passwords in application configuration files (like `web.config` or `.env` files). If a server was breached or source code was leaked, all external systems were instantly compromised. Key Vault exists to abstract secrets away from applications. Applications authenticate themselves to the vault dynamically at runtime to fetch the secrets they need.

## 3. Architecture
- **Scope:** Regional service.
- **Layer:** Platform as a Service (PaaS) for Security.
- **Under the Hood:** Key Vault uses different cryptographic backing depending on the SKU. The **Standard SKU** uses software-protected keys (FIPS 140-2 Level 1). The **Premium SKU** uses dedicated Hardware Security Modules (HSMs) certified to **FIPS 140-2 Level 2**. When you store a key in a Premium vault, the key never leaves the physical HSM boundary.

## 4. Core Components
- **Secrets:** Passwords, connection strings, API tokens, or any string data (max 25 KB per secret).
- **Keys:** Cryptographic keys used for encrypting data (RSA, EC). Used for operations like Azure Disk Encryption (ADE) or Transparent Data Encryption (TDE).
- **Certificates:** Provision, manage, and deploy public/private x509 SSL/TLS certificates. Integrates with Certificate Authorities to auto-renew.
- **Access Policies / Azure RBAC:** The authorization mechanism determining *who* or *what* can access the vault.

## 5. Step-by-Step Request Flow
**Scenario:** An Azure App Service needs to read a database connection string.
1. The App Service is configured with a **System-Assigned Managed Identity** by Entra ID.
2. The application code makes an API call to the Key Vault URI (e.g., `https://myvault.vault.azure.net/secrets/db-string`).
3. Behind the scenes, the Azure SDK fetches an authentication token from the local Azure Instance Metadata Service (IMDS) using its Managed Identity.
4. The token is presented to Key Vault.
5. Key Vault validates the token with Entra ID and checks its internal authorization rules (RBAC or Access Policy).
6. If the identity has the `Key Vault Secrets User` role (or equivalent Access Policy), the vault decrypts the secret and returns it to the application securely over TLS.

## 6. Real-World Production Use Cases
1. **Dynamic Secret Retrieval:** Web apps fetching API keys at startup so no secrets are stored on the host filesystem.
2. **Automated Certificate Renewal:** Key Vault automatically generates a CSR, communicates with DigiCert/GlobalSign, retrieves the new SSL certificate, and pushes it to an Azure Application Gateway before the old one expires.
3. **Customer-Managed Keys (CMK):** Using Key Vault to store a master encryption key to encrypt an Azure Storage Account, allowing the customer (not Microsoft) to revoke the key and instantly destroy data access.

## 7. Architecture & Design Considerations
- **Vault Segmentation (One vs Many):** **Do not put all enterprise secrets in one giant Key Vault.** The blast radius is too large, and Key Vault has API rate limits. Best practice: Create one Key Vault per environment, per application boundary (e.g., `kv-hr-app-prod`, `kv-finance-app-dev`).
- **Authorization Model:** Key Vault supports two permission models: Legacy "Vault Access Policies" and modern "Azure RBAC". Always select **Azure RBAC** for new deployments to integrate natively with Management Groups and PIM.

## 8. Microsoft Best Practices
- **Enable Soft Delete and Purge Protection:** This is critical. Without these, an attacker (or clumsy admin) could permanently delete your encryption keys, instantly destroying all data encrypted by them.
- **Use Managed Identities:** Never create a Service Principal with a client secret to access Key Vault. Use Managed Identities so there are no credentials to rotate.

## 9. Security Best Practices
- **Network Isolation:** By default, Key Vaults have public endpoints. You must configure Key Vault Firewalls to deny all traffic, and only allow access via **Azure Private Endpoints** (connecting the vault to your VNet).
- **Least Privilege:** A developer should have `Key Vault Secrets User` (read) in Dev, but zero access in Prod. In Prod, only the Application's Managed Identity should have `Key Vault Secrets User`.
- **Separate Key/Secret Officers from Readers:** The pipeline (Terraform/CI-CD) acts as the Secrets Officer (writing the secret). The Application acts as the Secrets User (reading the secret).

## 10. Monitoring & Observability
- **Diagnostic Settings:** Enable logging to Log Analytics. You must monitor the `AuditEvent` logs to see exactly which IP address and Identity requested which secret and when.
- **Alerting:** Set up Azure Monitor alerts for `Secret Expiration Date < 30 days` and for excessive `403 Forbidden` errors (which could indicate a brute-force or misconfigured app).

## 11. Backup & Disaster Recovery
- **Regional Resilience:** Key Vault contents are seamlessly replicated to the paired secondary region. In a full region outage, Microsoft fails over the DNS name to the secondary region in read-only mode automatically.
- **Granular Backup:** You can download an encrypted backup of specific keys/secrets via the Portal/CLI and restore them to a completely different Key Vault in the same geographic area.

## 12. Cost Optimization Techniques
- Key Vault is incredibly inexpensive (typically $0.03 per 10,000 transactions). Cost is rarely a concern.
- Only upgrade to the **Premium SKU** if you strictly require HSM-backed keys (FIPS 140-2 Level 2) for compliance reasons. The Standard SKU uses software-protected keys and handles 95% of use cases.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Key Vault?
   **A:** A secure service for storing and managing secrets, encryption keys, and certificates.
2. **Q:** Why shouldn't you store database passwords in your application code?
   **A:** Hardcoded secrets can be exposed in source control. Key Vault centralizes them securely.

### Intermediate
3. **Q:** How does an application running on an Azure VM authenticate to Key Vault?
   **A:** By using an Entra ID Managed Identity assigned to the VM, combined with an Access Policy or RBAC role on the Key Vault.
4. **Q:** What is Soft Delete in Key Vault?
   **A:** It protects against accidental deletion by retaining deleted vaults and objects for a configurable period (7-90 days).
5. **Q:** What is Purge Protection?
   **A:** When enabled alongside Soft Delete, it ensures that even an administrator cannot force-delete (purge) the secret before the retention period expires.

### Advanced
6. **Q:** How do you restrict access to a Key Vault at the network level?
   **A:** Use Key Vault Firewalls to allow only specific IPs, or use Azure Private Endpoint to make the Key Vault accessible only via a private IP on your VNet.
7. **Q:** Explain Key Vault Access Policies vs Azure RBAC.
   **A:** Access Policies are the legacy way of managing data-plane access per vault. Azure RBAC is the modern approach, providing unified, granular access control and the ability to inherit permissions from Management Groups or Subscriptions.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** Application returns `403 Forbidden` when attempting to read a secret.
  - **Resolution:** Two primary causes: 
    1. **Identity:** The Managed Identity attached to the app doesn't have the `Key Vault Secrets User` role. 
    2. **Network:** The Key Vault firewall is blocking the request. If the app is a PaaS service (like App Service) accessing a firewall-restricted Key Vault, you must enable VNet Integration on the App Service or check the "Allow Trusted Microsoft Services" box.
- **Scenario:** Unable to delete a Key Vault.
  - **Resolution:** If Purge Protection is on, you cannot bypass the soft-delete window. You must wait (e.g., 90 days) for it to permanently disappear. If you just need the name back, recover the deleted vault instead.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create Key Vault using RBAC authorization model
az keyvault create \
  --name "kv-app-prod-001" \
  --resource-group "rg-security" \
  --location "eastus" \
  --enable-rbac-authorization true \
  --enable-purge-protection true

# Add a Secret
az keyvault secret set --vault-name "kv-app-prod-001" --name "DbConnectionString" --value "Server=tcp:mysvr;Database=db;"
```

## 16. Terraform Implementation (IaC)
```hcl
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = "kv-app-prod-001"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"

  enable_rbac_authorization   = true
  purge_protection_enabled    = true
  soft_delete_retention_days  = 30

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }
}

# Assign Secret Officer role to the Terraform deployment identity
resource "azurerm_role_assignment" "kv_admin" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}
```

## 17. Production Readiness Checklist
- [ ] Is Soft Delete enabled?
- [ ] Is Purge Protection enabled?
- [ ] Is the Azure RBAC permission model selected instead of legacy Access Policies?
- [ ] Is the public network access disabled (Default Action: Deny)?
- [ ] Is a Private Endpoint configured for internal access?
- [ ] Are Audit Logs streaming to a Log Analytics Workspace?
- [ ] Is the architecture following the "One Key Vault per App boundary" rule?