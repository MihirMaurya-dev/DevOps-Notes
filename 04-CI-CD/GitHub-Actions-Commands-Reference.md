---
category: CI/CD
tags: [github-actions, pipeline, yaml, commands, reference, workflow, syntax, actions, expressions, contexts]
type: reference
status: active
level: beginner-to-intermediate
created: 2026-08-09
updated: 2026-08-09
---

# ⚡ GitHub Actions — Pipeline Commands & Syntax Reference

> Complete reference for every keyword, expression, context, and reusable action used inside GitHub Actions workflow YAML files.

---

## 📖 Before You Read

- You know what GitHub Actions is → [[GitHub-Actions]]
- This note is **not** about GitHub Actions concepts — it is a **hands-on syntax reference** for everything you write inside a `.yml` pipeline file
- For the full Terraform + OIDC flow → [[GitHub-Actions-Terraform-OIDC]]

---

## 🗺️ Anatomy of a Workflow File

```yaml
name:          # Workflow display name
on:            # Trigger events
  push: ...
  pull_request: ...

permissions:   # Token permissions (OIDC, contents, etc.)

env:           # Workflow-level environment variables

jobs:
  job-name:
    name:        # Display name for the job
    runs-on:     # Runner OS
    needs:       # Job dependencies
    if:          # Conditional execution
    environment: # Deployment environment (approval gates)
    permissions: # Job-level permission override
    outputs:     # Values this job exposes to other jobs
    env:         # Job-level environment variables

    steps:
      - name:    # Step display name
        uses:    # Reusable action from marketplace
        with:    # Inputs for the action
        run:     # Shell command(s)
        id:      # Step ID (to reference outputs later)
        if:      # Conditional — run this step only if condition is true
        env:     # Step-level environment variable
        continue-on-error:  # If true, the job continues even if this step fails
```

---

## 🔑 Group 1 — Top-Level Keys

### `name`

```yaml
name: Terraform CI/CD
```

The display name of the workflow — shown in the GitHub Actions tab. No functional effect.

---

### `on` — Trigger Events

Defines **what event causes the workflow to run**.

#### Push trigger

```yaml
on:
  push:
    branches:
      - main
      - 'feature/**'    # Glob pattern — matches feature/anything
    paths:
      - '**.tf'         # Only trigger if a .tf file was changed
```

| Key | What it does |
|-----|-------------|
| `branches` | Only trigger on pushes to these branches |
| `paths` | Only trigger if files matching this pattern were changed |
| `tags` | Trigger on tag pushes (e.g., `v1.*`) |

#### Pull Request trigger

```yaml
on:
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize   # Re-triggered when new commits are pushed to the PR
      - reopened
```

#### Manual trigger

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'dev'
        type: choice
        options: [dev, staging, prod]
```

Adds a "Run workflow" button in the GitHub UI with optional input fields.

#### Scheduled trigger (cron)

```yaml
on:
  schedule:
    - cron: '0 2 * * 1-5'    # Every weekday at 2:00 AM UTC
```

Standard 5-field cron: `minute hour day-of-month month day-of-week`

#### Multiple triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'
```

---

### `permissions`

Controls what the automatically-created `GITHUB_TOKEN` can access.

```yaml
permissions:
  id-token: write     # Required for OIDC login to Azure
  contents: read      # Read the repository code
  pull-requests: write  # Write PR comments
  issues: write
  packages: write     # Push to GitHub Container Registry (GHCR)
```

> ⚠️ Set at workflow level (applies to all jobs) or at job level (overrides for that job only). Always use **least privilege** — only grant what the workflow actually needs.

---

### `env` — Environment Variables

```yaml
# Workflow-level — available to ALL jobs and steps
env:
  TF_VERSION: '1.9.5'
  AZURE_REGION: 'eastus'
  NODE_ENV: 'production'
```

Referenced in steps as `${{ env.TF_VERSION }}` or directly as `$TF_VERSION` in shell.

---

## 💼 Group 2 — Job-Level Keys

### `runs-on` — Runner

```yaml
runs-on: ubuntu-latest      # GitHub-hosted Ubuntu (most common)
runs-on: windows-latest     # GitHub-hosted Windows
runs-on: macos-latest       # GitHub-hosted macOS
runs-on: self-hosted        # Your own server
runs-on: [self-hosted, linux, X64]   # Self-hosted with labels
```

> 💡 `ubuntu-latest` is the standard for Terraform, Azure CLI, and Docker pipelines. It comes pre-installed with most DevOps tools.

---

### `needs` — Job Dependencies

