---
tags: [architecture, patterns, security, zero-trust]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# 🛡️ Zero Trust Architecture — Complete Guide in Simple Language

---

## 🤔 What is Zero Trust?

**The Old Way of Security (Castle and Moat):**
Imagine a medieval castle. The moat and walls keep enemies out. But once someone gets inside the castle (through the front gate, even legitimately), they're trusted — they can go anywhere inside.

In traditional IT security, the "castle" was your corporate network. If you were connected via VPN (you got through the moat), you were trusted to access everything inside.

**The Problem:** If one person's VPN credentials get stolen, the attacker is now inside and can move freely. This is called **lateral movement**.

---

**The Zero Trust Way:**
Zero Trust assumes **the castle walls are already breached**. Assume attackers are ALREADY inside. Therefore:
- Every person, every device, every application must **prove their identity** EVERY time they access something
- Nobody gets access to more than they need (Least Privilege)
- Every action is logged and monitored

> 🧠 **The Zero Trust motto:** **"Never Trust, Always Verify"**

Think of it like a high-security office building where:
- You need a badge to enter the building ← Network perimeter
- You need a badge to enter each floor ← Network segmentation
- You need a badge for each specific room ← Application-level access
- AND the security camera logs every door you open ← Audit trail

---

## 📜 The 3 Core Principles of Zero Trust

### 1. 🔍 Verify Explicitly — "Prove yourself every time"

Don't just check IF someone has access. Check ALL of these before granting access:
- ✅ **Who are you?** (Identity — are you who you say you are? MFA enforced?)
- ✅ **What device are you using?** (Is it a company-managed, compliant device? Or a personal phone from a coffee shop?)
- ✅ **Where are you?** (Logging in from your normal country, or from a suspicious location?)
- ✅ **What time is it?** (3 AM access to the production database is unusual)
- ✅ **What are you trying to access?** (Is this data classified as sensitive?)

**In Azure, this is implemented with Conditional Access Policies.**

### 2. 🔑 Use Least Privilege Access — "Only what you need, only when you need it"

- Give people the **minimum permissions** needed to do their job — nothing more
- Use **Just-In-Time (JIT) access** — someone shouldn't have permanent admin access to production. They request it for 4 hours, do their work, access expires automatically.
- Use **Just-Enough-Access (JEA)** — a developer doesn't need the same access as a security engineer

**In Azure, this is implemented with:**
- Azure RBAC (Role-Based Access Control)
- Privileged Identity Management (PIM) for JIT

### 3. 💥 Assume Breach — "Design for when (not if) you're hacked"

- **Minimize blast radius:** If one component is compromised, limit how much damage it can do
- **Micro-segmentation:** Don't put all services in one big subnet. Divide them. Use NSGs to define exactly which IP can talk to which port.
- **End-to-end encryption:** Encrypt data everywhere — at rest, in transit, even between microservices inside your own network
- **Continuous monitoring:** Log everything. Use AI/ML-based threat detection to spot unusual behavior

---

## 🏗️ Implementing Zero Trust in Azure — Layer by Layer

### Layer 1: Identity — "The New Perimeter"

In Zero Trust, **Identity is the new perimeter**. The old perimeter was the network firewall. Now, the first and most important gate is: "Are you who you claim to be?"

#### Conditional Access Policies (Microsoft Entra ID)

Conditional Access is like an intelligent gatekeeper that evaluates dozens of conditions before granting access.

```
Rule Example: "Accessing Production Key Vault"
  IF user is a Developer
  AND device is Entra-joined (company managed) 
  AND MFA is completed
  AND location is India (expected)
  → GRANT access

  IF user is a Developer  
  AND device is unknown
  OR location is Russia (unexpected)
  → BLOCK access and raise security alert
```

**Real Terraform Example — Conditional Access Policy:**
```hcl
resource "azuread_conditional_access_policy" "require_mfa_for_admin" {
  display_name = "Require MFA for Admin Access"
  state        = "enabled"

  conditions {
    client_app_types = ["browser", "mobileAppsAndDesktopClients"]
    
    users {
      included_roles = ["62e90394-69f5-4237-9190-012177145e10"] # Global Administrator role
    }
    
    applications {
      included_applications = ["All"]  # All Azure applications
    }
  }

  grant_controls {
    operator          = "AND"
    built_in_controls = ["mfa"]  # Require Multi-Factor Authentication
  }
}
```

#### Privileged Identity Management (PIM) — JIT Access

Nobody should have permanent `Owner` or `Contributor` access to production. Use PIM:

```
Standard time: John is a "Reader" on Production
     │
John needs to deploy → Requests "Contributor" for 4 hours
     │
Approval from manager (automatic or manual)
     │
John has "Contributor" for exactly 4 hours
     │
Time expires → John is back to "Reader" automatically
All actions during those 4 hours are fully logged
```

---

