---
tags: [terraform, ci-cd, automation, pipeline]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# 🏗️ Terraform CI/CD Pipeline — Complete Guide in Simple Language

---

## 🤔 Why Should Terraform Run in a Pipeline (Not Locally)?

Imagine a team of 5 people all working on the same Terraform code, all running `terraform apply` from their own laptops. What happens?

- 😱 Person A runs `apply` — creates 3 VMs
- 😱 Person B simultaneously runs `apply` — creates 3 more VMs (now you have 6!)
- 😱 Person C accidentally has an older version of the state file — destroys what Person A created
- 😱 Nobody knows who applied what, or when

**Running Terraform from a CI/CD pipeline solves this:**
- ✅ Only ONE thing can run at a time (pipeline serializes changes)
- ✅ Every change is reviewed (via Pull Request) before it touches real infrastructure
- ✅ Complete audit trail in Git and pipeline logs
- ✅ No individual needs `az login` credentials to production — the pipeline handles it

> **Golden Rule:** In a professional environment, **ONLY the CI/CD pipeline applies Terraform to production**. Developers should never run `terraform apply` directly against production.

---

## 📋 The 3 Non-Negotiable Rules for Automated Terraform

### Rule 1: Remote State is Mandatory

A **state file** (`.tfstate`) is Terraform's memory — it tracks what infrastructure currently exists. When you run Terraform locally, this file is on your laptop. But:
- What if your laptop crashes?
- What if another team member needs to run Terraform?
- The pipeline runner is **ephemeral** — it's a fresh server created for each pipeline run and destroyed immediately after. Any local state file is lost!

**Solution: Store state in Azure Storage Account (a remote backend):**

```hcl
# backend.tf — Store state in Azure Blob Storage
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstateprod"    # Globally unique name
    container_name       = "tfstate"
    key                  = "prod/networking.tfstate"  # Path within the container
    # Authentication: Uses the pipeline's Managed Identity (no hardcoded keys!)
    use_oidc             = true
  }
}
```

**The state file in Storage Account acts as shared, persistent memory** that all pipeline runs and all team members can access safely.

### Rule 2: State Locking is Mandatory

What if two pipeline runs happen simultaneously? (e.g., someone merges two PRs at the same time)

Without locking: Both pipelines read state, both make changes, one overwrites the other = **state corruption** = infrastructure disaster.

Azure Storage Account blobs support **blob leasing** — when one pipeline run reads and writes state, it acquires a lease (a lock). Other pipeline runs must wait. 

This is configured automatically when you use `azurerm` backend — no extra setup needed.

### Rule 3: Non-Interactive Mode is Mandatory

A pipeline cannot answer questions. If Terraform says "Do you want to apply these changes? (yes/no)" — the pipeline hangs forever until it times out.

```bash
# ❌ Terraform will hang, waiting for you to type "yes"
terraform apply

# ✅ Always add -auto-approve in automation
terraform apply -input=false -auto-approve tfplan

# ❌ If a variable has no value, Terraform asks: "Enter a value for var.location:"
# The pipeline hangs.

# ✅ Always add -input=false to fail immediately if a variable is missing
terraform plan -input=false
```

---

## 🔄 The Standard Terraform Pipeline Workflow

The key insight: **Plan and Apply are separate pipeline stages, triggered at different times.**

```
Developer writes Terraform code changes
          │
          ▼
Developer opens a Pull Request (PR)
          │
          ▼
┌─────────────────────────────────────────┐
│  PR Phase ("Does this plan look good?")  │
│  1. terraform fmt -check                 │
│  2. terraform init                       │
│  3. terraform validate                   │
│  4. terraform plan → tfplan              │
│  5. Security scan (tfsec/checkov)        │
│  6. Post plan output to PR as comment    │
└─────────────────┬───────────────────────┘
                  │ Reviewer sees the plan, approves PR
                  │
                  ▼
Developer (or pipeline) merges PR to main
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Merge Phase ("Apply the exact plan")    │
│  1. terraform init                       │
│  2. terraform apply tfplan               │
│     (apply the EXACT plan from PR phase) │
└─────────────────────────────────────────┘
```

**Why save the plan file?**
In the PR phase you create `tfplan` (a saved plan). In the Apply phase, you apply THAT EXACT SAVED PLAN. This guarantees: "What the reviewer approved is EXACTLY what gets applied." No surprises.

---