```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    steps: ...

  apply:
    needs: plan           # Runs only AFTER plan completes successfully
    runs-on: ubuntu-latest
    steps: ...

  notify:
    needs: [plan, apply]  # Waits for BOTH jobs
    runs-on: ubuntu-latest
    steps: ...
```

Without `needs`, all jobs run **in parallel**. `needs` serializes them and passes their success status.

---

### `if` — Conditional Execution

```yaml
# Job-level condition — entire job is skipped if false
jobs:
  apply:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

```yaml
# Step-level condition — only this step is skipped
steps:
  - name: Notify on failure
    if: failure()
    run: echo "Something went wrong!"

  - name: Run only on PR
    if: github.event_name == 'pull_request'
    run: echo "This is a PR"
```

**Common condition expressions:**

| Expression | When it's true |
|-----------|---------------|
| `github.ref == 'refs/heads/main'` | Running on the main branch |
| `github.event_name == 'push'` | Triggered by a push event |
| `github.event_name == 'pull_request'` | Triggered by a PR |
| `success()` | All previous steps passed |
| `failure()` | At least one previous step failed |
| `always()` | Always runs, regardless of previous failures |
| `cancelled()` | The workflow was manually cancelled |
| `contains(github.ref, 'feature')` | Branch name contains "feature" |

---

### `environment` — Deployment Environments

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://myapp.com    # Optional — shown as a link in the GitHub UI
```

Links the job to a GitHub Environment. If the environment has **required reviewers** configured, the job pauses here and waits for approval before continuing.

**Effect:**
- Pipeline pauses at this job
- Reviewer gets a notification in GitHub
- After approval → job continues
- After rejection → job fails

---

### `outputs` — Passing Data Between Jobs

```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      plan_exit_code: ${{ steps.tf_plan.outputs.exitcode }}   # Expose step output

    steps:
      - name: Terraform Plan
        id: tf_plan
        run: |
          terraform plan -detailed-exitcode
          echo "exitcode=$?" >> $GITHUB_OUTPUT    # Write output to file

  apply:
    needs: plan
    runs-on: ubuntu-latest
    steps:
      - name: Check plan exit code
        run: echo "Exit code was ${{ needs.plan.outputs.plan_exit_code }}"
```

---

### `strategy` — Matrix Builds

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20]
      fail-fast: false    # Don't cancel all matrix runs if one fails
    runs-on: ${{ matrix.os }}
    steps:
      - run: node --version
```

Runs the job for **every combination** — in this example: 4 runs (2 OS × 2 Node versions).

---

### `timeout-minutes`

```yaml
jobs:
  deploy:
    timeout-minutes: 30    # Fail the job if it runs longer than 30 minutes
```

Prevents runaway pipelines from consuming minutes indefinitely.

---

## 📝 Group 3 — Step-Level Keys

### `uses` — Reusable Actions

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0    # Fetch all history (needed for some tools)
```

Syntax: `owner/repo@version`
- `@v4` — use major version 4 (recommended)
- `@v4.1.0` — pin to exact version (most secure)
- `@main` — use latest from main branch (risky — avoid in production)

---

### `run` — Shell Commands

```yaml
steps:
  - name: Single command
    run: echo "Hello World"

  - name: Multi-line commands
    run: |
      echo "Line 1"
      terraform init
      terraform validate

  - name: Run with specific shell
    shell: pwsh           # PowerShell (for Windows runners)
    run: Write-Host "Hello from PowerShell"
```

**Available shells:**

| Shell | Key |
|-------|-----|
| Bash (default on Linux/macOS) | `bash` |
| PowerShell Core | `pwsh` |
| Windows CMD | `cmd` |
| Python | `python` |

---

### `id` — Step Identifier

```yaml
steps:
  - name: Get timestamp
    id: timestamp
    run: echo "value=$(date +%Y%m%d)" >> $GITHUB_OUTPUT

  - name: Use timestamp
    run: echo "Building version ${{ steps.timestamp.outputs.value }}"
```

`id` lets you reference this step's outputs from later steps in the same job using `${{ steps.<id>.outputs.<key> }}`.

---

### `continue-on-error`

```yaml
steps:
  - name: Security scan
    continue-on-error: true    # Job continues even if this step fails
    run: tfsec .
```

Useful for non-blocking checks (e.g., security scans that should warn but not block).

---

### `working-directory`

```yaml
steps:
  - name: Terraform Init
    working-directory: ./environments/prod
    run: terraform init
```

Changes the working directory for just this step.

---

## 💬 Group 4 — Expressions & Contexts

All expressions are wrapped in `${{ }}`.

### GitHub Context — `github.*`

