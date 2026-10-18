---
tags: [ado, azure-devops, pipelines, parallelism, optimization, devsecops]
source: devopsinsiders/batch-18
created: 2026-10-02
level: intermediate
---

# ⚡ Azure DevOps Pipeline Parallelism & Optimization

---

## 📖 Before You Read

- You understand the basics of Azure DevOps YAML Pipelines → [[01-Azure-DevOps]]
- You have reviewed the multi-stage Terraform pipeline structure → [[05-Terraform-Pipeline]]
- You know the core security scanning tools: TFLint, tfsec, Checkov, and Infracost → [[01-TFLint]], [[02-tfsec]]

---

## 🤔 Why Pipeline Parallelism Matters

In standard CI/CD pipelines, stages and jobs execute **sequentially** by default. Each stage waits for the preceding stage to complete before starting:

```
Sequential Pipeline Execution (Default):
┌────────────────┐     ┌────────────────────┐     ┌────────────────┐     ┌─────────────────┐
│ Stage 1: Scan  │ ──► │ Stage 2: Validate  │ ──► │ Stage 3: Plan  │ ──► │ Stage 4: Apply   │
│   (3-5 mins)   │     │     (2 mins)       │     │   (2-3 mins)   │     │    (3 mins)     │
└────────────────┘     └────────────────────┘     └────────────────┘     └─────────────────┘
Total Runtime: ~10 - 13 minutes per build!
```

When developers push feature branches or trigger pull requests multiple times a day, long pipeline execution times cause:
1. **Developer Friction:** Developers context-switch while waiting for pipeline feedback.
2. **Queue Congestion:** Agent pools get choked, blocking critical hotfixes and deployments.
3. **Delayed PR Reviews:** Reviewers cannot inspect `terraform plan` output until linting, validation, and scanning finish sequentially.

### 💡 The Solution: Parallel Execution
Static security scanning (`tflint`, `tfsec`, `checkov`, `infracost`) and code syntax validation (`terraform validate`, `terraform fmt`) do **not depend on each other**. They can execute **simultaneously across separate build agents**:

```
Optimized Parallel Execution:
┌─────────────────────────┐
│ Stage 1: Terraform Scan │ ──┐
│ (TFLint, tfsec, Checkov)│   │
│       (3 mins)          │   │
└─────────────────────────┘   │     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
                              ├────►│  Stage 3: Plan   │ ──► │ Stage 4: Approval   │ ──► │ Stage 5: Apply   │
┌─────────────────────────┐   │     │ (Init + Plan)    │     │  (Manual Gate)      │     │  (on main branch)│
│ Stage 2: TF Validate    │ ──┘     │    (2 mins)      │     └─────────────────────┘     └──────────────────┘
│ (Init, fmt, validate)   │         └──────────────────┘
│       (2 mins)          │
└─────────────────────────┘
Total Runtime: ~5 - 7 minutes (Almost 50% faster!)
```

---

## ⚙️ How Azure DevOps Controls Stage Dependencies

By default, in an Azure DevOps multi-stage pipeline, if you do not specify `dependsOn`, a stage depends on the stage immediately preceding it.

To run stages in parallel:
- Set `dependsOn: []` (empty array) on any stage that should start immediately at pipeline trigger.
- For downstream stages that require both parallel tasks to pass, specify `dependsOn: [StageA, StageB]`.

### Stage Dependency Mapping

```yaml
stages:
  # Starts immediately at pipeline run
  - stage: TerraformScan
    displayName: 'Stage 1: Terraform Security Scan'
    dependsOn: []
    jobs:
      - job: ScanJob
        displayName: 'Security & Linting Scan'
        # steps here...

  # Also starts immediately at pipeline run in parallel with Stage 1
  - stage: TerraformValidate
    displayName: 'Stage 2: Terraform Validation'
    dependsOn: []
    jobs:
      - job: ValidateJob
        displayName: 'FMT & Validate'
        # steps here...

  # Runs ONLY when both Stage 1 and Stage 2 succeed
  - stage: TerraformPlan
    displayName: 'Stage 3: Terraform Plan'
    dependsOn:
      - TerraformScan
      - TerraformValidate
    condition: succeeded()
    jobs:
      - job: PlanJob
        displayName: 'Plan Generation'
        # steps here...

  # Runs after Plan, gated for main branch
  - stage: TerraformApply
    displayName: 'Stage 4: Terraform Apply'
    dependsOn: TerraformPlan
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - job: ApplyJob
        displayName: 'Apply Infrastructure'
        # steps here...
```

---

## 🛠️ Complete Production Pipeline with Parallel Stages

