---
tags: [azure, identity, entra-id, security]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🪪 Managed Identity in Azure — The Beginner's Complete Guide

---

## 📖 Before You Read

Before diving in, it helps if you understand:
- What a **password** is and why it's sensitive
- What an **Azure resource** is — any service you create in Azure (like a Virtual Machine, a Web App, a Storage Account)
- What [[Key-Vault]] is — Azure's secure secret storage
- What [[Storage-Account]] is — Azure's cloud storage service
- What **GitHub** is — a popular website where developers store and share code

Don't worry if you're fuzzy on any of these — we'll explain everything!

---

## 🤔 What is a Managed Identity? — Plain English + Real-World Analogy

Imagine you're a new employee at a company. On your first day, you're given:
- An **employee ID badge** with your name and photo
- Access to certain rooms (the HR office, your team's floor, the cafeteria)
- You don't need to memorize passwords for each door — your badge handles it automatically

Now imagine instead of a person, it's a **computer program** (your app, your Virtual Machine, your pipeline). The program needs to access certain services (like a database or a secret vault). Traditionally, you'd give it a "username and password" — which is risky.

**Managed Identity** gives your program its own **automatic ID badge** — an identity in Azure's identity system that Azure manages for you. The program shows its badge to access resources, and Azure verifies it behind the scenes. No passwords in your code. No secrets to manage.

> 🧠 **In simple words:** A Managed Identity is an automatically managed digital ID card for an Azure resource (like a Virtual Machine or an App Service). It lets your resource securely access other Azure services without needing to store any passwords in your code.

---

## 🧠 Why Do We Need It? — The Problem It Solves

### The Old, Dangerous Way (Connection Strings)

In the old days, if your **Virtual Machine (VM)** — a virtual computer running in the cloud — needed to access something like:
- A database in Azure SQL
- A secret in Azure Key Vault
- Files in an Azure Storage Account

...you'd write the credentials directly into your code or config file:

```python
# ❌ THE DANGEROUS OLD WAY — Don't do this!

# Connection string: a text string containing all the info needed to connect to a resource
# Think of it like a URL + username + password all in one line
connection_string = "DefaultEndpointsProtocol=https;AccountName=mystorageacct;AccountKey=abc123xyz=="

# Database password stored directly in the code
db_connection = "Server=myserver.database.windows.net;Database=mydb;User=admin;Password=SuperSecret123!"
```

**The Huge Problem:** If this code is ever:
- 😱 Accidentally pushed to a public GitHub repository
- 😱 Seen by a disgruntled employee
- 😱 Included in an error log that's not properly secured
- 😱 Leaked in a security breach

...the attacker now has **full access** to your database, storage, and everything else. This happens regularly in the real world and causes massive data breaches.

### The Managed Identity Solution — No More Passwords in Code!

```python
# ✅ THE SAFE, MODERN WAY — Using Managed Identity

from azure.identity import DefaultAzureCredential      # Import the Azure identity library
from azure.storage.blob import BlobServiceClient       # Import the Azure storage library

# DefaultAzureCredential automatically uses the VM's Managed Identity
# It's like showing your ID badge automatically — no username or password needed!
credential = DefaultAzureCredential()

# Connect to storage using the identity — no connection string with a secret key!
blob_client = BlobServiceClient(
    account_url="https://mystorageacct.blob.core.windows.net",
    credential=credential   # ← Azure handles the auth automatically via Managed Identity
)

# Now you can read/write files — and your code has ZERO secrets in it!
```

There's literally no password, no key, no secret in the code. Azure proves the identity of your VM automatically.

---

## ⚙️ How Does It Work? — Step by Step

Here's what happens behind the scenes when a VM with a Managed Identity accesses a Key Vault:

```
Step 1: You enable Managed Identity on your VM
        Azure automatically creates an identity for it in Microsoft Entra ID
        (Entra ID = Microsoft's cloud identity system, like a digital HR department)

Step 2: You assign permissions
        "Give this VM's identity the 'Key Vault Secrets User' role on this Key Vault"
        (Like telling HR: "This employee badge should open the archives room")

Step 3: Your app runs on the VM and needs a secret
        It calls: DefaultAzureCredential() or similar

Step 4: Azure automatically sends a request to a special internal endpoint
        http://169.254.169.254/metadata/identity/oauth2/token
        (This is an IP address that ONLY exists inside Azure VMs — you can't reach it from outside)
        
Step 5: Azure returns a short-lived TOKEN (like a temporary visitor pass — expires in ~1 hour)

Step 6: Your app uses the token to call Key Vault
        "Here's my token, please give me the secret 'database-password'"

Step 7: Key Vault checks: "Is this token valid? Does this identity have permission?"
        YES → Returns the secret value ✅
        NO  → Returns "Access Denied" ❌
```

**The key insight:** Your code never stores the token or the password. The token is fetched automatically at runtime and expires quickly. Even if someone somehow captured the token, it's useless after an hour.

---

## 🔄 Types of Managed Identities

There are two "flavors" of Managed Identity, and knowing when to use each is important:

### 🔵 Type 1: System-Assigned Managed Identity

🤔 **What is it?**

Think of this like an **employee badge tied to a specific desk**. The badge only works for one person, and when that person leaves the company (the desk is removed), the badge is automatically deactivated.

A System-Assigned identity is created **for one specific Azure resource** and its lifecycle is **tied to that resource**. Delete the VM → identity is deleted automatically.

⚙️ **How to enable it (Terraform example):**

```hcl
# Creating a Virtual Machine with a System-Assigned Managed Identity
resource "azurerm_linux_virtual_machine" "my_vm" {
  name                = "my-application-vm"
  resource_group_name = "my-rg"
  location            = "East US"
  size                = "Standard_B2s"   # VM size (like picking a computer spec)

  # ... other VM settings ...

  identity {
    type = "SystemAssigned"   # ← This enables a System-Assigned Managed Identity!
    # Azure will automatically create an identity for THIS specific VM
  }
}

# After creation, you can reference the identity's ID:
# azurerm_linux_virtual_machine.my_vm.identity[0].principal_id
# and use it to assign roles (permissions)
```

✅ **Best for:** A workload that runs on a SINGLE resource. Simple, automatic, no extra management.

❌ **Not ideal for:** Multiple resources that all need the same permissions (you'd have to assign roles separately to each one).

---

### 🟢 Type 2: User-Assigned Managed Identity

🤔 **What is it?**

Think of this like a **shared key card** at an office. Multiple employees can be given copies of the same key card. If one employee leaves, the card isn't destroyed — other employees still use it. The card has its own existence, independent of any individual employee.

A User-Assigned identity is a **standalone Azure resource** with its own lifecycle. You create it independently, then attach it to as many Azure resources as you want.

⚙️ **How to create and use it (Terraform example):**

```hcl
# STEP 1: Create the User-Assigned Managed Identity as a standalone resource
resource "azurerm_user_assigned_identity" "app_identity" {
  name                = "my-app-identity"        # A descriptive name for this identity
  resource_group_name = "my-rg"
  location            = "East US"
}
# This creates a STANDALONE identity that we can reuse across multiple resources

# STEP 2: Attach it to a Virtual Machine
resource "azurerm_linux_virtual_machine" "vm_one" {
  name = "vm-one"
  # ... other settings ...

  identity {
    type = "UserAssigned"   # ← Using a User-Assigned identity (not System-Assigned)
    identity_ids = [
      azurerm_user_assigned_identity.app_identity.id  # ← Attach our shared identity
    ]
  }
}

# STEP 3: Attach the SAME identity to another VM — they share the same permissions!
resource "azurerm_linux_virtual_machine" "vm_two" {
  name = "vm-two"
  # ... other settings ...

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.app_identity.id  # ← Same identity, different VM!
    ]
  }
}

# STEP 4: Assign permissions ONCE — both VMs automatically get them
resource "azurerm_role_assignment" "kv_access" {
  scope                = azurerm_key_vault.example.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.app_identity.principal_id
  # ☝️ Assign the role to the identity — BOTH VMs now have this permission!
}
```

✅ **Best for:** Multiple resources that all need the **same permissions** (e.g., 5 different VMs that all need to read from the same Key Vault). Assign once, done.

✅ **Best for:** When you need the identity to **outlive** the resources it's attached to (e.g., delete a VM and recreate it — the identity and its permissions stay the same).

---

## 🔑 OIDC and Workload Identity Federation — For CI/CD Pipelines

### What Is CI/CD?

**CI/CD** stands for **Continuous Integration / Continuous Deployment**:
- **Continuous Integration (CI):** Every time a developer pushes code, an automated system builds and tests it
- **Continuous Deployment (CD):** After testing, the code is automatically deployed to servers

This is done by **pipeline** systems like **GitHub Actions** or **Azure DevOps** — automated workflows that run in the cloud.

### The Old Problem with Pipelines

Your pipeline needs to deploy resources to Azure. Traditionally you'd:
1. Create a **Service Principal** (a type of "app identity" in Entra ID)
2. Generate a **Client Secret** (like a password) for it
3. Store that secret in GitHub Secrets (encrypted storage for pipeline credentials)

The problem: the secret **expires** and needs rotating. If you forget, the pipeline breaks. And secrets, even stored securely, can be compromised.

### The Modern Solution: OIDC (Workload Identity Federation)

**OIDC** stands for **OpenID Connect** — an open standard (a publicly agreed-upon method) for identity verification. "Open" means any service can implement it — GitHub, Azure, Google, etc., all understand it.

**Workload Identity Federation** uses OIDC to allow GitHub (or other services) to prove their identity to Azure **without any stored secrets**.

Here's the analogy: Imagine two trusted banks that know each other. When a customer from Bank A visits Bank B, they don't need a separate account — Bank B trusts Bank A's identification. GitHub and Azure have established this kind of trust.

**How it works:**

```
GitHub Actions pipeline runs:
  1. GitHub generates a short-lived OIDC token (valid for ~5 minutes)
     "I am GitHub Actions, running for repo 'myorg/myapp', on branch 'main'"
     
  2. The pipeline sends this token to Entra ID:
     "Azure, please give me access — here's my GitHub OIDC token as proof"
     
  3. Entra ID checks: "Do we trust GitHub Actions tokens? Yes.
     Does this specific repo/branch match our federated credential config? Yes."
     → Returns an Azure access token ✅

  4. Pipeline uses the Azure token to deploy resources
  
RESULT: No long-lived secret was ever stored anywhere! 🎉
```

💡 **Real Example — Setting up OIDC in Terraform:**

```hcl
# STEP 1: Create an App Registration (an "app identity" in Entra ID)
# This is the identity that GitHub Actions will "become" when it authenticates
resource "azuread_application" "github_app" {
  display_name = "github-actions-myapp"   # Descriptive name
}

# STEP 2: Create a Service Principal for that App Registration
resource "azuread_service_principal" "github_sp" {
  client_id = azuread_application.github_app.client_id
}

# STEP 3: Set up Federated Credential — the "trust agreement" between GitHub and Azure
resource "azuread_application_federated_identity_credential" "github_oidc" {
  application_id = azuread_application.github_app.id
  display_name   = "github-actions-main-branch"

  # Tell Azure: trust tokens that come from...
  audiences = ["api://AzureADTokenExchange"]   # ← Standard Azure audience for OIDC
  issuer    = "https://token.actions.githubusercontent.com"  # ← GitHub's OIDC server

  subject   = "repo:myorg/myapp:ref:refs/heads/main"
  # ☝️ Only trust tokens from THIS specific repo AND branch
  # If someone tries to use a token from a different repo or branch, Azure denies it!
}

# STEP 4: Give this identity permission to deploy to Azure
resource "azurerm_role_assignment" "github_contributor" {
  scope                = "/subscriptions/${var.subscription_id}"  # Access to the whole subscription
  role_definition_name = "Contributor"   # Can create/modify resources (but not manage access)
  principal_id         = azuread_service_principal.github_sp.object_id
}
```

```yaml
# In your GitHub Actions workflow file (.github/workflows/deploy.yml):

name: Deploy to Azure

on:
  push:
    branches: [main]   # Trigger when code is pushed to the 'main' branch

permissions:
  id-token: write      # ← Required! Allows GitHub to generate an OIDC token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest   # Run on a GitHub-hosted Linux server
    steps:
      - name: Login to Azure using OIDC (no passwords!)
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}        # The App Registration's ID (not a secret!)
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}        # Your Entra ID tenant ID
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}  # Your Azure subscription ID
          # ☝️ Notice: NO client secret! Azure verifies identity via OIDC token instead
      
      - name: Deploy infrastructure
        run: terraform apply -auto-approve   # Deploy using Terraform
```

---

## 💡 Comparing Old Way vs. New Way

| Aspect | Old Way (Connection Strings) | New Way (Managed Identity) |
|--------|------------------------------|---------------------------|
| Secrets in code? | ❌ Yes — very risky! | ✅ No — completely eliminated |
| Rotation needed? | ❌ Yes — manual, easy to forget | ✅ No — Azure handles automatically |
| Cost | Free | ✅ Free |
| Setup complexity | Simple initially, risky long-term | Small initial setup, much safer |
| If code is stolen | ❌ Attacker gets all access | ✅ Attacker gets nothing useful |

---

## ✅ Best Practices Summary

### 1. 🚫 Never Hardcode Secrets

```
❌ db_password = "SuperSecret123!"     ← In your code
✅ credential = DefaultAzureCredential()  ← Identity-based, no secrets
```

### 2. 🎯 Use Least Privilege

**Least Privilege** means: give an identity the **minimum permissions** it needs to do its job, and nothing more.

```
❌ Giving your app the "Owner" role on the entire subscription
✅ Giving your app "Key Vault Secrets User" on one specific Key Vault
```

Like giving an intern a key only to the stationery cupboard, not to the entire building.

### 3. 💰 Remember: Managed Identities Are FREE!

There is absolutely no cost to enabling or using Managed Identities. There's no reason NOT to use them.

---

## ⚠️ Common Mistakes Beginners Make

1. **Using Service Principal secrets in pipelines** — The old way: creating a client secret and storing it in GitHub Secrets. Use OIDC + Workload Identity Federation instead. Secrets expire, get forgotten, and can be compromised.

2. **Assigning the "Owner" role** — "Owner" gives full control over everything in a subscription. Your app likely only needs to read one Key Vault secret. Use specific, narrow roles.

3. **Confusing System-Assigned and User-Assigned** — Use System-Assigned for simple single-resource scenarios. Use User-Assigned when multiple resources need the same access. Don't mix them up.

4. **Forgetting to assign RBAC roles** — Enabling a Managed Identity creates an identity, but it has NO permissions by default. You must separately assign roles. "I enabled Managed Identity but my app can't access Key Vault" is usually because the role assignment was forgotten.

5. **Not using Managed Identity at all** — Surprisingly common! Many beginners don't know this feature exists and keep using connection strings out of habit.

---

## 🎯 Key Takeaway

A **Managed Identity** gives your Azure resource (VM, App Service, Pipeline, etc.) an automatic, Azure-managed digital ID badge — eliminating the need to ever store passwords, keys, or secrets in your code. Always use Managed Identities instead of connection strings. For CI/CD pipelines, use **OIDC (Workload Identity Federation)** instead of long-lived secrets. This single practice prevents the majority of cloud security breaches.

---

## ❓ Beginner FAQ

**Q1: Can I use Managed Identity from my local development machine?**
> Managed Identities only work for resources running inside Azure (VMs, App Services, etc.). For local development on your laptop, you'd use `az login` (the Azure CLI login command) and `DefaultAzureCredential` falls back to your logged-in Azure account automatically. This is why `DefaultAzureCredential` is so convenient — it works both locally and in production without changing your code.

**Q2: What's the difference between a Managed Identity and a Service Principal?**
> A **Service Principal** is also an identity for an application in Entra ID, but YOU have to manage its credentials (create a secret/password, rotate it when it expires, store it securely). A **Managed Identity** is a special type of Service Principal where **Azure manages everything** — creation, rotation, deletion. Always prefer Managed Identity when possible; use Service Principals only when Managed Identity isn't available.

**Q3: What is Microsoft Entra ID? Is it the same as Active Directory?**
> Microsoft Entra ID (formerly called Azure Active Directory or Azure AD) is Microsoft's cloud-based identity service. Traditional **Active Directory (AD)** is an on-premises (runs in your own office/data center) system for managing Windows users and computers. Entra ID is its cloud version, designed for internet-scale apps and cloud services. They can work together but are different systems.

**Q4: How do I know if Managed Identity is working? How do I test it?**
> The easiest way is to check your application's logs — if it successfully reads a secret from Key Vault without any credentials in the code, it's working. You can also go to the Azure Portal (portal.azure.com), find your resource, look at the "Identity" tab, and see if "Status: On" appears for the identity. Then check the "Role assignments" in your Key Vault to confirm the identity has the right role.

**Q5: Is there any scenario where I MUST use a password/secret instead of Managed Identity?**
> Yes, a few. For example: connecting to external services outside Azure (like a third-party API that doesn't support OIDC). In those cases, store the credentials in [[Key-Vault]] and have your Managed Identity fetch them from there — the secret still never appears in your code!