```yaml
${{ github.ref }}                  # Full ref: refs/heads/main
${{ github.ref_name }}             # Short branch name: main
${{ github.sha }}                  # Full commit SHA
${{ github.actor }}                # Username who triggered the run
${{ github.repository }}           # org/repo-name
${{ github.event_name }}           # push / pull_request / workflow_dispatch
${{ github.run_id }}               # Unique ID for this workflow run
${{ github.run_number }}           # Incrementing run counter (1, 2, 3...)
${{ github.workspace }}            # Path to the checked-out repo on the runner
${{ github.event.pull_request.number }}   # PR number (only on PR events)
```

---

### Secrets Context — `secrets.*`

```yaml
${{ secrets.AZURE_CLIENT_ID }}
${{ secrets.AZURE_TENANT_ID }}
${{ secrets.AZURE_SUBSCRIPTION_ID }}
${{ secrets.GITHUB_TOKEN }}        # Auto-created token — no setup needed
```

> ⚠️ Secret values are **masked in logs** — they appear as `***`. Never `echo` a secret directly into a file that gets uploaded as an artifact.

---

### Variables Context — `vars.*`

```yaml
${{ vars.AZURE_CLIENT_ID }}        # Non-sensitive config values
${{ vars.ENVIRONMENT_NAME }}
```

---

### Environment Variables Context — `env.*`

```yaml
env:
  MY_VAR: hello

steps:
  - run: echo ${{ env.MY_VAR }}    # Accessed via expression
  - run: echo $MY_VAR              # Or directly as shell variable
```

---

### Inputs Context — `inputs.*`

```yaml
# Only available when triggered by workflow_dispatch
on:
  workflow_dispatch:
    inputs:
      target_env:
        required: true

steps:
  - run: echo "Deploying to ${{ inputs.target_env }}"
```

---

### Needs Context — `needs.*`

```yaml
jobs:
  apply:
    needs: plan
    steps:
      - run: echo "${{ needs.plan.outputs.plan_exit_code }}"
      - run: echo "${{ needs.plan.result }}"   # success / failure / cancelled / skipped
```

---

### Steps Context — `steps.*`

```yaml
steps:
  - id: my_step
    run: echo "result=42" >> $GITHUB_OUTPUT

  - run: echo "${{ steps.my_step.outputs.result }}"
      # outputs.result = "42"
      # outcome = success / failure / skipped / cancelled
      # conclusion = success / failure / skipped / cancelled
```

---

## 📁 Group 5 — Special Files Written During a Run

These are special environment files that GitHub Actions reads after each step.

### `$GITHUB_OUTPUT` — Set Step Outputs

```bash
echo "key=value" >> $GITHUB_OUTPUT
echo "version=1.9.5" >> $GITHUB_OUTPUT
```

Referenced later as `${{ steps.<id>.outputs.key }}`.

---

### `$GITHUB_ENV` — Set Environment Variables for Subsequent Steps

```bash
echo "TF_LOG=DEBUG" >> $GITHUB_ENV
echo "MY_VAR=hello" >> $GITHUB_ENV
```

Available to all **subsequent steps** in the same job as `$MY_VAR` or `${{ env.MY_VAR }}`.

---

### `$GITHUB_STEP_SUMMARY` — Write to the Job Summary Page

```bash
echo "## Terraform Plan Results" >> $GITHUB_STEP_SUMMARY
echo "| Resource | Action |" >> $GITHUB_STEP_SUMMARY
echo "|----------|--------|" >> $GITHUB_STEP_SUMMARY
echo "| azurerm_resource_group.main | create |" >> $GITHUB_STEP_SUMMARY
```

Renders as **Markdown on the workflow run summary page** in GitHub UI — great for surfacing plan output.

---

### `$GITHUB_PATH` — Add to PATH

```bash
echo "/custom/tool/bin" >> $GITHUB_PATH
```

Adds a directory to `$PATH` for all subsequent steps.

---

## 🧩 Group 6 — Most-Used Actions Reference

### `actions/checkout@v4`

Downloads the repository code onto the runner.

```yaml
- uses: actions/checkout@v4
  with:
    ref: ${{ github.sha }}     # Checkout a specific commit
    fetch-depth: 0             # Full history (needed for git log, changelog tools)
    token: ${{ secrets.GITHUB_TOKEN }}
```

**Must be the first step in almost every job.**

---

### `actions/upload-artifact@v4`

Saves files from one job so other jobs (or humans) can access them.

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: terraform-plan          # Artifact name
    path: tfplan                  # File or folder to upload
    retention-days: 5             # Auto-delete after N days (default: 90)
    if-no-files-found: error      # error / warn / ignore
