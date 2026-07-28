---
tags: [terraform, remote-backend, state, azure, state-locking]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-07-28
---

# Terraform Remote Backends on Azure: From Basics to Production

## 📖 Introduction
By default, Terraform stores the crucial State File (`terraform.tfstate`) locally on your hard drive. This is known as a **Local Backend**. While suitable for learning, it becomes a disaster waiting to happen for enterprise DevOps teams.

A **Remote Backend** solves this by configuring Terraform to store and manage the State File in a centralized, highly secure cloud location—in our case, an **Azure Storage Account**.

---

## 🧠 Why Remote Backend?
There are three massive problems with keeping the state file on your laptop:
1. **Collaboration:** If your coworker runs the code, they don't have your state file. Terraform will try to build duplicate resources and fail.
2. **Security:** The State File contains sensitive passwords and keys in plain, readable text. Keeping passwords on a developer's laptop is a huge security risk.
3. **Concurrency (Corruption):** What if you and your coworker both type `terraform apply` at the exact same second? You will corrupt the infrastructure state.

A Remote Backend solves all of this by centralizing the file, encrypting it at rest, and providing a feature called **State Locking**.

---

## 🏗️ Setup (Storage Account + Blob)

To use a remote backend in Azure, we need a Storage Account and a Blob Container. We also must enable **Versioning** to keep a history of our state files (crucial for disaster recovery).

### Bash Bootstrap Script
Here is a production-grade Bash script to bootstrap the remote state infrastructure using the Azure CLI:

```bash
#!/bin/bash
# setup-backend.sh

RESOURCE_GROUP_NAME="rg-terraform-state-prod"
STORAGE_ACCOUNT_NAME="sttfstateprod$(date +%s)" # Ensuring global uniqueness
CONTAINER_NAME="tfstate"
LOCATION="eastus"

# 1. Create Resource Group
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# 2. Create Storage Account (Standard tier, LRS for cost, but GRS recommended for Prod)
az storage account create \
  --name $STORAGE_ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  --location $LOCATION \
  --sku Standard_LRS \
  --encryption-services blob

# 3. Enable Versioning (Crucial for state file recovery)
az storage account blob-service-properties update \
  --account-name $STORAGE_ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  --enable-versioning true

# 4. Create Blob Container
az storage container create \
  --name $CONTAINER_NAME \
  --account-name $STORAGE_ACCOUNT_NAME \
  --auth-mode login

echo "✅ Storage Account Name: $STORAGE_ACCOUNT_NAME"
```

---

## ⚙️ Backend Configuration

Once the infrastructure is ready, you must configure Terraform to use it. Add this `backend` block to your Terraform configuration.

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state-prod"
    storage_account_name = "sttfstateprod12345678"
    container_name       = "tfstate"
    
    # The exact name we want to give our state file
    key                  = "core-infrastructure.tfstate"
    
    # Enable OIDC / Managed Identity instead of Access Keys
    use_oidc             = true
  }
}
```

*Note: We do not put credentials in this block. Authentication is handled outside of the code.*

---

## 🔒 State Locking Deep Dive

**State Locking** prevents two processes from modifying the state file at the same time, preventing corruption.

In Azure, Terraform implements state locking using a native Storage Account feature called a **Blob Lease**. 

### How it works:
```text
[Terraform Apply Started]
         |
         v
[Request Lease] ----> Azure Storage Account (Blob: core-infrastructure.tfstate)
         |               |
         |               +--> Status: "Leased" (Locked for others)
         v
[Deploy Infrastructure]
         |
         v
[Update State File]
         |
         v
[Release Lease] ----> Azure Storage Account
                         |
                         +--> Status: "Available" (Unlocked)
