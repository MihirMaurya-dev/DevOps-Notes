---
tags: [terraform, github-actions, azure, oidc, ci-cd, feature-branch, pull-request, production-approval]
source: devopsinsiders/batch-18
created: 2026-08-09
updated: 2026-08-09
---

# 🚀 GitHub Actions + Azure OIDC — Complete Terraform CI/CD Flow

---

## 🗺️ Complete Flow Overview

```text
Local Machine
     ↓
GitHub Main Branch Protection
     ↓
Clone Repo
     ↓
Feature Branch
     ↓
Terraform Code Change
     ↓
git push feature/*
     ↓
GitHub Actions
     ↓
Azure Login via OIDC
     ↓
Terraform Scan
     ↓
Terraform Init
     ↓
Terraform Validate
     ↓
Terraform Plan
     ↓
PR
     ↓
Review + Merge
     ↓
Main Branch
     ↓
Azure Login via OIDC
     ↓
Terraform Plan
     ↓
Manual Approval
     ↓
Terraform Apply
     ↓
Azure
```

---

## Step 1 — GitHub `main` Branch Protection

**Repo → Settings → Rules → Rulesets → New ruleset**

`main` ke liye ye settings enable karo:

| Rule | Setting |
|------|---------|
| Require pull request | ✅ ON |
| Require 1 approval | ✅ ON |
| Require status checks | ✅ ON |
| Block force pushes | ✅ ON |
| Block deletion | ✅ ON |
| Direct push to main | ❌ OFF |

> **Result:** Developer ab directly `main` branch me push nahi kar sakta. Sabko PR se jaana padega.

---

## Step 2 — Azure me App Registration Banao

**Azure Portal → Microsoft Entra ID → App registrations → New registration**

```text
Name: github-terraform-oidc
```

Create karne ke baad ye values note karo:

```text
Tenant ID     = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Client ID     = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Step 3 — Service Principal Create Karo

App Registration ke liye service principal available hona chahiye.

```bash
# Azure me login karo
az login

# Current subscription check karo
az account show

# Correct subscription select karo
az account set --subscription "<SUBSCRIPTION_ID>"

# Service Principal create karo
az ad sp create --id <CLIENT_ID>
```

---

## Step 4 — Azure RBAC Permission Do

**Subscription-level example:**

```bash
az role assignment create \
  --assignee <CLIENT_ID> \
  --role Contributor \
  --scope /subscriptions/<SUBSCRIPTION_ID>
```

> ⚠️ **Production Best Practice:** Subscription-level Contributor blindly mat do.
>
> Better approach — **Least Privilege RBAC:**
> ```text
> Resource Group
>       ↓
> Contributor (only on required RG)
> ```
> Ya required resources ke according specific role assign karo.

---

## Step 5 — GitHub OIDC Federated Credential Banao

**Azure Portal:**

```text
Entra ID → App registrations → github-terraform-oidc
        → Certificates & secrets → Federated credentials → Add credential
```

### Main Branch ke liye Trust:

```text
Organization:  YOUR_ORG
Repository:    YOUR_ORG/YOUR_REPO
Entity type:   Branch
Branch:        main
```

### PR Workflow ke liye Trust:

Agar PR-triggered workflow me Azure login chahiye, **alag federated credential** banao:

```text
Organization:  YOUR_ORG
Repository:    YOUR_ORG/YOUR_REPO
Entity type:   Pull Request
```

> **Why two credentials?** OIDC trust subject PR aur Branch ke liye alag hota hai. Dono ka ek credential nahi ban sakta.

---

## Step 6 — GitHub Variables Configure Karo

**Repo → Settings → Secrets and variables → Actions → Variables**

```text
AZURE_CLIENT_ID       = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_TENANT_ID       = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_SUBSCRIPTION_ID = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> **Note:** IDs technically secret nahi hote, lekin centralized configuration ke liye **GitHub Variables** (not Secrets) use karo. Client Secret ki zarurat hi nahi hai — OIDC use kar rahe hain.

---

## Step 7 — Local Repo Clone Karo

```bash
git clone https://github.com/<ORG>/<REPO>.git
cd <REPO>
git checkout main
git pull origin main
```

---

## Step 8 — Feature Branch Banao

```bash
git checkout -b feature/terraform-modules
```

### Recommended Terraform Project Structure:

```text
.
├── main.tf
├── provider.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
│
└── modules/
    ├── resource_group/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    ├── vnet/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    ├── subnet/
    ├── nsg/
    └── vm/
```

---

## Step 9 — Feature Branch me Code Change Karo

```bash
# Code format karo
terraform fmt -recursive

# Local validation
terraform init
terraform validate
terraform plan

# Git me commit karo
git status
git add .
git commit -m "Add Terraform parent and child modules"
git push -u origin feature/terraform-modules
```

---

## Step 10 — GitHub Actions Workflow YAML

**File path:** `.github/workflows/terraform.yml`

