---
tags: [git, repository, github, azure-repos, gitignore, branches]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Repository Creation & Setup

## 1. Intro: Setting up a Repository
Before you can track changes, you need a repository. You can either initialize a new one locally or create one on a hosting platform and clone it.

## 2. Core Concepts: Init vs Clone
- **`git init`**: Turns an existing local directory into a Git repository. It creates a hidden `.git` folder where Git stores its tracking data.
- **`git clone <url>`**: Downloads an existing repository from a remote server (like GitHub or Azure Repos) to your local machine, setting up the remote connection automatically.

## 3. Hands-on: Creating a Repo (CLI + GUI)

### GitHub (GUI)
1. Log in to GitHub.
2. Click the `+` icon in the top right -> **New repository**.
3. Enter a repository name (e.g., `terraform-azure-infra`).
4. Choose Public or Private.
5. Click **Create repository**.

### Azure Repos (GUI)
1. Go to your Azure DevOps Project.
2. Navigate to **Repos**.
3. Click the repository dropdown at the top -> **New repository**.
4. Select Git, enter a name, and click **Create**.

### Remote Setup (CLI)
If you used `git init` locally, you need to connect it to the remote repository:
```bash
git remote add origin <url-of-remote-repo>
git branch -M main
git push -u origin main
```

## 4. `.gitignore` for DevOps/Terraform Projects
The `.gitignore` file tells Git which files or directories to ignore.

### What to Ignore
- **`.terraform/`**: Local plugins and modules downloaded by Terraform.
- **`*.tfstate` / `*.tfstate.backup`**: State files that contain sensitive resource data and should be stored remotely (e.g., in an Azure Storage Account), not in Git.
- **`*.tfvars`**: Variable files that might contain secrets (like passwords or API keys).
- **`.env`**: Environment variable files.
- **`crash.log`**: Application crash logs.

### Full `.gitignore` Template for Terraform + Azure
```gitignore
# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Exclude all .tfvars files, which are likely to contain sensitive data
*.tfvars
*.tfvars.json

# Ignore override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Include override files you do want to add to version control
!example_override.tf

# Ignore CLI configuration files
.terraformrc
terraform.rc

# Azure specific
.azure/
```

## 5. Branch Protection Rules
Branch protection rules are crucial for maintaining code quality and security on the `main` branch.
- **Require Pull Request (PR):** Prevents direct pushes to the branch. All changes must go through a PR.
- **Require Code Review:** Enforces that at least one (or more) reviewers must approve the PR before merging.
- **Prevent Force Push:** Stops users from overwriting the branch history with `git push --force`.
- **Require Status Checks:** Ensures CI/CD pipelines (like a successful `terraform plan`) pass before merging.

## 6. README.md
A `README.md` is the landing page of your repository. It explains what the project is and how to use it.
**What to include:**
- Project title and description.
- Prerequisites (e.g., Terraform v1.5+, Azure CLI).
- Instructions on how to run/deploy the code.
- Information on repository structure.

## 7. Pre-commit Hooks
Pre-commit hooks are scripts that run automatically before a commit is created. They help catch issues early.
- **`detect-secrets`**: Scans code for accidentally committed passwords or API keys.
- **`tflint`**: A Terraform linter that checks for errors and best practices.
- **`terraform fmt`**: Ensures all Terraform code is formatted consistently.

## 8. Real-World Usage
In enterprise setups, creating repositories is often automated using Terraform itself (e.g., using the GitHub or Azure DevOps Terraform provider) to ensure standardized branch protection and access controls from day one.

## 9. Interview Q&A
**Q: Why shouldn't you commit `.tfstate` files to Git?**
A: `.tfstate` files can contain sensitive information (like passwords or connection strings) in plain text. They should be stored in a secure remote backend (like an Azure Storage Account) with state locking enabled.

**Q: How do you fix a commit if you accidentally committed a secret before pushing?**
A: You can use `git reset --soft HEAD~1` to undo the commit while keeping the files, remove the secret, and commit again. (If pushed, the secret is compromised and must be rotated immediately).