```

If another user runs `terraform apply` while the file is Leased, Azure rejects the request, and Terraform prints a "State is Locked" error.

---

## 🌍 Environment-wise State Strategy

When managing multiple environments (Dev, Staging, Prod), you must separate their state files. Never mix environment states! Here are the three strategies, from simplest to most robust:

### 1. Separate Key in the Same Container (Basic)
All environments share a Storage Account and Container, but use different filenames (`key`).
- Dev: `key = "dev.tfstate"`
- Prod: `key = "prod.tfstate"`
*Pros: Easy setup.*
*Cons: High risk. Someone with access to Dev can accidentally read/delete Prod state.*

### 2. Separate Container per Environment (Better)
All environments share a Storage Account, but use different containers.
- Dev Container: `tfstate-dev`
- Prod Container: `tfstate-prod`
*Pros: Better organization, allows setting RBAC at the container level.*
*Cons: Still shares the underlying Storage Account. Blast radius is still large.*

### 3. Separate Storage Account per Environment (Production-Grade)
Every environment gets its own dedicated Storage Account (and often its own Subscription).
- Dev: `sttfstatedev001` in Dev Subscription
- Prod: `sttfstateprod001` in Prod Subscription
*Pros: Total isolation. Smallest blast radius. Maximum security.*
*Cons: Requires managing multiple storage accounts.*

---

## 🚀 CI/CD Integration

In CI/CD, we use Service Principals or Managed Identities to authenticate. Here is a GitHub Actions snippet using OIDC (OpenID Connect) to authenticate to Azure without storing long-lived secrets.

```yaml
name: Terraform Deploy

on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      ARM_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      ARM_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      ARM_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      ARM_USE_OIDC: true
      
    steps:
      - uses: actions/checkout@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          client-id: ${{ env.ARM_CLIENT_ID }}
          tenant-id: ${{ env.ARM_TENANT_ID }}
          subscription-id: ${{ env.ARM_SUBSCRIPTION_ID }}

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: terraform init

      - name: Terraform Apply
        run: terraform apply -auto-approve
```

---

## 🛡️ Security Best Practices

1. **Role-Based Access Control (RBAC):** Do not give users "Storage Account Contributor". Use the built-in "Storage Blob Data Contributor" role scoped specifically to the container.
2. **Managed Identity / OIDC vs Access Keys:** Never use Storage Account Access Keys (`account_key`). They are long-lived and dangerous. Use Azure AD (Entra ID) authentication via OIDC or Managed Identities.
3. **Soft Delete & Versioning:** Always enable Blob Soft Delete (min 7 days) and Blob Versioning. If a pipeline corrupts the state, you can instantly revert to the previous version.
4. **Network Restrictions:** Restrict the Storage Account firewall to only allow traffic from your CI/CD runners' IP addresses or specific Azure Virtual Networks.

---

## 🎤 Interview Q&A

**Q1: What happens if a pipeline crashes mid-deployment while using a remote backend?**
**A1:** The state file remains locked because Terraform couldn't release the Blob Lease. Subsequent runs will fail with a "State is locked" error. An admin must manually log into Azure Storage and "Break the Lease" on the `.tfstate` blob.

**Q2: How do you migrate local state to an Azure remote backend?**
**A2:** First, add the `backend "azurerm" {}` block to your code. Then, run `terraform init`. Terraform will detect the local state file and prompt: "Do you want to copy existing state to the new backend?" Type `yes`.

**Q3: Why shouldn't we put the Azure Storage Account Access Key in the backend block?**
**A3:** It is a massive security vulnerability to hardcode secrets in source control. Instead, rely on the `ARM_USE_OIDC` environment variable or `az login` to authenticate dynamically using Entra ID (Azure AD).

**Q4: We have Dev, Staging, and Prod. How should we structure our state files in Azure?**
**A4:** The most secure, production-grade approach is complete isolation: a separate Azure Storage Account (and ideally separate Azure Subscriptions) for each environment. This prevents cross-environment contamination and limits the blast radius of a security breach.

**Q5: What Azure feature provides Terraform state locking?**
**A5:** Terraform uses the Azure Blob Lease mechanism. It acquires an exclusive write lock on the blob during an operation, preventing concurrent modifications.

**Q6: We accidentally deleted our state file in Azure. How do we recover?**
**A6:** If you followed best practices and enabled "Blob Versioning" and "Soft Delete" on the Storage Account, you can navigate to the Azure Portal, view deleted blobs/versions, and restore the previous version of the `.tfstate` file.