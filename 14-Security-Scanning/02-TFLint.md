# TFLint

[TFLint](https://github.com/terraform-linters/tflint) is a Terraform linter focused on finding possible errors (like illegal instance types) and enforcing best practices, beyond what `terraform validate` does.

## Key Features
- Finds provider-specific errors (e.g., invalid Azure VM size).
- Enforces naming conventions.
- Detects unused declarations (variables, locals).

## Installation
```bash
# macOS
brew install tflint

# Windows (Chocolatey)
choco install tflint

# Windows (Scoop)
scoop install tflint

# Windows (winget)
winget install --id TerraformLinters.tflint
```

## Usage

1. **Initialize TFLint (downloads plugins):**
```bash
tflint --init
```

2. **Run TFLint:**
```bash
tflint
```

## Configuration (`.tflint.hcl`)
Create a `.tflint.hcl` file in your repository root to configure rules.

```hcl
plugin "azurerm" {
    enabled = true
    version = "0.27.0"
    source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
}

rule "terraform_naming_convention" {
  enabled = true
  format = "snake_case"
}

rule "terraform_unused_declarations" {
  enabled = true
}
```

## Production Grade (CI/CD Integration)
In CI pipelines, run TFLint to catch cloud-provider specific errors before running `terraform plan`.
```yaml
# GitHub Actions Example
- name: Run TFLint
  uses: terraform-linters/setup-tflint@v3
- run: tflint --init
- run: tflint -f compact
```
