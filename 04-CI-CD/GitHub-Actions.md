---
tags: [github, actions, ci-cd, automation]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# ⚡ GitHub Actions — Complete Guide in Simple Language

---

## 🤔 What is GitHub Actions?

Think of GitHub as a place where you store your code (like a locker). GitHub Actions is like having a **robot assistant sitting right next to that locker**. 

Whenever you do something (like push code, open a pull request, or even on a timer), the robot wakes up and automatically does tasks for you — like testing your code, building it, and deploying it to a server.

> 🧠 **In simple words:** GitHub Actions is a free CI/CD (automation) system built directly inside GitHub. You write instructions in a YAML file, and GitHub's computers run them for you automatically.

**The big advantage over Azure DevOps Pipelines:** GitHub Actions lives *inside* your GitHub repository. There's no separate platform to set up — your code and your pipeline live side by side.

---

## 📁 Where Do Workflows Live?

All GitHub Actions workflows are stored in a special folder in your repository:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── ci.yml          ← Your CI pipeline
│       ├── deploy.yml      ← Your deploy pipeline
│       └── nightly.yml     ← A scheduled job
├── src/
│   └── ... your code ...
```

The `.github/workflows/` folder is where all the magic happens. Every `.yml` file inside it is a separate, independent workflow.

---

## 🔑 Core Concepts Explained Simply

### 1. 📋 Workflow
A **Workflow** is the entire automation recipe — the whole YAML file. It defines:
- **When** to run (triggered by an event)
- **What** to run (jobs and steps)

### 2. ⚡ Events — "What Wakes the Robot Up?"

An **Event** is a trigger — something that happens in GitHub that causes your workflow to start running.

| Event | What it means |
|-------|---------------|
| `push` | Someone pushed (uploaded) code to the repository |
| `pull_request` | Someone opened a Pull Request (a request to merge code) |
| `workflow_dispatch` | Someone manually clicked "Run workflow" in the GitHub UI |
| `schedule` | A timer (like a cron job — "run every night at midnight") |
| `release` | Someone created a new GitHub Release |

```yaml
on:
  push:
    branches: [ "main" ]           # Trigger when code is pushed to main
  pull_request:
    branches: [ "main" ]           # Trigger when a PR targets main
  workflow_dispatch:               # Allow manual runs from the GitHub UI
  schedule:
    - cron: '0 0 * * *'           # Run every night at midnight (UTC)
```

### 3. 💼 Jobs — "Groups of Tasks"

A **Job** is a group of steps that run together on the same machine (runner). 

- By default, **all jobs run in parallel** (at the same time) — like having multiple robots working simultaneously.
- To make jobs run in order (one after the other), use the `needs:` keyword.

```yaml
jobs:
  build:               # Job 1: Build
    runs-on: ubuntu-latest
    steps: ...

  test:                # Job 2: Test — runs AT THE SAME TIME as build by default
    runs-on: ubuntu-latest
    steps: ...

  deploy:              # Job 3: Deploy — waits for BOTH build AND test to finish
    needs: [build, test]
    runs-on: ubuntu-latest
    steps: ...
```

### 4. 🖥️ Runners — "Which Computer Runs My Code?"

A **Runner** is the server/computer that actually executes your workflow steps.

**GitHub-Hosted Runners (easiest, recommended for most use cases):**
- Microsoft manages these — you don't set anything up
- Comes pre-installed with common tools (Node.js, Python, Docker, Azure CLI, etc.)
- A fresh, clean machine is created for EVERY run and thrown away when done

```yaml
runs-on: ubuntu-latest    # A fresh Ubuntu Linux server
runs-on: windows-latest   # A fresh Windows server
runs-on: macos-latest     # A fresh macOS machine
```

**Self-Hosted Runners (for private network access):**
- Your own server (on-premises or Azure VM) that you install the GitHub runner software on
- Use when you need to access private databases, internal APIs, or private AKS clusters
- The runner "phones home" to GitHub asking for jobs

```yaml
runs-on: self-hosted    # Your own server
```

### 5. 📝 Steps — "Individual Tasks"

A **Step** is a single task within a job. It can be:
- A **`run:`** step — a shell command you type (like `npm install`)
- A **`uses:`** step — a pre-built Action from the marketplace

```yaml
steps:
  - name: Install dependencies   # A 'run' step — just a command
    run: npm install

  - name: Checkout code          # A 'uses' step — using a pre-built action
    uses: actions/checkout@v4
