---
tags: [ado, azure-devops, pipelines, templates, parameters, dry-principles]
source: devopsinsiders/batch-18
created: 2026-10-04
level: intermediate
---

# 📦 Parameterized Pipelines & Reusable YAML Templates

---

## 📖 Before You Read

- You know Azure DevOps YAML syntax and hierarchy → [[01-Azure-DevOps]]
- You understand multi-stage Terraform pipelines → [[05-Terraform-Pipeline]]
- You know how pipeline stages and jobs execute in parallel → [[09-Pipeline-Parallelism-and-Optimization]]

---

## 🛑 The Problem: Copy-Paste Antipattern Across Projects

In large enterprises, organizations often manage dozens or hundreds of infrastructure repositories (e.g., networking, AKS, storage, VMs, databases):

```
The Bad Practice (Copy-Paste Nightmare):
Project 1: azure-pipelines.yml (300 lines) ────┐
Project 2: azure-pipelines.yml (300 lines) ────┼──► Any change to security scans or Terraform
Project 3: azure-pipelines.yml (300 lines) ────┤    tasks requires updating 50+ repositories manually!
Project 10: azure-pipelines.yml (300 lines) ───┘
```

When every project copies the same 300 lines of pipeline YAML:
- ❌ **Zero Standardization:** One team runs tfsec v1.2, another runs v1.8, another forgets security scanning entirely.
- ❌ **Maintenance Nightmare:** Upgrading `TerraformTask@4` to `TerraformTask@5` requires modifying every repo.
- ❌ **No Governance:** Central cloud platform teams cannot enforce mandatory compliance gates across repositories.

---

## 💡 The Solution: Modular YAML Templates & Parameters

Azure DevOps supports **YAML Templates** and **Runtime Parameters**, allowing platform engineers to create a centralized pipeline template repository that application and infrastructure teams consume with a single clean configuration.

```
Enterprise DRY Architecture:
┌────────────────────────────────────────────────────────┐
│ Central Template Repo: "devopsinsiders-templates"      │
│  └── templates/                                        │
│      ├── steps/install-tools.yml                       │
│      ├── jobs/terraform-scan.yml                       │
│      └── stages/terraform-lifecycle.yml                │
└────────────────────────────────────────────────────────┘
                           ▲
       Called via `template:` or `extends:`
                           │
┌──────────────────────────┴─────────────────────────────┐
│ Project Repo: "axion-monolithic-infra"                 │
│  └── azure-pipelines.yml (Only 25 lines of config!)    │
└────────────────────────────────────────────────────────┘
```

---

## 🧩 Runtime Parameters in Azure DevOps

Parameters are evaluated at **pipeline compile time** before any job runs. They provide a user-friendly UI dropdown when triggering manual pipeline runs:

### Supported Parameter Data Types

| Type | Description | Allowed Values Example |
|------|-------------|------------------------|
| `string` | Text string | `'dev'`, `'preprod'`, `'prod'` |
| `number` | Integer or float | `1`, `5`, `10` |
| `boolean` | True / False checkbox | `true`, `false` |
| `object` | Complex YAML dictionary or list | Key-value pairs |
| `stepList` | List of pipeline steps | Injectable custom tasks |
| `jobList` | List of pipeline jobs | Injectable custom jobs |

### Parameter Block Example

```yaml
parameters:
  - name: environment
    displayName: 'Target Deployment Environment'
    type: string
    default: 'preprod'
    values:
      - 'dev'
      - 'preprod'
      - 'prod'

  - name: runSecurityScan
    displayName: 'Execute tfsec & Checkov Scans?'
    type: boolean
    default: true

  - name: autoApplyDev
    displayName: 'Auto-apply in Dev without manual gate?'
    type: boolean
    default: false
```

---

## 🏗️ Building Reusable YAML Templates (Step-by-Step)

### Step 1: Step Template (`templates/steps/tf-init-step.yml`)
Reusable step for running Terraform Init across any stage:

