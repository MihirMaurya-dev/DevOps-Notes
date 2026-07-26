# Terraform Built-in Tools

Terraform provides native commands to format code and perform basic validation before using external tools.

## 1. terraform fmt
`terraform fmt` is used to rewrite Terraform configuration files to a canonical format and style. This ensures consistency across the team.

### Usage:
```bash
# Format files in the current directory
terraform fmt

# Format recursively in subdirectories
terraform fmt -recursive

# Check if files are formatted (used in CI/CD pipelines)
# Returns non-zero exit code if files need formatting
terraform fmt -check
```

## 2. terraform validate
`terraform validate` checks whether the configuration is syntactically valid and internally consistent, regardless of any provided variables or existing state.

### Usage:
```bash
# Initialize first (validate requires init to download providers/modules)
terraform init -backend=false

# Run validation
terraform validate
```

### CI/CD Best Practice:
Always run `terraform fmt -check` and `terraform validate` as the first steps in your CI/CD pipeline (e.g., GitHub Actions, Azure DevOps). If these fail, the pipeline should fail immediately.