```

### 6. 🧩 Actions — "Pre-Built Power Tools"

An **Action** is a reusable, pre-packaged piece of automation. Instead of writing complex scripts, you use someone else's well-tested action.

Think of them like **apps from an app store for automation**.

Popular actions:
| Action | What it does |
|--------|--------------|
| `actions/checkout@v4` | Downloads your code onto the runner |
| `actions/setup-node@v4` | Installs a specific version of Node.js |
| `actions/setup-python@v5` | Installs a specific version of Python |
| `azure/login@v2` | Logs into Azure using OIDC (no passwords!) |
| `docker/build-push-action@v6` | Builds a Docker image and pushes it to a registry |

---

## 💡 A Real Complete Example — Node.js App CI/CD

```yaml
# .github/workflows/ci-cd.yml
# This pipeline: Tests, Builds, and Deploys a Node.js web app to Azure

name: CI/CD Pipeline

# ─── TRIGGERS ───────────────────────────────────────────────────────────────
on:
  push:
    branches: [ "main" ]        # Run when code lands on main
  pull_request:
    branches: [ "main" ]        # Also run to validate PRs before merging

# ─── ENVIRONMENT VARIABLES ──────────────────────────────────────────────────
env:
  NODE_VERSION: '20'            # Use Node.js version 20

# ─── JOBS ───────────────────────────────────────────────────────────────────
jobs:

  # ── JOB 1: Build & Test ───────────────────────────────────────────────────
  build-and-test:
    name: 🔨 Build & Test
    runs-on: ubuntu-latest

    steps:
      # Step 1: Download the code from the repository
      - name: 📥 Checkout Code
        uses: actions/checkout@v4

      # Step 2: Install the correct version of Node.js
      - name: ⚙️ Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'          # Cache npm packages to speed up future runs

      # Step 3: Install all npm dependencies
      - name: 📦 Install Dependencies
        run: npm ci             # 'ci' is like 'install' but faster & stricter for pipelines

      # Step 4: Run tests
      - name: 🧪 Run Tests
        run: npm test

      # Step 5: Build the application
      - name: 🏗️ Build Application
        run: npm run build

      # Step 6: Upload the built files so the deploy job can use them
      - name: 📤 Upload Build Artifact
        uses: actions/upload-artifact@v4
        with:
          name: built-app
          path: ./dist           # The folder with the built files
          retention-days: 1      # Auto-delete after 1 day (we don't need it long)

  # ── JOB 2: Deploy ─────────────────────────────────────────────────────────
  deploy:
    name: 🚀 Deploy to Azure
    runs-on: ubuntu-latest
    needs: build-and-test        # ← Only run AFTER the build-and-test job succeeds
    if: github.ref == 'refs/heads/main'  # ← Only deploy when code is on main (not PRs)

    # Environment protection: if "production" environment is configured with
    # required reviewers in GitHub Settings, this job will PAUSE and wait for approval
    environment: production

    # Permissions needed for OIDC login to Azure (passwordless!)
    permissions:
      id-token: write
      contents: read

    steps:
      # Step 1: Download the built files from the build job
      - name: 📥 Download Build Artifact
        uses: actions/download-artifact@v4
        with:
          name: built-app
          path: ./dist

      # Step 2: Log into Azure using OIDC (NO passwords stored!)
      - name: 🔐 Login to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      # Step 3: Deploy to Azure App Service
      - name: 🌐 Deploy to App Service
        uses: azure/webapps-deploy@v3
        with:
          app-name: 'my-nodejs-app'
          package: './dist'
