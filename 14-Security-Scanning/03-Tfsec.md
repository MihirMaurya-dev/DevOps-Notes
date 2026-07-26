# tfsec

[tfsec](https://github.com/aquasecurity/tfsec) is a static analysis security scanner for Terraform code. It identifies potential security misconfigurations based on best practices (e.g., CIS benchmarks).

> **Note:** tfsec has been integrated into **Trivy** (`trivy config`), but is still widely used as a standalone tool. Both are valid options.

---

## How It Works

tfsec parses your `.tf` files **without running `terraform init`** — it is a pure static analysis tool. It checks for known bad patterns like open ports, missing encryption, and disabled logging against a built-in ruleset.

```
Your .tf files → tfsec parser → Rule evaluation → Findings report
                 (no credentials needed, offline scan)
```

---

## Installation

```bash
# macOS
brew install tfsec

# Windows (Chocolatey)
choco install tfsec

# Linux / CI (binary)
curl -L "$(curl -s https://api.github.com/repos/aquasecurity/tfsec/releases/latest \
  | grep -o 'https://github.com[^"]*tfsec-linux-amd64')" -o tfsec
chmod +x tfsec && sudo mv tfsec /usr/local/bin/
```

---

## Usage

```bash
# Scan current directory
tfsec .

# Scan with verbose output (shows full context)
tfsec . --verbose

# Output in JSON format (for CI integration)
tfsec . --format json --out results.json

# Output in SARIF format (for GitHub Code Scanning)
tfsec . --format sarif --out results.sarif

# Fail only on HIGH and CRITICAL severity
tfsec . --minimum-severity HIGH
```

---

## Common Findings (Azure Examples)

| Rule ID | Finding | What To Fix |
|---------|---------|-------------|
| `azure-storage-no-public-access` | Storage account allows public blob access | Set `allow_nested_items_to_be_public = false` |
| `azure-network-no-public-ingress` | NSG allows inbound from `0.0.0.0/0` on all ports | Restrict source to specific IP or service tag |
| `azure-keyvault-ensure-secret-expiry` | Key Vault secret has no expiry date | Add `expiration_date` to `azurerm_key_vault_secret` |
| `azure-database-enable-audit` | Azure SQL auditing disabled | Set `extended_auditing_policy` on SQL server |

---

## Handling False Positives (Ignores)

If tfsec flags something you've consciously accepted, ignore it with a comment **above** the resource:

```hcl
# tfsec:ignore:azure-network-no-public-ingress
resource "azurerm_network_security_rule" "allow_http_from_agw" {
  name                       = "allow-http-inbound"
  direction                  = "Inbound"
  access                     = "Allow"
  protocol                   = "Tcp"
  source_address_prefix      = "10.0.1.0/24"   # App Gateway subnet only
  destination_port_range     = "443"
  # ...
}
```

---

## Production Grade (CI/CD Integration)

### GitHub Actions
```yaml
- name: Run tfsec
  uses: aquasecurity/tfsec-action@v1.0.0
  with:
    minimum_severity: HIGH          # Only fail on HIGH and CRITICAL
    format: sarif
    soft_fail: false                # Fail the pipeline if issues found
```

### Azure DevOps
```yaml
- script: |
    tfsec . --minimum-severity HIGH --format json --out tfsec-report.json
    cat tfsec-report.json
  displayName: 'Run tfsec Security Scan'
  failOnStderr: false

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: tfsec-report.json
    artifactName: tfsec-results
```

> **Pipeline Best Practice:** Run tfsec **before** `terraform plan`. If tfsec finds CRITICAL issues, there is no point running a plan on broken infrastructure code.