```

---

### `actions/download-artifact@v4`

Downloads an artifact uploaded by a previous job.

```yaml
- uses: actions/download-artifact@v4
  with:
    name: terraform-plan          # Must match the upload name
    path: ./downloaded-plan       # Where to put it on the runner (optional)
```

---

### `azure/login@v2`

Authenticates to Azure using OIDC (no passwords).

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

**Requires** `permissions: id-token: write` on the job.
After this step, `az` CLI commands are authenticated automatically.

---

### `hashicorp/setup-terraform@v3`

Installs a specific version of the Terraform CLI onto the runner.

```yaml
- uses: hashicorp/setup-terraform@v3
  with:
    terraform_version: '1.9.5'    # Pin exact version
    terraform_wrapper: true       # Wraps terraform to capture outputs (default: true)
```

> 💡 Set `terraform_wrapper: false` if you need raw exit codes from terraform commands (e.g., for `-detailed-exitcode`).

---

### `actions/setup-node@v4`

Installs Node.js on the runner.

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'          # Cache npm packages between runs
```

---

### `actions/cache@v4`

Caches files between workflow runs to speed up pipelines.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.terraform.d/plugin-cache    # What to cache
    key: ${{ runner.os }}-terraform-${{ hashFiles('**/.terraform.lock.hcl') }}
    restore-keys: |
      ${{ runner.os }}-terraform-
```

---

### `docker/login-action@v3`

Logs into a Docker registry (Docker Hub, GHCR, ACR).

```yaml
# Azure Container Registry
- uses: docker/login-action@v3
  with:
    registry: myacr.azurecr.io
    username: ${{ secrets.ACR_USERNAME }}
    password: ${{ secrets.ACR_PASSWORD }}

# GitHub Container Registry (GHCR)
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

---

### `docker/build-push-action@v6`

Builds and pushes a Docker image.

```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    file: ./Dockerfile
    push: true
    tags: |
      myacr.azurecr.io/myapp:latest
      myacr.azurecr.io/myapp:${{ github.sha }}
```

---

### `github/codeql-action/analyze@v3`

Runs GitHub's CodeQL security scanner.

```yaml
- uses: github/codeql-action/analyze@v3
  with:
    languages: ['javascript', 'python']
```

---

## 🔧 Group 7 — Common `run` Commands Used in Pipelines

### Azure CLI (`az`)

```bash
# Verify Azure login
az account show

# List resource groups
az group list -o table

# Get a resource ID
az group show --name rg-main --query id -o tsv

# Deploy ARM template
az deployment group create \
  --resource-group rg-main \
  --template-file main.bicep

# Get AKS credentials
az aks get-credentials --resource-group rg-aks --name aks-prod
```

---

### Terraform CLI

```bash
terraform init
terraform init -upgrade
terraform fmt -check -recursive
terraform validate
terraform plan -out=tfplan
terraform apply -auto-approve tfplan
terraform destroy -auto-approve
terraform state list
terraform output -json
```

---

### Docker CLI

```bash
docker build -t myapp:${{ github.sha }} .
docker push myacr.azurecr.io/myapp:latest
docker run --rm myapp:latest npm test
```

---

### Git CLI

```bash
git config user.email "ci@github.com"
git config user.name "GitHub Actions"
git checkout -b feature/auto-update
git add .
git commit -m "chore: auto-update generated files"
git push origin feature/auto-update
```

---

### General Shell Utilities (bash)

```bash
# Set exit on error — pipeline fails if any command fails
set -e

# Print each command before running it (useful for debugging)
set -x

# Check if a file exists
if [ -f tfplan ]; then echo "Plan file found"; fi

# Write multi-line string to a file
cat << EOF > config.json
{
  "env": "production"
}
EOF

# Capture command output into a variable
RESOURCE_ID=$(az group show --name rg-main --query id -o tsv)
echo "Resource ID: $RESOURCE_ID"

# Exit with specific code
exit 1
```

---

## 📋 Group 8 — Quick Reference Table

### Top-Level Workflow Keys

| Key | Purpose |
|-----|---------|
| `name` | Workflow display name |
| `on` | Trigger events |
| `permissions` | GITHUB_TOKEN scope |
| `env` | Workflow-wide environment variables |
| `jobs` | The work to execute |

### Job-Level Keys

| Key | Purpose |
|-----|---------|
| `runs-on` | Runner OS / machine |
| `needs` | Job dependency (serialization) |
| `if` | Conditional — skip job if false |
| `environment` | Link to deployment environment (approval gate) |
| `permissions` | Job-specific token permissions |
| `env` | Job-scoped environment variables |
| `outputs` | Expose values to downstream jobs |
| `strategy.matrix` | Run job multiple times with different values |
| `timeout-minutes` | Maximum job runtime |
| `continue-on-error` | Job-level failure tolerance |