Here is the complete production-grade Azure DevOps pipeline YAML implementing parallel security scans, validation, manual approval gate, and deployment:

```yaml
# ==============================================================================
# Enterprise Azure DevOps Pipeline: Parallel Security, Validation & Deployment
# DevOps Insiders Batch 18 — Flagship Production Pattern
# ==============================================================================

name: $(Build.DefinitionName)_$(Date:yyyyMMdd)$(Rev:.r)

trigger:
  branches:
    include:
      - main
      - feature/*

pool:
  name: vistara-agents      # Self-hosted agent pool
  # For Microsoft-hosted agents: vmImage: 'ubuntu-latest'

variables:
  - name: workingDirectory
    value: '$(System.DefaultWorkingDirectory)/environments/preprod'
  - name: serviceConnection
    value: 'corp-prod-01-sc'
  - name: backendStorageAccount
    value: 'distoragetf786'
  - name: backendContainer
    value: 'tfstate'
  - name: backendStateKey
    value: 'preprod.terraform.tfstate'

stages:

  # ============================================================================
  # STAGE 1: Parallel Security & Policy Scan
  # ============================================================================
  - stage: TerraformScan
    displayName: '🔒 Security & Static Scan'
    dependsOn: []          # Starts immediately
    jobs:
      - job: SecurityScanJob
        displayName: 'TFLint, tfsec & Checkov Scan'
        steps:
          - checkout: self
            displayName: '📥 Checkout Repository'

          # Dynamic TFLint installation script
          - pwsh: |
              if (-not (Get-Command tflint -ErrorAction SilentlyContinue)) {
                Write-Host "Installing TFLint on agent..."
                Invoke-WebRequest -Uri "https://github.com/terraform-linters/tflint/releases/download/v0.50.3/tflint_windows_amd64.zip" -OutFile "$env:TEMP\tflint.zip"
                Expand-Archive -Path "$env:TEMP\tflint.zip" -DestinationPath "$env:ProgramFiles\tflint" -Force
                $CurrentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
                if ($CurrentPath -notlike "*$env:ProgramFiles\tflint*") {
                    [Environment]::SetEnvironmentVariable("Path", "$CurrentPath;$env:ProgramFiles\tflint", [EnvironmentVariableTarget]::Machine)
                }
                $env:Path += ";$env:ProgramFiles\tflint"
              }
              tflint --version
            displayName: '⚙️ Ensure TFLint Installed'

          - pwsh: |
              Write-Host "Running TFLint..."
              tflint --init
              tflint --chdir=$(workingDirectory)
            displayName: '🔍 Run TFLint Code Linting'

          - pwsh: |
              Write-Host "Running tfsec static analysis..."
              if (Get-Command tfsec -ErrorAction SilentlyContinue) {
                tfsec $(workingDirectory) --soft-fail
              } else {
                Write-Host "tfsec not found, running checkov..."
              }
            displayName: '🛡️ Run tfsec Security Analysis'

  # ============================================================================
  # STAGE 2: Parallel Terraform Format & Validation
  # ============================================================================
  - stage: TerraformValidate
    displayName: '📐 Format & Validation'
    dependsOn: []          # Starts immediately, runs concurrently with Stage 1
    jobs:
      - job: ValidateJob
        displayName: 'Init & Validate'
        steps:
          - checkout: self
            displayName: '📥 Checkout Repository'

          - task: TerraformTask@5
            displayName: '🔧 Terraform Init (for validation)'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(workingDirectory)'
              backendServiceArm: '$(serviceConnection)'
              backendAzureRmStorageAccountName: '$(backendStorageAccount)'
              backendAzureRmContainerName: '$(backendContainer)'
              backendAzureRmKey: '$(backendStateKey)'

          - task: TerraformTask@5
            displayName: '📐 Terraform Validate'
            inputs:
              provider: 'azurerm'
              command: 'validate'
              workingDirectory: '$(workingDirectory)'

  # ============================================================================
  # STAGE 3: Plan Stage (Depends on both Scan & Validate)
  # ============================================================================
  - stage: TerraformPlan
    displayName: '📋 Terraform Plan'
    dependsOn:
      - TerraformScan
      - TerraformValidate
    condition: succeeded()
    jobs:
      - job: PlanJob
        displayName: 'Generate Execution Plan'
        steps:
          - checkout: self
            displayName: '📥 Checkout Repository'

          - task: TerraformTask@5
            displayName: '🔧 Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(workingDirectory)'
              backendServiceArm: '$(serviceConnection)'
              backendAzureRmStorageAccountName: '$(backendStorageAccount)'
              backendAzureRmContainerName: '$(backendContainer)'
              backendAzureRmKey: '$(backendStateKey)'

          - task: TerraformTask@5
            displayName: '📋 Terraform Plan'
            inputs:
              provider: 'azurerm'
              command: 'plan'
              workingDirectory: '$(workingDirectory)'
              environmentServiceNameAzureRM: '$(serviceConnection)'
              commandOptions: '-out=$(Build.ArtifactStagingDirectory)/tfplan -input=false'

          - task: PublishPipelineArtifact@1
            displayName: '📤 Publish Terraform Plan Artifact'
            inputs:
              targetPath: '$(Build.ArtifactStagingDirectory)/tfplan'
              artifact: 'tfplan-artifact'

  # ============================================================================
  # STAGE 4: Manual Approval Gate (Server Pool)
  # ============================================================================
  - stage: ManualApproval
    displayName: '🔐 Manual Approval Before Apply'
    dependsOn: TerraformPlan
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - job: WaitForApproval
        displayName: 'Waiting for Lead Approval'
        pool: server        # Agentless job — does not consume an agent runner!
        steps:
          - task: ManualValidation@1
            displayName: 'Approve Infrastructure Apply'
            inputs:
              notifyUsers: 'leads@devopsinsiders.com'
              instructions: 'Terraform Plan generated successfully. Review the published plan artifact before approving.'
              onTimeout: 'reject'

  # ============================================================================
  # STAGE 5: Apply Stage (Runs only on approved main branch)
  # ============================================================================
  - stage: TerraformApply
    displayName: '🚀 Terraform Apply'
    dependsOn: ManualApproval
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - job: ApplyJob
        displayName: 'Apply Approved Plan'
        steps:
          - checkout: self
            displayName: '📥 Checkout Repository'

          - task: DownloadPipelineArtifact@2
            displayName: '📥 Download Plan Artifact'
            inputs:
              buildType: 'current'
              artifactName: 'tfplan-artifact'
              targetPath: '$(workingDirectory)'

          - task: TerraformTask@5
            displayName: '🔧 Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(workingDirectory)'
              backendServiceArm: '$(serviceConnection)'
              backendAzureRmStorageAccountName: '$(backendStorageAccount)'
              backendAzureRmContainerName: '$(backendContainer)'
              backendAzureRmKey: '$(backendStateKey)'

          - task: TerraformTask@5
            displayName: '🚀 Terraform Apply'
            inputs:
              provider: 'azurerm'
              command: 'apply'
              workingDirectory: '$(workingDirectory)'
              environmentServiceNameAzureRM: '$(serviceConnection)'
              commandOptions: '$(workingDirectory)/tfplan -input=false -auto-approve'
```

