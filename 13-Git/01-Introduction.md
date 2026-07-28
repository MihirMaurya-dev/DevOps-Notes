---
tags: [git, github, gitlab, azure-repos, bitbucket, version-control]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Introduction to Git & Platform Comparison

## 1. Intro: What is Git vs What is a Git Hosting Platform
**Git** is a distributed version control system (VCS). It runs locally on your machine and tracks changes to files over time, allowing multiple people to collaborate on a single project without overwriting each other's work.

A **Git Hosting Platform** (like GitHub, GitLab, Azure Repos, or Bitbucket) is a web-based service that hosts Git repositories in the cloud. It provides a central location for teams to push their code, manage pull requests (PRs), run CI/CD pipelines, and track issues.

## 2. Core Concepts: Version Control Fundamentals
- **Repository (Repo):** A folder where your project files and their version history are stored.
- **Commit:** A snapshot of your repository at a specific point in time. It records the changes made to the files.
- **Branch:** A parallel version of a repository. It allows you to work on new features or bug fixes without affecting the main codebase.
- **Merge:** The process of combining changes from one branch into another (e.g., merging a feature branch into the `main` branch).
- **History:** The complete log of all commits made to the repository, allowing you to track who made what changes and when.

## 3. Platform Comparison Table
| Feature | GitHub | GitLab | Azure Repos | Bitbucket |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Open Source, Enterprise | All-in-one DevOps, CI/CD | Enterprise, Azure Ecosystem | Atlassian Ecosystem (Jira) |
| **CI/CD Integration** | GitHub Actions (Excellent) | GitLab CI/CD (Excellent) | Azure Pipelines (Excellent) | Bitbucket Pipelines (Good) |
| **Pricing** | Free for public/private, Paid Pro/Team/Enterprise | Free tier, Paid Premium/Ultimate | Free for up to 5 users, Paid Basic/Test Plans | Free for up to 5 users, Paid Standard/Premium |
| **Access Control** | Roles, Teams, Branch Protection | Roles, Branch Protection, Protected Environments | RBAC, Azure Entra ID, Branch Policies | Roles, Branch Permissions |
| **Enterprise Features** | GitHub Advanced Security | Security Scanning, Compliance | Azure Boards, Test Plans | Jira/Confluence deep integration |
| **When to use?** | Open source projects, General purpose | Self-hosted CI, Unified DevOps | Azure-heavy shops, Enterprise | Teams heavily using Jira/Confluence |

## 4. How Azure DevOps / GitHub Connect to Terraform Pipelines
When writing Infrastructure as Code (IaC) with Terraform, your Git platform acts as the source of truth.
1. **Source Code:** You store your `.tf` files in GitHub or Azure Repos.
2. **Trigger:** When you push a commit or open a Pull Request, the platform triggers a CI/CD pipeline (GitHub Actions or Azure Pipelines).
3. **Execution:** The pipeline runs `terraform init`, `terraform plan`, and `terraform apply`.
4. **Authentication:** The pipeline uses service principals or managed identities to securely connect to the cloud provider (e.g., Azure) to provision resources.

## 5. Git Internals Simplified
Under the hood, Git uses a simple object database stored in the `.git` directory:
- **Blob:** Represents the content of a file.
- **Tree:** Represents a directory structure, mapping names to blobs or other trees.
- **Commit:** Points to a specific tree (a snapshot) and contains metadata (author, timestamp, parent commit).
- **HEAD:** A pointer to the current commit or branch you are working on.
- **Refs:** References (like branch names or tags) that point to specific commits.

## 6. Real-World Usage
In a DevOps environment, Git is not just for application code; it is used for infrastructure code (Terraform), configuration management (Ansible), and pipeline definitions (YAML). Everything is version-controlled.

## 7. CI/CD Integration
Git hosting platforms tightly integrate with CI/CD tools. For example, a push to the `main` branch in Azure Repos can automatically trigger an Azure DevOps pipeline to deploy your Terraform infrastructure.

## 8. Best Practices
- Commit often, but ensure each commit represents a logical unit of work.
- Write clear and descriptive commit messages.
- Always use branches for new features or bug fixes; never commit directly to `main`.
- Use `.gitignore` to prevent tracking sensitive or unnecessary files.

## 9. Interview Q&A
**Q: What is the difference between Git and GitHub?**
A: Git is the underlying version control software installed locally. GitHub is a cloud-based service that hosts Git repositories and provides collaboration tools.

**Q: Explain what HEAD is in Git.**
A: HEAD is a reference that points to the current commit or branch you have checked out in your working directory.