## 📋 Complete Pipeline Example (Azure DevOps)

```yaml
# azure-pipelines.yml — Full Terraform CI/CD Pipeline

trigger: none      # Don't auto-trigger on push; this is a "apply" pipeline
                   # Triggered separately after PR pipeline

variables:
  TF_VERSION: '1.7.0'
  BACKEND_RG: 'rg-terraform-state'
  BACKEND_SA: 'stterraformstateprod'
  BACKEND_CONTAINER: 'tfstate'
  BACKEND_KEY: 'prod/main.tfstate'
  SERVICE_CONNECTION: 'azure-oidc-service-connection'

stages:

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 1: Validate & Plan (runs on every PR)
# ─────────────────────────────────────────────────────────────────────────────
- stage: Plan
  displayName: '📋 Validate & Plan'
  jobs:
  - job: TerraformPlan
    displayName: 'Terraform Plan'
    pool:
      vmImage: 'ubuntu-latest'
    
    steps:
    # Install the correct version of Terraform
    - task: TerraformInstaller@1
      displayName: '⚙️ Install Terraform v$(TF_VERSION)'
      inputs:
        terraformVersion: '$(TF_VERSION)'

    # Initialize Terraform (connect to remote state backend)
    - task: TerraformTaskV4@4
      displayName: '🔧 terraform init'
      inputs:
        provider: 'azurerm'
        command: 'init'
        backendServiceArm: '$(SERVICE_CONNECTION)'
        backendAzureRmResourceGroupName: '$(BACKEND_RG)'
        backendAzureRmStorageAccountName: '$(BACKEND_SA)'
        backendAzureRmContainerName: '$(BACKEND_CONTAINER)'
        backendAzureRmKey: '$(BACKEND_KEY)'

    # Check formatting — code must be properly formatted
    - script: |
        terraform fmt -check -recursive
        if [ $? -ne 0 ]; then
          echo "❌ Code is not formatted. Run 'terraform fmt' locally and commit."
          exit 1
        fi
        echo "✅ Formatting check passed"
      displayName: '🎨 terraform fmt -check'
      workingDirectory: '$(System.DefaultWorkingDirectory)'

    # Validate syntax
    - task: TerraformTaskV4@4
      displayName: '✅ terraform validate'
      inputs:
        provider: 'azurerm'
        command: 'validate'
        environmentServiceNameAzureRM: '$(SERVICE_CONNECTION)'

    # Security scan — find misconfigurations before they reach production
    - script: |
        # Install tfsec (Terraform security scanner)
        curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
        
        # Run scan — exit 1 if HIGH severity issues found
        tfsec . --minimum-severity HIGH --format lovely
      displayName: '🔒 Security Scan (tfsec)'
      workingDirectory: '$(System.DefaultWorkingDirectory)'
    
    # Create the plan and save it as a file
    - task: TerraformTaskV4@4
      displayName: '📋 terraform plan'
      inputs:
        provider: 'azurerm'
        command: 'plan'
        commandOptions: '-input=false -out=tfplan'    # Save plan to file
        environmentServiceNameAzureRM: '$(SERVICE_CONNECTION)'

    # Save the plan file as a pipeline artifact for the Apply stage to use
    - task: PublishBuildArtifacts@1
      displayName: '📤 Publish Plan File'
      inputs:
        pathToPublish: '$(System.DefaultWorkingDirectory)/tfplan'
        artifactName: 'terraform-plan'

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2: Apply (runs only on merge to main, with manual approval)
# ─────────────────────────────────────────────────────────────────────────────
- stage: Apply
  displayName: '🚀 Apply to Production'
  dependsOn: Plan
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  
  jobs:
  - deployment: TerraformApply
    displayName: 'Terraform Apply'
    environment: 'production'   # ← Pipeline pauses here for human approval!
    pool:
      vmImage: 'ubuntu-latest'
    
    strategy:
      runOnce:
        deploy:
          steps:
          - task: TerraformInstaller@1
            displayName: '⚙️ Install Terraform'
            inputs:
              terraformVersion: '$(TF_VERSION)'

          # Download the plan file created in Stage 1
          - download: current
            artifact: 'terraform-plan'
            displayName: '📥 Download Plan File'

          - task: TerraformTaskV4@4
            displayName: '🔧 terraform init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              backendServiceArm: '$(SERVICE_CONNECTION)'
              backendAzureRmResourceGroupName: '$(BACKEND_RG)'
              backendAzureRmStorageAccountName: '$(BACKEND_SA)'
              backendAzureRmContainerName: '$(BACKEND_CONTAINER)'
              backendAzureRmKey: '$(BACKEND_KEY)'

          # Apply ONLY the pre-approved plan file — no surprises!
          - task: TerraformTaskV4@4
            displayName: '🚀 terraform apply'
            inputs:
              provider: 'azurerm'
              command: 'apply'
              commandOptions: '-input=false -auto-approve $(Pipeline.Workspace)/terraform-plan/tfplan'
              environmentServiceNameAzureRM: '$(SERVICE_CONNECTION)'
```

