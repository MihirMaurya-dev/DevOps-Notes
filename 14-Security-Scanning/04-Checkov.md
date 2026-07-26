# Checkov

[Checkov](https://github.com/bridgecrewio/checkov) is an open-source **policy-as-code** tool by Prisma Cloud (Palo Alto Networks). It scans Terraform, ARM, Bicep, Kubernetes, Dockerfiles, and CloudFormation for security and compliance misconfigurations.

---

## How It Works

Checkov maps your IaC resources to a large built-in library of **checks** (policies). Each check has an ID (e.g., `CKV_AZURE_35`) and tests a specific attribute of a resource.

```
Your .tf files → Checkov parser → Check evaluation → Pass / Fail / Skip report
                 (no cloud credentials, offline static analysis)
```

---

## Installation

```bash
# pip (recommended)
pip install checkov

# With a specific version
pip install checkov==3.2.0

# Docker
docker pull bridgecrew/checkov
docker run --rm -v $(pwd):/tf bridgecrew/checkov -d /tf
```

---

## Usage

```bash
# Scan a Terraform directory
checkov -d .

# Scan only specific checks
checkov -d . --check CKV_AZURE_35,CKV_AZURE_59

# Skip specific checks (suppress known false positives globally)
checkov -d . --skip-check CKV_AZURE_98

# Output formats
checkov -d . --output cli              # Default terminal output
checkov -d . --output json             # JSON for programmatic use
checkov -d . --output junitxml > checkov_report.xml  # CI test report

# Scan only a specific file type
checkov -d . --framework terraform

# Scan Kubernetes manifests
checkov -d ./k8s-manifests --framework kubernetes
```

---

## Common Azure Findings

| Check ID | What It Checks | Resource |
|----------|---------------|----------|
| `CKV_AZURE_35` | Storage Account default action not Deny | `azurerm_storage_account` |
| `CKV_AZURE_59` | Storage Account allows public blob access | `azurerm_storage_account` |
| `CKV_AZURE_13` | App Service HTTPS-only not enforced | `azurerm_app_service` |
| `CKV_AZURE_41` | Key Vault soft delete not enabled | `azurerm_key_vault` |
| `CKV_AZURE_109`| Key Vault allows public network access | `azurerm_key_vault` |
| `CKV_AZURE_131`| NSG rule allows unrestricted SSH (port 22) | `azurerm_network_security_rule` |

---

## Handling False Positives (Inline Skip)

Add a `checkov:skip` comment **inside** the resource block with the check ID and a reason:

```hcl
resource "azurerm_storage_account" "tfstate" {
  # checkov:skip=CKV_AZURE_59:Public blob access disabled — this is a private state bucket
  # checkov:skip=CKV_AZURE_35:Network rules set separately via azurerm_storage_account_network_rules

  name                     = "stterraformstate"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  blob_properties {
    delete_retention_policy {
      days = 7
    }
  }
}
```

---

## Custom Policies (YAML)

You can write your own organization-specific policies:

```yaml
# custom-policies/check_cost_center_tag.yaml
metadata:
  name: "Ensure CostCenter tag is present on all Resource Groups"
  id: "CUSTOM_ORG_001"
  category: "CONVENTION"
  severity: "MEDIUM"
definition:
  cond_type: "attribute"
  resource_types:
    - "azurerm_resource_group"
  attribute: "tags.CostCenter"
  operator: "exists"
```

Run with your custom policy directory:
```bash
checkov -d . --external-checks-dir ./custom-policies/
```

---

## Production Grade (CI/CD Integration)

### GitHub Actions
```yaml
- name: Run Checkov IaC Scan
  uses: bridgecrewio/checkov-action@master
  with:
    directory: .
    framework: terraform
    output_format: cli,sarif
    output_file_path: console,results.sarif
    soft_fail: false                 # Fail pipeline on any FAILED check
    skip_check: CKV_AZURE_98        # Global skip for accepted risk

- name: Upload Checkov SARIF to GitHub Security
  uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: results.sarif
```

### Azure DevOps
```yaml
- script: |
    pip install checkov
    checkov -d . \
      --framework terraform \
      --output junitxml \
      --skip-check CKV_AZURE_98 \
      > checkov_report.xml
  displayName: 'Run Checkov'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: JUnit
    testResultsFiles: checkov_report.xml
    testRunTitle: 'Checkov IaC Security Scan'
```

> **Tip:** Upload results as JUnit in Azure DevOps so each Checkov check appears as a **test case** in the pipeline test report — making it very easy to see which specific check failed.

---

## Full Security Scanning Pipeline Order

The recommended order to run all tools in a CI/CD pipeline gate:

```
1. terraform fmt -check     → Code style
2. terraform validate       → Syntax correctness
3. tflint                   → Provider-specific best practices
4. tfsec / trivy config     → Security misconfigurations
5. checkov                  → Compliance (CIS, PCI-DSS, custom policies)
6. gitleaks / trufflehog    → Secrets detection
                ↓
         Only if all pass:
7. terraform plan           → Infrastructure diff
8. terraform apply          → Deploy
```