### Step-Level Keys

| Key | Purpose |
|-----|---------|
| `name` | Step display name |
| `uses` | Use a reusable action |
| `with` | Inputs for the action |
| `run` | Execute shell command(s) |
| `id` | Step identifier for output reference |
| `if` | Skip this step conditionally |
| `env` | Step-scoped environment variables |
| `working-directory` | Change directory for this step only |
| `continue-on-error` | Step failure does not fail the job |
| `shell` | Override the shell (bash, pwsh, cmd) |

### Contexts

| Context | Access Pattern | Contains |
|---------|---------------|---------|
| `github` | `${{ github.* }}` | Event info, repo, SHA, actor |
| `secrets` | `${{ secrets.* }}` | Encrypted secret values |
| `vars` | `${{ vars.* }}` | Plain-text config variables |
| `env` | `${{ env.* }}` | Environment variables |
| `inputs` | `${{ inputs.* }}` | workflow_dispatch inputs |
| `needs` | `${{ needs.<job>.* }}` | Output and result of upstream jobs |
| `steps` | `${{ steps.<id>.* }}` | Output and result of previous steps |
| `runner` | `${{ runner.* }}` | Runner OS, arch, temp directory |
| `job` | `${{ job.status }}` | Current job status |

---

## 🔁 Full Pipeline Pattern — Terraform CI/CD (Reference)

```yaml
name: Terraform CI/CD

on:
  push:
    branches: [main, 'feature/**']
  pull_request:
    branches: [main]

permissions:
  id-token: write
  contents: read
  pull-requests: write

env:
  TF_VERSION: '1.9.5'

jobs:

  plan:
    name: Terraform Plan
    runs-on: ubuntu-latest

    outputs:
      plan_exit_code: ${{ steps.plan.outputs.exitcode }}

    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
          terraform_wrapper: false

      - run: terraform fmt -check -recursive

      - run: terraform init

      - run: terraform validate

      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -out=tfplan -detailed-exitcode
          echo "exitcode=$?" >> $GITHUB_OUTPUT

      - name: Write Plan Summary
        if: always()
        run: |
          echo "## Terraform Plan" >> $GITHUB_STEP_SUMMARY
          terraform show -no-color tfplan >> $GITHUB_STEP_SUMMARY

      - uses: actions/upload-artifact@v4
        with:
          name: terraform-plan
          path: tfplan
          retention-days: 5

  apply:
    name: Terraform Apply
    runs-on: ubuntu-latest
    needs: plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: production

    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}

      - run: terraform init

      - uses: actions/download-artifact@v4
        with:
          name: terraform-plan

      - run: terraform apply -auto-approve tfplan
```

---

## 🎤 Interview Answers

**Q: How do you pass data between two jobs in GitHub Actions?**
> *"Using job `outputs`. In the first job, you write a key-value pair to `$GITHUB_OUTPUT` from a step and declare it as a job output. In the second job (which has `needs: first-job`), you access it via `${{ needs.first-job.outputs.key }}`. Artifacts are used for passing files — outputs are for passing scalar values like IDs or exit codes."*

**Q: What does `permissions: id-token: write` do?**
> *"It grants the workflow permission to request an OIDC token from GitHub's identity provider. This token is then exchanged with Azure for a short-lived access token, enabling passwordless authentication. Without `id-token: write`, the `azure/login@v2` action cannot generate the OIDC token and the login will fail."*

**Q: What is the difference between `secrets.*` and `vars.*`?**
> *"Secrets are encrypted at rest and masked in logs — they appear as `***` if printed. They are used for sensitive values like passwords or API keys. Variables are stored in plain text and visible in logs — they are used for non-sensitive configuration like environment names, region codes, or version numbers."*

**Q: How do you make a job run only when merging to main and not on PRs?**
> *"Add an `if` condition to the job: `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`. This ensures the job only executes when there is a direct push to main — which happens when a PR is merged — and not when the workflow is triggered by a pull_request event."*

---

## 🔗 Related Notes

- [[GitHub-Actions]] — GitHub Actions concepts and fundamentals
- [[GitHub-Actions-Terraform-OIDC]] — Full 14-step Terraform + OIDC flow
- [[Terraform-Pipeline]] — Equivalent pipeline using Azure DevOps
- [[16-Commands-Reference]] — Terraform CLI commands used inside pipeline `run` steps
- [[14-Security-Scanning/03-Tfsec]] — Adding tfsec to pipeline
- [[14-Security-Scanning/04-Checkov]] — Adding Checkov to pipeline
