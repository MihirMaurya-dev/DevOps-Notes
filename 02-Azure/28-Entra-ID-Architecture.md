---
tags: [azure, entra-id, identity, architecture, rbac]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🔐 Azure Entra ID — Architecture & Access Management

Microsoft Entra ID (formerly Azure Active Directory) is Microsoft's cloud-based Identity and Access Management (IAM) service. It is the **identity backbone** of every Azure deployment.

> [!important]
> In the cloud, **Identity is the new security perimeter.** The network boundary no longer matters — who you are matters more than where you are.

---

## 1. Tenant Hierarchy

```
Entra ID Tenant (Root — entire organization)
│
├── Management Groups         (Governance scope — policies & RBAC)
│   ├── Platform MG
│   └── Landing Zones MG
│       ├── Corp Subscription
│       └── Online Subscription
│
├── Azure Subscriptions       (Billing + Resource boundary)
│   └── Resource Groups
│       └── Azure Resources   (VMs, VNets, Key Vaults...)
│
└── Entra ID Objects
    ├── Users                 (Human identities)
    ├── Groups                (Collections of users/service principals)
    ├── App Registrations     (Application identities)
    ├── Service Principals    (App identity per tenant)
    └── Managed Identities    (Machine identities — no passwords)
```

> [!note]
> An Azure Subscription **trusts** an Entra ID Tenant, but the Tenant is **above** and **independent** from the subscription hierarchy. You can move subscriptions between tenants.

---

## 2. Key Identity Types

| Identity Type | Who Uses It | Example |
|---|---|---|
| **User** | Humans (employees, admins) | `john@contoso.com` |
| **Group** | Collections of users | `Cloud-Admins`, `Network-Readers` |
| **Service Principal** | Applications | Terraform, GitHub Actions |
| **Managed Identity** | Azure Resources | VM accessing Key Vault |
| **Guest User (B2B)** | External partners | Vendor from `partner.com` |

---

## 3. Authentication Flow (How Login Works)

```
User → browser → app.contoso.com
         ↓ (no session, redirect to login)
login.microsoftonline.com
         ↓
   [1] Check credentials (Password / Passwordless)
   [2] Evaluate Conditional Access Policies
         ↓  (CA requires MFA?)
   [3] Prompt MFA (Authenticator App)
         ↓  (MFA passed)
   [4] Issue JWT Token (access token + refresh token)
         ↓
App receives token → validates signature → grants access
```

---

## 4. RBAC (Role-Based Access Control)

RBAC in Azure is about **who can do what on which resource**.

```
Principal  +  Role          +  Scope          =  Assignment
(Who)         (What)           (Where)
─────────────────────────────────────────────────────────────
John Doe   +  Contributor  +  Subscription A  =  Can create/modify resources in Sub A
Terraform  +  Owner        +  Resource Group  =  Can manage all resources in that RG
MI (VM)    +  KV Secrets   +  Key Vault       =  Can read secrets from that KV
```

**Built-in Roles (Most Used):**

| Role | What It Can Do |
|------|---------------|
| `Owner` | Full control, including managing access |
| `Contributor` | Create/modify resources, cannot manage access |
| `Reader` | Read-only view |
| `User Access Administrator` | Can manage access (RBAC) but not resources |
| `Key Vault Secrets User` | Can read secrets from Key Vault |
| `AcrPull` | Can pull images from Azure Container Registry |

---

## 5. Conditional Access (Zero Trust Enforcement)

Conditional Access is an **If → Then** policy engine.

**Example Policies:**
```
IF  user is logging in from an unknown country
THEN block access

IF  user is accessing the Azure Portal
THEN require MFA + compliant device

IF  sign-in risk is HIGH (compromised account)
THEN force password reset
```

> [!tip]
> Always use **Report-Only mode** first when creating a new Conditional Access policy. It logs what *would* have happened without actually enforcing the policy — safe for testing in production.

---

## 6. Privileged Identity Management (PIM)