---

## 🌿 Handling Multiple Environments (Dev/Staging/Prod)

### Option 1: Terraform Workspaces (Simple Projects)
```bash
terraform workspace new dev
terraform workspace new staging  
terraform workspace new prod

terraform workspace select dev
terraform plan -var-file="environments/dev.tfvars"
```

### Option 2: Separate State Files (Recommended for Enterprise)
Each environment has its own state file path:
```
tfstate/
├── dev/main.tfstate
├── staging/main.tfstate
└── prod/main.tfstate
```

Each pipeline stage uses a different `backendAzureRmKey` value pointing to its environment's state file.

---

## 🔒 Authentication in the Pipeline

**Never store Azure credentials (client secrets) in the pipeline!**

Use **OIDC / Workload Identity Federation** for the Service Connection. The pipeline authenticates to Azure using a short-lived token generated by Azure DevOps — no stored secrets.

```hcl
# Tell Terraform to use OIDC authentication automatically
provider "azurerm" {
  features {}
  use_oidc        = true    # Reads ARM_OIDC_TOKEN automatically set by the task
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.client_id
}
```

---

## ⚠️ Common Mistakes and Fixes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Running `terraform refresh` in pipeline | Command is DEPRECATED | Use `terraform plan -refresh-only` instead |
| Not using `-input=false` | Pipeline hangs forever waiting for input | Always add `-input=false` to all commands |
| Using local state | State lost after every pipeline run | Use `azurerm` backend in Storage Account |
| No state locking | Concurrent runs corrupt state | Storage Account backend provides this automatically |
| Applying without a plan file | Different resources might be changed than what was reviewed | Always `plan -out=tfplan`, then `apply tfplan` |
| Hardcoding subscription IDs | Security risk, not portable | Use `var.subscription_id` or environment variables |
| No drift detection | Production drifts from code silently | Set up a nightly pipeline that runs `terraform plan` and alerts if there's drift |

---

## 🕵️ Drift Detection — Keeping Reality in Sync with Code

**Configuration drift** happens when someone manually changes something in Azure (via portal or CLI) that doesn't match your Terraform code. Your code says "3 VMs" but production has "5 VMs" because someone added 2 manually.

**Solution: Nightly drift detection pipeline:**

```yaml
# Scheduled pipeline that runs every night at midnight
schedules:
- cron: '0 0 * * *'    # Every night at midnight
  displayName: Nightly Drift Detection
  branches:
    include:
    - main
  always: true          # Run even if no new commits

stages:
- stage: DriftCheck
  jobs:
  - job: CheckDrift
    steps:
    # ... init steps ...
    - task: TerraformTaskV4@4
      displayName: '🔍 Check for Drift'
      inputs:
        command: 'plan'
        commandOptions: '-input=false -detailed-exitcode'
        # Exit code 0 = no changes needed (good!)
        # Exit code 1 = error
        # Exit code 2 = changes detected (DRIFT!)
    
    - script: |
        if [ "$(terraform.plan.exitCode)" -eq "2" ]; then
          echo "⚠️ DRIFT DETECTED! Infrastructure has been changed outside of Terraform!"
          # Send alert to Teams/Slack
        fi
```

---

## 🎯 Key Takeaways

1. **Never apply Terraform locally to production** — only CI/CD pipelines do that
2. **Remote state is non-negotiable** — use Azure Storage Account backend
3. **Plan then Apply as separate stages** — reviewers see exactly what will change before it happens
4. **Use OIDC for authentication** — no client secrets, no expiry, no maintenance
5. **Always use `-input=false`** — prevents pipelines from hanging
6. **Use `-out=tfplan` and apply that file** — guarantees what's reviewed is what gets applied
7. **Set up drift detection** — nightly plan checks catch manual changes before they become problems