### Layer 2: Network — "Micro-Segmentation"

#### Don't trust the network perimeter alone

Even inside your VNet, traffic should be restricted. Use **Network Security Groups (NSGs)** to create micro-segments:

```
Web Tier Subnet (10.1.1.0/24)
  → Can ONLY send traffic TO App Tier on port 8080
  → CANNOT directly reach Database Tier
  → CANNOT reach other subnets except App Tier

App Tier Subnet (10.1.2.0/24)
  → Can ONLY receive from Web Tier on port 8080
  → Can ONLY send to DB Tier on port 5432 (PostgreSQL)

Database Tier Subnet (10.1.3.0/24)
  → Can ONLY receive from App Tier on port 5432
  → No outbound internet access at all
```

```hcl
# NSG Rule: Only allow Web → App communication
resource "azurerm_network_security_rule" "allow_web_to_app" {
  name                        = "Allow-Web-To-App"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "8080"
  source_address_prefix       = "10.1.1.0/24"  # Web Tier only
  destination_address_prefix  = "10.1.2.0/24"  # App Tier
  ...
}

# The implicit "Deny All" at the bottom of every NSG handles everything else
```

#### Private Endpoints — No Public Internet for PaaS Services

By default, Azure PaaS services (Key Vault, SQL, Storage) are accessible over the public internet. In Zero Trust, **nothing should be public that doesn't need to be**.

```hcl
# Make Key Vault only accessible via private network
resource "azurerm_private_endpoint" "keyvault_pe" {
  name                = "pe-keyvault-prod"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name
  subnet_id           = azurerm_subnet.private_endpoints.id  # Dedicated PE subnet

  private_service_connection {
    name                           = "psc-keyvault"
    private_connection_resource_id = azurerm_key_vault.kv.id
    subresource_names              = ["vault"]
    is_manual_connection           = false
  }
}
# Now mykeyvault.vault.azure.net resolves to a private IP, not the public internet
```

---

### Layer 3: Data — "Encrypt Everything"

**At Rest:** Enable encryption using Customer Managed Keys (CMK) stored in Key Vault:
```hcl
resource "azurerm_storage_account" "sa" {
  # ... other config ...
  
  customer_managed_key {
    key_vault_key_id          = azurerm_key_vault_key.sa_key.id
    user_assigned_identity_id = azurerm_user_assigned_identity.sa_identity.id
  }
}
```

**In Transit:** Enforce TLS 1.2 or higher:
```hcl
resource "azurerm_storage_account" "sa" {
  min_tls_version = "TLS1_2"   # Block TLS 1.0 and 1.1 (old, insecure versions)
  # ...
}
```

---

### Layer 4: Applications & Workloads

- Use **Managed Identities** instead of storing credentials in code
- Scan container images for vulnerabilities before deploying to AKS
- Apply **Pod Security Standards** in Kubernetes (restrict what pods can do)
- Regularly scan code for secrets using tools like `git-secrets` or **GitHub Advanced Security**

---

## 🔍 Monitoring — The "Assume Breach" Layer

Zero Trust requires continuous monitoring because you always assume something is compromised. Key tools:

| Tool | Purpose |
|------|---------|
| **Microsoft Sentinel** | Cloud-native SIEM. Collects all logs and uses ML to detect threats |
| **Microsoft Defender for Cloud** | Assesses your Azure resources for security misconfigurations and vulnerabilities |
| **Entra ID Sign-In Logs** | Every login attempt — successful, failed, MFA challenged |
| **Azure Activity Log** | Every management action (who created a VM, who changed a firewall rule) |
| **Log Analytics** | Central repository for all logs |

---

## 📋 Zero Trust Maturity Assessment

Microsoft defines 3 stages of Zero Trust maturity:

| Stage | Identity | Network | Data |
|-------|----------|---------|------|
| **Traditional** | Password only | VPN = trusted | Unencrypted |
| **Advanced** | MFA + Conditional Access | Micro-segmentation | Encryption at rest |
| **Optimal** | PIM + passwordless | Automated threat response | Data classification + CMK |

> 💡 **Start with Identity.** Enabling MFA and basic Conditional Access policies gives you 80% of the security benefit of Zero Trust for 20% of the effort.

---

## 🎯 Key Takeaways

1. **Zero Trust = Never trust anything by default**, whether it's inside or outside your network
2. **Identity is the new perimeter** — Conditional Access + MFA is your first and most important control
3. **Least Privilege + JIT** — Nobody has standing admin access. Request it, use it, it expires.
4. **Micro-segmentation** — Use NSGs to restrict every subnet from talking to every other subnet
5. **Private Endpoints** — PaaS services should never be reachable from the public internet
6. **Encrypt everything** — At rest (CMK), in transit (TLS 1.2+), between services (mTLS in a service mesh)
7. **Log and monitor everything** — Assume you've already been breached; continuous monitoring catches lateral movement