PIM enforces **Just-In-Time (JIT)** privilege. Instead of permanent admin roles, users **activate** roles temporarily when needed.

**Without PIM:**
```
John has "Global Admin" role → permanently, 24/7, even on weekends
```
**With PIM:**
```
John has "Eligible" for Global Admin
→ John clicks "Activate" when needed
→ Provides justification + approver approves
→ Granted Global Admin for 2 hours only
→ Role automatically removed after 2 hours
```

---

## 7. Managed Identity (Best Practice for Azure Resources)

Never hardcode credentials. Use Managed Identity so Azure resources authenticate to each other automatically.

**System-Assigned vs User-Assigned:**

| | System-Assigned | User-Assigned |
|---|---|---|
| Lifecycle | Tied to the resource | Independent resource |
| Sharing | 1 resource only | Can be shared across multiple resources |
| Use Case | Single VM → Key Vault | Multiple VMs/Functions using the same identity |

**Terraform — Enable Managed Identity on a VM:**
```hcl
resource "azurerm_linux_virtual_machine" "app_vm" {
  name                = "app-vm-prod"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B2s"

  identity {
    type = "SystemAssigned"   # Entra ID creates an identity for this VM
  }
  # ...
}

# Grant the VM's identity access to Key Vault
resource "azurerm_role_assignment" "vm_kv_access" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_virtual_machine.app_vm.identity[0].principal_id
}
```

---

## 8. Hybrid Identity (On-Premises + Cloud)

If you have on-premises Active Directory:

```
On-Premises AD (Windows Server)
        ↓ sync via
Microsoft Entra Connect
        ↓
Entra ID (Cloud)
```

**Sync Options:**
- **Password Hash Sync (PHS):** Hash of hash of password synced to cloud. Simplest, recommended.
- **Pass-Through Authentication (PTA):** Cloud validates credentials against on-prem in real-time.
- **Federation (ADFS):** Most complex, for specific compliance requirements.

---

## 9. Production Best Practices

> [!warning]
> Never use the Global Administrator account for day-to-day operations. Use PIM to elevate only when required.

- ✅ **Break-Glass Accounts:** 2 cloud-only emergency accounts excluded from Conditional Access, monitored by alerts
- ✅ **Block Legacy Auth:** Disable POP3, IMAP, SMTP basic auth (they bypass MFA)
- ✅ **PIM for all privileged roles:** No permanent Global Admin, Owner, or User Access Admin assignments
- ✅ **Named Locations:** Define trusted IP ranges, block high-risk geographies
- ✅ **Log to Sentinel/Log Analytics:** Entra ID only keeps logs 30 days by default

---

## 10. Monitoring & Observability

Route Entra ID logs to Log Analytics for long-term retention:

```hcl
resource "azurerm_monitor_diagnostic_setting" "entra_diag" {
  name               = "entra-id-diag"
  target_resource_id = "/tenants/${var.tenant_id}/providers/microsoft.aadiam"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.central.id

  enabled_log {
    category = "SignInLogs"
  }
  enabled_log {
    category = "AuditLogs"
  }
}
```

**Key KQL Queries:**
```kql
// Failed logins in last 24 hours
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != "0"
| summarize count() by UserPrincipalName, ResultDescription

// Privileged role activations (PIM)
AuditLogs
| where OperationName == "Add member to role completed (PIM activation)"
| project TimeGenerated, InitiatedBy, TargetResources
```

---

## 11. Production Readiness Checklist

- [ ] Break-Glass accounts created and monitored with alerts
- [ ] Legacy Authentication blocked via Conditional Access
- [ ] MFA enforced for all users (standard + admin)
- [ ] PIM configured for Global Admin, Subscription Owner, User Access Admin
- [ ] Sign-in & Audit logs routed to Log Analytics / Sentinel
- [ ] Conditional Access in Report-Only mode validated before enforcement
- [ ] No service accounts using username/password — using Managed Identities or Service Principals with certificates