```yaml
# templates/steps/tf-init-step.yml
parameters:
  - name: workingDirectory
    type: string
  - name: serviceConnection
    type: string
  - name: storageAccount
    type: string
  - name: containerName
    type: string
  - name: stateKey
    type: string

steps:
  - task: TerraformTask@5
    displayName: '🔧 Terraform Init [${{ parameters.stateKey }}]'
    inputs:
      provider: 'azurerm'
      command: 'init'
      workingDirectory: '${{ parameters.workingDirectory }}'
      backendServiceArm: '${{ parameters.serviceConnection }}'
      backendAzureRmStorageAccountName: '${{ parameters.storageAccount }}'
      backendAzureRmContainerName: '${{ parameters.containerName }}'
      backendAzureRmKey: '${{ parameters.stateKey }}'
```

---

### Step 2: Stage Template (`templates/stages/terraform-deploy.yml`)
Encapsulates Init, Validate, Plan, Approval, and Apply:

```yaml
# templates/stages/terraform-deploy.yml
parameters:
  - name: environmentName
    type: string
  - name: workingDirectory
    type: string
  - name: serviceConnection
    type: string
  - name: storageAccount
    type: string
  - name: containerName
    type: string
  - name: stateKey
    type: string
  - name: isProduction
    type: boolean
    default: false

stages:
  - stage: Plan_${{ parameters.environmentName }}
    displayName: '📋 Plan — ${{ parameters.environmentName }}'
    jobs:
      - job: Plan
        displayName: 'Generate Plan'
        steps:
          - checkout: self

          - template: ../steps/tf-init-step.yml
            parameters:
              workingDirectory: '${{ parameters.workingDirectory }}'
              serviceConnection: '${{ parameters.serviceConnection }}'
              storageAccount: '${{ parameters.storageAccount }}'
              containerName: '${{ parameters.containerName }}'
              stateKey: '${{ parameters.stateKey }}'

          - task: TerraformTask@5
            displayName: '📋 Terraform Plan'
            inputs:
              provider: 'azurerm'
              command: 'plan'
              workingDirectory: '${{ parameters.workingDirectory }}'
              environmentServiceNameAzureRM: '${{ parameters.serviceConnection }}'
              commandOptions: '-out=$(Build.ArtifactStagingDirectory)/${{ parameters.environmentName }}.tfplan'

          - task: PublishPipelineArtifact@1
            displayName: '📤 Publish Plan Artifact'
            inputs:
              targetPath: '$(Build.ArtifactStagingDirectory)/${{ parameters.environmentName }}.tfplan'
              artifact: '${{ parameters.environmentName }}-plan'

  # Manual Gate: Only triggered if isProduction is true
  - ${{ if eq(parameters.isProduction, true) }}:
    - stage: Approval_${{ parameters.environmentName }}
      displayName: '🔐 Manual Gate — ${{ parameters.environmentName }}'
      dependsOn: Plan_${{ parameters.environmentName }}
      jobs:
        - job: ServerApproval
          pool: server
          steps:
            - task: ManualValidation@1
              displayName: 'Lead Approval Required for Production'
              inputs:
                notifyUsers: 'approvers@company.com'
                instructions: 'Verify production plan artifact before approving apply.'

  - stage: Apply_${{ parameters.environmentName }}
    displayName: '🚀 Apply — ${{ parameters.environmentName }}'
    dependsOn:
      - ${{ if eq(parameters.isProduction, true) }}:
        - Approval_${{ parameters.environmentName }}
      - ${{ if eq(parameters.isProduction, false) }}:
        - Plan_${{ parameters.environmentName }}
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - job: Apply
        displayName: 'Apply Plan'
        steps:
          - checkout: self

          - task: DownloadPipelineArtifact@2
            displayName: '📥 Download Plan'
            inputs:
              buildType: 'current'
              artifactName: '${{ parameters.environmentName }}-plan'
              targetPath: '${{ parameters.workingDirectory }}'

          - template: ../steps/tf-init-step.yml
            parameters:
              workingDirectory: '${{ parameters.workingDirectory }}'
              serviceConnection: '${{ parameters.serviceConnection }}'
              storageAccount: '${{ parameters.storageAccount }}'
              containerName: '${{ parameters.containerName }}'
              stateKey: '${{ parameters.stateKey }}'

          - task: TerraformTask@5
            displayName: '🚀 Terraform Apply'
            inputs:
              provider: 'azurerm'
              command: 'apply'
              workingDirectory: '${{ parameters.workingDirectory }}'
              environmentServiceNameAzureRM: '${{ parameters.serviceConnection }}'
              commandOptions: '${{ parameters.workingDirectory }}/${{ parameters.environmentName }}.tfplan -auto-approve'
```