```yaml
name: Terraform CI/CD

on:
  push:
    branches:
      - main
      - 'feature/**'

  pull_request:
    branches:
      - main

permissions:
  id-token: write   # Required for OIDC
  contents: read

jobs:

  # ───────────────────────────────────────────────────────
  # JOB 1: Plan — Runs on feature push AND PR
  # ───────────────────────────────────────────────────────
  terraform-plan:

    name: Terraform Scan and Plan

    runs-on: ubuntu-latest

    steps:

      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Azure Login - OIDC
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Verify Azure Login
        run: az account show

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Upload Terraform Plan
        uses: actions/upload-artifact@v4
        with:
          name: terraform-plan
          path: tfplan


  # ───────────────────────────────────────────────────────
  # JOB 2: Apply — Runs ONLY on merge to main
  # ───────────────────────────────────────────────────────
  terraform-apply:

    name: Terraform Apply

    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    needs: terraform-plan

    runs-on: ubuntu-latest

    environment:
      name: production   # ← Yahan pipeline ruk jaata hai approval ke liye

    steps:

      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Azure Login - OIDC
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init

      - name: Download Terraform Plan
        uses: actions/download-artifact@v4
        with:
          name: terraform-plan

      - name: Terraform Apply
        run: terraform apply -auto-approve tfplan
```

### 🔑 Key Design Decisions

| Decision | Reason |
|----------|--------|
| `id-token: write` permission | OIDC token generate karne ke liye required |
| `terraform plan -out=tfplan` | Plan file save karo — same file apply hogi |
| `upload-artifact` + `download-artifact` | Plan ko Plan job se Apply job me transfer karo |
| `environment: production` | Is point pe pipeline approval ke liye ruk jaata hai |
| `if: github.ref == 'refs/heads/main'` | Apply sirf main branch merge pe chalega |

---

## Step 11 — Production Approval Configure Karo

**GitHub → Settings → Environments → New environment**

```text
Name: production
```

Then:

```text
Environment → Required reviewers → Add reviewer (your GitHub username or team)
```

**Ab flow ye hoga:**

```text
Terraform Plan (auto)
      ↓
⏸️ Waiting for approval...
      ↓
Reviewer approves in GitHub
      ↓
Terraform Apply (runs)
```

---

## Step 12 — Feature Branch Push ka Result

```bash
git push origin feature/terraform-modules
```

Pipeline chalega aur **sirf yahan tak jaayega:**

```text
Checkout
   ↓
Azure Login (OIDC)
   ↓
Terraform fmt check
   ↓
Terraform init
   ↓
Terraform validate
   ↓
Terraform plan ✅
   ↓
(STOPS — Apply nahi hoga feature branch pe)
```

---

## Step 13 — PR Create Karo

GitHub UI me:

```text
feature/terraform-modules
          ↓
     Pull Request
          ↓
         main
```

Reviewer:
1. PR me Terraform plan output dekhe
2. Code review kare
3. Approve kare
4. **Merge Pull Request** click kare

---

## Step 14 — Main Branch Pipeline (Full Flow)

Merge hote hi automatically trigger hoga:

```text
main
 ↓
Azure Login (OIDC)
 ↓
Terraform fmt check
 ↓
Terraform init
 ↓
Terraform validate
 ↓
Terraform plan (same tfplan artifact)
 ↓
Production Environment
 ↓
⏸️ Manual Approval
 ↓
Terraform Apply
 ↓
Azure Infrastructure ✅
```

---

## 💡 Important: Same Plan Apply Karna Better Practice Hai

> **Ek common galati:** Main branch pe dobara naya `terraform plan` generate karna aur phir apply karna.
>
> **Problem:** PR reviewer ne jo plan dekha aur approve kiya, aur jo actually apply hua — dono alag ho sakte hain agar beech me koi change aa jaaye.
>
> **Better Practice:** Feature/PR phase me bana `tfplan` artifact ko **hi** main branch ke apply step me use karo. Upar wale workflow me yahi approach hai:
> ```
> upload-artifact (Plan job) → download-artifact (Apply job) → apply tfplan
> ```
>
> **Result:** "What reviewer approved = Exactly what gets applied." No surprises.

---

## 🎤 Interview me Poora Flow Kaise Explain Karna

> *"We have protected the main branch and disabled direct pushes. Developers work on feature branches and raise PRs. Feature branch execution performs Azure OIDC authentication followed by Terraform formatting, initialization, validation, and plan only — apply nahi hota. After code review and approval, the PR is merged into main. The main branch pipeline again authenticates to Azure using GitHub OIDC, performs Terraform plan, and waits at a protected production environment for manual approval. After approval, the same pre-reviewed Terraform plan artifact is applied to Azure — ensuring what the reviewer approved is exactly what gets deployed."*

---

## 🔗 Related Notes

- [[05-Terraform-Pipeline|Terraform-Pipeline]] — Azure DevOps equivalent pipeline
- [[02-GitHub-Actions|GitHub-Actions]] — GitHub Actions fundamentals
- [[09-Remote-Backend]] — Terraform remote state (required for pipeline)
- [[15-Best-Practices]] — Terraform production best practices