```

---

## 🔐 Authentication with Azure (OIDC — The Secure Way)

### ❌ The Old Way — Storing Secrets (Avoid!)

In the past, you'd create an Azure Service Principal, generate a "client secret" (a password), and store it in GitHub Secrets. Every time the pipeline runs, it uses that password to log in.

**Problems:**
- The password expires (usually in 1-2 years) and breaks your pipeline
- Rotating (changing) it is manual and error-prone
- If someone steals the secret, they have long-term access to your Azure

### ✅ The Modern Way — OIDC Federated Identity (Passwordless!)

**OIDC (OpenID Connect)** lets GitHub Actions prove its identity to Azure using a short-lived token (valid for ~5 minutes), with **no passwords stored anywhere**.

**How it works:**
1. You set up a *trust relationship* between your GitHub repository and Azure Entra ID
2. When your pipeline runs, GitHub generates a one-time token
3. Azure verifies: "Yes, this token really came from THIS GitHub Actions workflow in THIS repo"
4. Azure grants access — done! No secrets needed.

**Setup steps:**
```
1. In Azure Portal → Microsoft Entra ID → App Registrations → Your App
2. Go to "Certificates & Secrets" → "Federated credentials"
3. Add credential → Choose "GitHub Actions"
4. Fill in: Organization, Repository, Entity (branch/environment)
5. In GitHub → Settings → Secrets → Add these (NOT secrets, just IDs):
   - AZURE_CLIENT_ID  (the App Registration's Application ID)
   - AZURE_TENANT_ID  (your Azure Tenant/Directory ID)
   - AZURE_SUBSCRIPTION_ID
```

```yaml
# In your workflow — this is ALL you need, no password!
permissions:
  id-token: write   # ← This tells GitHub to generate an OIDC token
  contents: read

steps:
  - name: 'Login to Azure'
    uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}       # Not really a secret — just an ID
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}       # Same
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

---

## 🔑 GitHub Secrets & Variables

### Secrets (for sensitive values)
Secrets are **encrypted** and **never shown in logs** (they appear as `***`).

Use for: passwords, API keys, connection strings.

```yaml
# Access a secret in your workflow
- name: Use a secret
  run: echo "The secret is ${{ secrets.MY_SECRET }}"
  # This will print: "The secret is ***" in the logs
```

### Variables (for non-sensitive config)
Variables are stored in plain text — use for non-sensitive configuration values.

```yaml
# Access a variable
- name: Use a variable
  run: echo "Deploying to ${{ vars.ENVIRONMENT_NAME }}"
```

---

## 🛡️ Environments & Protection Rules

A **GitHub Environment** is a deployment target (like `staging` or `production`). You can add **protection rules**:

- **Required reviewers:** The workflow pauses and waits for a specific person to approve before continuing
- **Wait timer:** Forces a X-minute wait before continuing (e.g., a 15-minute window to cancel)
- **Deployment branches:** Only allow deployments from specific branches (e.g., only `main` can deploy to production)

```yaml
jobs:
  deploy-prod:
    environment: production     # ← Links to the "production" environment with protection rules
    steps:
      - ...
```

---

## 🆚 GitHub Actions vs Azure DevOps Pipelines

| Feature | GitHub Actions | Azure DevOps Pipelines |
|---------|---------------|----------------------|
| **Home** | Inside GitHub repository | Separate Azure DevOps service |
| **Best for** | Open source, modern tech | Large enterprises, Microsoft-heavy |
| **Syntax** | `on:`, `jobs:`, `steps:` | `trigger:`, `stages:`, `jobs:`, `steps:` |
| **Marketplace** | Huge (thousands of free actions) | Smaller marketplace |
| **Free tier** | 2,000 minutes/month (private repos) | 1,800 minutes/month |
| **Self-hosted** | Self-hosted runners | Self-hosted agents |
| **Project management** | Basic (GitHub Issues/Projects) | Full Azure Boards |

> 💡 **Bottom line:** If your code is in GitHub, GitHub Actions is the natural choice. The concepts are identical — just different syntax.

---

## ⚠️ Common Mistakes to Avoid

1. **Using `@latest` tag for actions** — Always pin to a specific version (e.g., `actions/checkout@v4`) not `@latest`. Unpinned actions can break when the action author releases a breaking change.

2. **Storing real secrets as plain text in the YAML** — NEVER do `run: az login --password "myRealPassword123"`. Always use `${{ secrets.SECRET_NAME }}`.

3. **Not using OIDC for Azure auth** — If you're using a client secret for Azure login, switch to OIDC. Secrets expire and cause silent failures.

4. **Deploying on every push to every branch** — Add `if: github.ref == 'refs/heads/main'` to deployment jobs so only the main branch triggers deploys.

5. **Skipping `needs:` between jobs** — Without `needs:`, all jobs run in parallel. Your deploy job will start at the same time as your build job and fail because nothing is built yet!

---

## 🎯 Key Takeaway

GitHub Actions is a powerful, free automation platform built directly into GitHub. You write YAML files in `.github/workflows/` to define pipelines that trigger on events (push, PR, schedule). Always use **OIDC federated credentials** instead of storing Azure passwords as secrets — it's safer and requires zero maintenance. Use **Environments** with required reviewers to add human approval gates before production deployments.