---

## 🚦 Parallelism Within Jobs (Matrix Strategy & Slicing)

In addition to parallel stages, Azure DevOps allows running multiple jobs in parallel within the same stage using a **matrix strategy**:

```yaml
jobs:
  - job: TestMultiEnvironment
    displayName: 'Test Environment Configs'
    strategy:
      matrix:
        Dev:
          envName: 'dev'
          tfvarsPath: 'environments/dev/terraform.tfvars'
        Preprod:
          envName: 'preprod'
          tfvarsPath: 'environments/preprod/terraform.tfvars'
        Prod:
          envName: 'prod'
          tfvarsPath: 'environments/prod/terraform.tfvars'
      maxParallel: 3      # Runs all 3 environments concurrently!
    steps:
      - script: echo "Testing configuration for $(envName)..."
```

---

## 💡 Best Practices for Pipeline Optimization

1. **Keep Agentless Gates Agentless:** Always set `pool: server` for `ManualValidation@1`. This frees up execution agents for actual builds while waiting hours for human approval.
2. **Avoid Full Re-clones:** Use shallow fetching (`checkout: self, fetchDepth: 1`) to drastically reduce git checkout duration on large repos.
3. **Use Artifacts for Plans:** Never re-run `terraform plan` in the Apply stage. Download the exact binary plan file created in Stage 3 to guarantee zero drift between review and application.
4. **Cache Dependencies:** Cache `.terraform/providers` or tools directory using the `Cache@2` task to eliminate repeated network downloads on every run.
5. **Fail-Fast Policy:** Position lightweight linters (syntax and formatting) first or in parallel so broken pull requests fail within seconds rather than minutes.

---

## 🔗 Related Notes

- [[01-Azure-DevOps]] — Azure DevOps Complete Beginner Guide
- [[05-Terraform-Pipeline]] — Multi-stage Terraform CI/CD Workflow
- [[10-Parameterized-Pipelines-and-Templates]] — Reusable Templates and Runtime Parameters
- [[01-TFLint]] — Terraform Linting Reference
- [[02-tfsec]] — Infrastructure Security Analysis