---

### Step 3: Consuming the Template in Your Root Pipeline

In the actual application or infrastructure repository, the pipeline becomes ultra-concise and clean:

```yaml
# azure-pipelines.yml (In Root Repository)
trigger:
  branches:
    include:
      - main
      - feature/*

pool:
  name: vistara-agents

parameters:
  - name: targetEnv
    displayName: 'Environment to Deploy'
    type: string
    default: 'preprod'
    values:
      - 'preprod'
      - 'prod'

stages:
  # Deploy Preprod
  - ${{ if eq(parameters.targetEnv, 'preprod') }}:
    - template: templates/stages/terraform-deploy.yml
      parameters:
        environmentName: 'Preprod'
        workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'
        serviceConnection: 'corp-preprod-sc'
        storageAccount: 'distoragetf786'
        containerName: 'tfstate'
        stateKey: 'preprod.terraform.tfstate'
        isProduction: false

  # Deploy Production
  - ${{ if eq(parameters.targetEnv, 'prod') }}:
    - template: templates/stages/terraform-deploy.yml
      parameters:
        environmentName: 'Production'
        workingDirectory: '$(System.DefaultWorkingDirectory)/environments/prod'
        serviceConnection: 'corp-prod-sc'
        storageAccount: 'distoragetf786'
        containerName: 'tfstate'
        stateKey: 'prod.terraform.tfstate'
        isProduction: true
```

---

## ⚡ Compile-Time vs Runtime Evaluation

Understanding the difference between compile-time expressions and runtime conditions is essential:

```
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│ Compile-Time Expression: `${{ ... }}`        │ Runtime Variable: `$( ... )` or `eq(...)`     │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ Evaluated BEFORE the pipeline starts running. │ Evaluated DURING pipeline execution.          │
│ Used for inserting stages, jobs, parameters,  │ Used in job/stage `condition:` and task       │
│ or loops (`${{ each item in list }}`).       │ input fields.                                 │
│ Example: `${{ if eq(parameters.env, 'prod')}}`│ Example: `eq(variables['Build.SourceBranch'],  │
│                                               │         'refs/heads/main')`                   │
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 🎯 Key Takeaways & Best Practices

1. **Use `parameters` for User Choices:** When engineers trigger pipelines manually from the ADO UI, parameters give a validated dropdown rather than freeform text variables.
2. **One Central Repository for Templates:** Place pipeline templates in a central repository (e.g., `infra-pipeline-templates`) and reference it as a repository resource.
3. **Keep Child Repos Lightweight:** Application developers should not need to understand complex Azure DevOps YAML syntax. They provide 15 lines of config; the templates handle compliance, linting, scanning, plan storage, and approval gates.
4. **Enforce Branch Conditions:** Never allow a feature branch run to deploy to production. Use both parameter filtering and `eq(variables['Build.SourceBranch'], 'refs/heads/main')`.

---

## 🔗 Related Notes

- [[01-Azure-DevOps]] — Azure DevOps Complete Beginner Guide
- [[05-Terraform-Pipeline]] — Multi-stage Terraform CI/CD Workflow
- [[09-Pipeline-Parallelism-and-Optimization]] — Pipeline Parallelism and Optimization
- [[06-Axion-3-Tier-Enterprise-Project]] — Axion 3-Tier Enterprise Infrastructure & Pipeline
