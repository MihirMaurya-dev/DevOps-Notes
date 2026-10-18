---
tags: [ado, azure-devops, pipelines, boards]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🚀 Azure DevOps (ADO) — The Beginner's Complete Guide

---

## 📖 Before You Read

Before diving in, it helps to understand these concepts:
- What **Git** is — a version control system (a tool that tracks changes to code files, like "track changes" in Microsoft Word, but much more powerful)
- What a **repository (repo)** is — a folder of code files tracked by Git
- What **branches** are in Git — think of them like parallel copies of your code where you can make changes without affecting the main version
- What [[08-Managed-Identity|Managed-Identity]] is (helpful for understanding service connections)

If you're completely new to Git, spend an hour on a Git basics tutorial first — it'll make CI/CD make much more sense!

---

## 🤔 What is Azure DevOps? — Plain English + Real-World Analogy

Imagine a **car manufacturing factory**:
- The **design team** plans what features the car should have and tracks progress
- The **assembly line** automatically builds the car when designs are finalized
- The **quality control** team tests every car before it leaves the factory
- The **shipping department** delivers the finished car to the dealership

Making software follows a very similar process:
- **Plan** what features to build and track who's doing what
- **Write code** and store it in a shared repository
- **Automatically build and test** the code every time a developer makes a change
- **Deploy** (ship) the working software to servers where users can use it

**Azure DevOps** (often called **ADO** for short) is Microsoft's all-in-one platform that supports this entire software factory. It gives your team all the tools they need — from planning to shipping — in one place.

> 🧠 **In simple words:** Azure DevOps is a suite (a collection) of tools by Microsoft that helps teams plan, build, test, and deploy software together. It's like a complete factory floor for software development.

---

## 🧠 Why Do We Need It? — The Problem It Solves

Without a tool like Azure DevOps, software teams face real problems:

- 😓 **No visibility:** Managers don't know what developers are working on or if they're on schedule
- 😓 **Manual testing:** Developers forget to run tests. Bugs reach production (the live app users see)
- 😓 **Manual deployment:** Deploying code means someone manually copies files to a server — slow, error-prone, scary
- 😓 **Code conflicts:** Two developers change the same file — chaos ensues
- 😓 **No audit trail:** "Who deployed that broken change at 2 AM?" — nobody knows

Azure DevOps solves all of these with automation and structure.

---

## ⚙️ Core Services of Azure DevOps — The Five Tools

Azure DevOps is made up of 5 integrated services. Think of each one as a separate department in your software factory:

---

### 1. 📋 Azure Boards — The Planning Department

🤔 **What is it?**

**Azure Boards** is a digital project management tool — like a smart whiteboard for tracking work. Similar to **Jira** (a popular project management tool used at many companies).

It supports **Agile** methodologies. **Agile** is a popular way of organizing software development — instead of planning everything upfront for a 2-year project, you work in short cycles called **Sprints** (usually 2 weeks each), delivering small pieces of working software frequently.

Key concepts in Azure Boards:
- **Work Items:** Individual pieces of work — bugs to fix, features to build, tasks to complete
- **Kanban Board:** A visual board with columns like "To Do → In Progress → Done" — like sticky notes on a whiteboard
- **Sprint:** A 2-week (or similar) period where the team commits to completing certain work items
- **Backlog:** The full list of all work items, prioritized by importance

🧠 **Why do we need it?**

Without Boards, a developer might say: "I'm working on the login feature." A manager asks: "When will it be done? What else is left?" No one knows. Boards makes all work visible to everyone, making it easy to track progress and priorities.

---

### 2. 📁 Azure Repos — The Code Library

🤔 **What is it?**

**Azure Repos** is a cloud-hosted **Git repository** service. A Git repository (repo) is where your code lives — all the files, all the history, all the changes ever made.

Think of it like **Google Docs for code**: 
- Multiple developers can work on the same codebase simultaneously
- Every change is tracked — you can see WHO changed WHAT and WHEN
- You can go back to any previous version of the code if something breaks
- Unlimited, private repositories — your code is not public unless you choose

🧠 **Why do we need it?**

Without a shared code repository, developers email code files to each other. Someone overwrites someone else's work. You lose track of which version is the "latest." Azure Repos solves this with proper version control.

> 💡 **ADO vs GitHub:** GitHub is also a very popular Git hosting service (also owned by Microsoft now). For personal projects and open source, GitHub is more common. For large enterprise companies (especially those already using Microsoft products), Azure DevOps Repos is often preferred because of its deep integration with the rest of Azure DevOps.

---

### 3. ⚙️ Azure Pipelines — The Automated Assembly Line ⭐ (Most Important!)

🤔 **What is it?**

This is the heart of Azure DevOps. **Azure Pipelines** is an automated **CI/CD** system.

Let's break down **CI/CD**:

- **CI = Continuous Integration:** Every time a developer pushes code changes, the pipeline automatically builds the application and runs tests. "Continuous" means this happens automatically, every single time, not just occasionally. "Integration" means checking that the new code integrates (works together) with existing code.

- **CD = Continuous Deployment (or Continuous Delivery):** After the CI stage passes (tests green, build successful), the pipeline automatically deploys (ships) the code to a server — dev environment, staging environment, production environment, etc.

🧠 **Why do we need it?**

**Without CI/CD:**
```
Developer writes code → Manually runs tests (maybe forgets) → 
Manually builds the app → Manually copies files to server → 
Hopes nothing broke → Users report bugs 😱
```

**With CI/CD (Azure Pipelines):**
```
Developer pushes code → Pipeline automatically:
  1. Builds the application
  2. Runs all tests
  3. Reports pass/fail
  4. Deploys to dev server (if tests pass)
  5. Deploys to staging (after review)
  6. Deploys to production (after approval)
All in minutes, automatically, every time! 🎉
```

Pipelines are defined in a file called **`azure-pipelines.yml`** stored alongside your code. **YAML** (Yet Another Markup Language — pronounced "YAM-ul") is a human-readable format for writing configuration using indentation.

---

### 4. 🧪 Azure Test Plans — The Quality Control Department

🤔 **What is it?**

**Azure Test Plans** is a tool for planning, executing, and tracking software tests. It supports:

- **Planned Testing:** Writing test cases in advance ("When I click the Login button with correct credentials, I should see the dashboard")
- **Exploratory Testing:** A tester freely explores the app looking for unexpected bugs
- **Automated Test Results:** Connecting with automated tests run in the pipeline

🧠 **Why do we need it?**

Without structured test plans, QA (Quality Assurance — the people who test software) testers just click around randomly and hope they find bugs. Test Plans gives structure: every feature has documented test cases, every test run has a recorded result, and nothing ships without passing all tests.

---

### 5. 📦 Azure Artifacts — The Parts Warehouse

🤔 **What is it?**

**Azure Artifacts** is a **package management** service. A "package" in software is a reusable piece of code — like a library or a module — that you can share between projects or teams.

It supports multiple package types:
- **npm** — packages for JavaScript/Node.js development
- **NuGet** — packages for .NET (Microsoft's development framework) development
- **Maven** — packages for Java development
- **Python (PyPI)** — packages for Python development

🧠 **Why do we need it?**

Imagine your company has a custom library for handling payments. 5 different apps all use it. Without Artifacts, you'd email a zip file of the library to each team. When you update it, you email again. Chaos!

With Artifacts, you publish the library as a versioned package. All apps point to Artifacts to download it. When you release version 2.0, teams can update on their own schedule.

---

## 🔑 Azure Pipelines Deep Dive — Key Terminology Explained

Let's get into the most important tool: **Azure Pipelines**. Understanding these terms is critical:

### 📌 Trigger — "When Should the Pipeline Run?"

A **Trigger** tells the pipeline WHEN to automatically start. Think of it like a motion sensor light — it turns on automatically when it detects movement (code being pushed).

Common trigger types:
- **Push Trigger:** Run when code is pushed to a specific branch
- **Pull Request Trigger (PR Trigger):** Run when someone creates a Pull Request (a request to merge code from one branch into another — think of it like a "code review request")
- **Scheduled Trigger:** Run on a schedule (like every night at midnight)

```yaml
# In your azure-pipelines.yml file:

trigger:
  branches:
    include:
      - main          # ← Run the pipeline whenever code is pushed to the 'main' branch
      - develop       # ← Also run when pushed to the 'develop' branch
    exclude:
      - feature/*     # ← DON'T run for feature branches (saves build minutes)

pr:
  branches:
    include:
      - main          # ← Also run when someone opens a Pull Request targeting 'main'
                      # This validates code BEFORE it gets merged, catching bugs early!
```

---

### 🖥️ Pool — "Which Computer Runs the Pipeline?"

A **Pool** specifies the **Agent** (the computer/server) that runs your pipeline. An **Agent** is basically a server with software installed on it that can pick up and execute your pipeline jobs.

There are two types:

#### Microsoft-Hosted Agents
Microsoft provides and manages these servers. You don't set them up — you just use them.

```yaml
pool:
  vmImage: 'ubuntu-latest'   # ← Use Microsoft's Ubuntu Linux server
  # Other options: 'windows-latest', 'macos-latest'
```

✅ Pros: Zero setup, always up to date, free for public repos
❌ Cons: Limited runtime (60 minutes per job on free tier), can't access private networks

#### Self-Hosted Agents
Your own servers (on-premises, in your office, or in Azure) that you install the Azure DevOps agent software on. They "phone home" to Azure DevOps asking for jobs to run.

```yaml
pool:
  name: 'MyCompanyAgentPool'   # ← Use your own servers in this pool
```

✅ Pros: Can access your private network/databases, longer runtime, custom software pre-installed
❌ Cons: You maintain the servers yourself

---

### 🏗️ Stage — "Major Phases of the Pipeline"

A **Stage** is a major phase or logical boundary in your pipeline. Think of stages like different rooms in your factory:

```
Build Stage → Test Stage → Deploy to Dev Stage → Deploy to Prod Stage
```

Stages can be configured to require **manual approval** before running — for example, a production deployment should only happen after a human reviews and approves it.

---

### 💼 Job — "A Unit of Work on One Agent"

A **Job** is a collection of steps that run on ONE agent (server) as a unit. Jobs within the same stage can run in **parallel** (at the same time) if you have multiple agents available — like having multiple assembly lines running simultaneously.

```
Stage: Build
├── Job: Build Windows version   (runs on Windows agent)
└── Job: Build Linux version     (runs on Linux agent, at the same time!)
```

---

### 📝 Step — "The Smallest Building Block"

A **Step** is a single action inside a Job. It can be:
- A **Script:** A command you type (like `npm install` or `dotnet build`)
- A **Task:** A pre-built, packaged action (see below)

---

### 📦 Task — "Pre-Built Actions"

A **Task** is a pre-packaged script that performs a specific action. Microsoft and the community provide hundreds of tasks for common operations. Instead of writing complex scripts yourself, you use a task.

Think of tasks like **LEGO bricks** — pre-made pieces you snap together to build your pipeline.

Common tasks:
- `TerraformTaskV4@4` — runs Terraform commands to manage infrastructure
- `AzureCLI@2` — runs Azure CLI commands
- `Docker@2` — builds and pushes Docker images
- `PublishTestResults@2` — publishes test results to the pipeline

---

## 💡 Real Example — A Complete Azure Pipeline

Here's a real-world pipeline with detailed comments explaining every line:

```yaml
# ============================================================
# azure-pipelines.yml — A complete CI/CD Pipeline
# This file lives in your Git repository root
# ============================================================

# --- TRIGGERS ---
trigger:
  branches:
    include:
      - main          # Run this pipeline when code is pushed to 'main'

# --- GLOBAL VARIABLES ---
variables:
  # Variables are reusable values — define once, use anywhere
  azureServiceConnection: 'my-azure-service-connection'  # Name of your service connection
  resourceGroupName: 'my-production-rg'                  # Azure Resource Group name
  location: 'East US'                                    # Azure region

# ============================================================
# STAGE 1: Build & Test
# ============================================================
stages:
- stage: Build                    # Name of the stage (used in UI and references)
  displayName: '🔨 Build & Test'  # Human-friendly name shown in Azure DevOps UI
  
  jobs:
  - job: BuildJob                 # Name of the job
    displayName: 'Build Application'
    
    pool:
      vmImage: 'ubuntu-latest'    # Use Microsoft's Ubuntu Linux server
    
    steps:
    # STEP 1: Check out (download) the code from the repository
    - checkout: self              # 'self' means the current repository
      displayName: '📥 Checkout Code'
    
    # STEP 2: Install dependencies (all the libraries your app needs)
    - script: npm install         # 'npm install' downloads packages listed in package.json
      displayName: '📦 Install Dependencies'
      workingDirectory: '$(Build.SourcesDirectory)'
      # $(Build.SourcesDirectory) = a built-in variable pointing to where code was downloaded
    
    # STEP 3: Run automated tests
    - script: npm test            # 'npm test' runs your test suite
      displayName: '🧪 Run Tests'
    
    # STEP 4: Build the application
    - script: npm run build       # 'npm run build' creates production-ready files
      displayName: '🏗️ Build App'
    
    # STEP 5: Package the built files and save them as a "build artifact"
    # An artifact here = the output files from building (different from Azure Artifacts service)
    - task: PublishBuildArtifacts@1
      displayName: '📤 Publish Build Artifacts'
      inputs:
        pathToPublish: '$(Build.SourcesDirectory)/dist'  # The folder with built files
        artifactName: 'webapp-build'                      # Name for this artifact package

# ============================================================
# STAGE 2: Deploy to Development Environment
# ============================================================
- stage: DeployDev
  displayName: '🚀 Deploy to Dev'
  dependsOn: Build              # Only start AFTER the Build stage finishes successfully
  condition: succeeded()        # Only run if Build stage SUCCEEDED (don't deploy broken code!)
  
  jobs:
  - deployment: DeployWebApp    # 'deployment' type (special job type for deployments — adds tracking)
    displayName: 'Deploy to Dev App Service'
    environment: 'development'  # Links to an Azure DevOps Environment (for tracking and approvals)
    
    pool:
      vmImage: 'ubuntu-latest'
    
    strategy:
      runOnce:                  # Deploy once (other strategies: rolling, canary)
        deploy:
          steps:
          # Download the build artifact we created in Stage 1
          - download: current
            artifact: 'webapp-build'
            displayName: '📥 Download Build Artifacts'
          
          # Deploy to Azure App Service using a Service Connection (explained below!)
          - task: AzureWebApp@1
            displayName: '🌐 Deploy to Azure App Service'
            inputs:
              azureSubscription: '$(azureServiceConnection)'  # Which Azure subscription to use
              appName: 'my-webapp-dev'                         # Name of the Dev App Service
              package: '$(Pipeline.Workspace)/webapp-build'   # Path to the artifact files

# ============================================================
# STAGE 3: Deploy to Production (with manual approval!)
# ============================================================
- stage: DeployProd
  displayName: '🏭 Deploy to Production'
  dependsOn: DeployDev          # Only start AFTER Dev deployment succeeds
  condition: succeeded()
  
  jobs:
  - deployment: DeployToProd
    displayName: 'Deploy to Production App Service'
    environment: 'production'   # This environment has APPROVAL GATES configured!
    # ☝️ When the pipeline reaches this job, it will PAUSE and wait for a human
    # to go into Azure DevOps and click "Approve" before continuing.
    # This prevents accidental production deployments!
    
    pool:
      vmImage: 'ubuntu-latest'
    
    strategy:
      runOnce:
        deploy:
          steps:
          - download: current
            artifact: 'webapp-build'
          
          - task: AzureWebApp@1
            displayName: '🌐 Deploy to Production App Service'
            inputs:
              azureSubscription: '$(azureServiceConnection)'
              appName: 'my-webapp-prod'     # Production app service (different from dev!)
              package: '$(Pipeline.Workspace)/webapp-build'
```

---

## 🔌 Service Connections — How Azure DevOps Talks to Azure

### The Problem

Azure DevOps (where your pipeline runs) and Azure (where you deploy your resources) are technically two different services. By default, they don't trust each other. 

For your pipeline to deploy resources to Azure (create VMs, deploy apps, etc.), it needs to **authenticate** (prove its identity) and **be authorized** (have permission) to do so.

This is done through a **Service Connection**.

**A Service Connection is like a pre-configured bridge** between Azure DevOps and your Azure Subscription. You set it up once, give it a name (like `my-azure-service-connection`), and then reference it in your pipelines with `azureSubscription: 'my-azure-service-connection'`.

### The Old Way — Service Principal with Secret (❌ Avoid!)

A **Service Principal** is an application identity in **Microsoft Entra ID** (Azure's identity system — like a digital HR department). 

The OLD way to create a service connection:
1. Create a Service Principal in Entra ID
2. Generate a **Client Secret** (a password) for it
3. Store that secret in Azure DevOps
4. The pipeline authenticates using that secret

**Problems:**
- 😓 The secret **expires** (usually after 1-2 years) — when it does, ALL pipelines using it break
- 😓 Someone must remember to rotate (change) the secret before it expires
- 😓 The secret is a long-lived credential — if stolen, it provides access until manually revoked

### The Modern Way — Workload Identity Federation / OIDC (✅ Best Practice!)

**OIDC** stands for **OpenID Connect** — an open, standard protocol (a universally agreed-upon method) for identity verification. **Workload Identity Federation** uses OIDC to allow Azure DevOps to prove its identity to Azure without any stored secrets.

How it works: Azure DevOps and Azure Entra ID establish a **trust relationship**. When the pipeline runs:
1. Azure DevOps generates a **short-lived token** (valid for ~5 minutes, like a one-time pass)
2. The pipeline presents this token to Azure
3. Azure validates it ("Yes, this is a real Azure DevOps pipeline from our trusted organization")
4. Azure returns access — no long-lived secrets involved!

**Benefits:**
- ✅ **No secrets to rotate** — tokens are auto-generated and expire in minutes
- ✅ **More secure** — even if intercepted, expired tokens are worthless
- ✅ **Less maintenance** — no "pipeline broke because service principal secret expired" incidents

```
# How to create a Service Connection with Workload Identity Federation:
# 1. In Azure DevOps, go to Project Settings → Service Connections
# 2. Click "New Service Connection" → Select "Azure Resource Manager"
# 3. Select "Workload Identity Federation (automatic)"
# 4. Select your Azure Subscription and Resource Group
# 5. Give it a name (e.g., "my-azure-service-connection")
# 6. Azure DevOps automatically configures the OIDC trust relationship!
```

---

## 🌍 Azure DevOps vs GitHub Actions — Which to Use?

| Aspect | Azure DevOps (ADO) | GitHub Actions |
|--------|-------------------|----------------|
| **Best for** | Large enterprises, Microsoft-heavy shops | Open source, modern tech companies |
| **Integration** | Deep Azure integration | Works with any cloud |
| **Project management** | Built-in Boards | Basic (needs external tools) |
| **Popularity trend** | Established, enterprise-dominant | Growing rapidly |
| **Free tier** | 5 users free, limited build minutes | Free for public repos, limited for private |
| **Learning curve** | Moderate | Slightly easier |

> 💡 **The honest answer:** Both are excellent. If you're working at a large enterprise that already uses Azure DevOps — learn ADO. If you're starting fresh or working on open source — GitHub Actions is gaining momentum fast. The CI/CD concepts (triggers, stages, jobs, steps) are the same in both!

---

## ⚠️ Common Mistakes Beginners Make

1. **Using Service Principal secrets for Service Connections** — Always use Workload Identity Federation (OIDC) instead. Secrets expire and cause surprise outages.

2. **Putting ALL steps in one job** — When one thing fails, the whole job fails. Structure your pipeline with separate jobs for build, test, and deploy so you can clearly see what failed.

3. **Not using approval gates for production** — Never let code deploy to production automatically without a human review. Configure an approval gate on your production environment.

4. **Hardcoding values instead of using variables** — If you hardcode resource names, connection strings, etc. in the pipeline YAML, changing them requires editing many places. Use pipeline variables or variable groups.

5. **Not testing the pipeline on a non-main branch first** — Test your pipeline changes on a feature branch first. A broken pipeline on main can block your entire team.

6. **Ignoring build artifacts** — Not properly publishing build artifacts means later stages can't find the built files. Always use `PublishBuildArtifacts` and `DownloadBuildArtifacts` tasks to pass files between stages.

---

## 🎯 Key Takeaway

**Azure DevOps** is a complete platform that handles the entire software delivery lifecycle — planning (Boards), code storage (Repos), automated build/test/deploy (Pipelines), testing (Test Plans), and package management (Artifacts). The most critical piece is **Azure Pipelines**, which automates your CI/CD process using YAML-defined pipelines. Always use **Workload Identity Federation (OIDC) Service Connections** instead of Service Principals with secrets — it's more secure and requires zero maintenance.

---

## ❓ Beginner FAQ

**Q1: What's the difference between CI and CD?**
> **CI (Continuous Integration)** is the "build and test" phase — every code push automatically triggers a build and test run to catch bugs early. **CD (Continuous Deployment/Delivery)** is the "ship it" phase — after CI passes, the tested code is automatically (or semi-automatically) deployed to servers. CI catches bugs; CD ships working code fast.

**Q2: What's a YAML file and why does it matter?**
> YAML (Yet Another Markup Language) is a file format for writing configuration. In Azure Pipelines, your entire pipeline is defined in a `azure-pipelines.yml` file sitting next to your code in the repository. This is called "Pipeline as Code" — instead of clicking around in a UI to set up your pipeline, you write it as code. The big benefit: it's version-controlled (tracked in Git), reviewable (other developers can review changes), and reproducible (you can recreate the exact same pipeline from the file).

**Q3: How do I safely store passwords and secrets in my pipeline?**
> Never put secrets directly in your YAML file! Use one of these options: (1) **Pipeline Variables** — go to your pipeline's settings and add secret variables (they're masked in logs), (2) **Variable Groups** — shared variables across multiple pipelines, linked to Azure Key Vault for extra security, (3) **[[Key-Vault]] integration** — link your Azure Key Vault directly to Azure DevOps to pull secrets at runtime.

**Q4: What's the difference between Azure DevOps and GitHub?**
> Both are made by Microsoft (Microsoft acquired GitHub in 2018), but they're separate products. GitHub is primarily a code hosting platform with Actions for CI/CD, popular in open source communities. Azure DevOps is a full ALM (Application Lifecycle Management) suite with integrated Boards, Repos, Pipelines, Test Plans, and Artifacts — more commonly used in enterprise Microsoft environments. Many companies use both (GitHub for code, Azure DevOps Pipelines for CI/CD).

**Q5: Can Azure Pipelines deploy to things other than Azure?**
> Absolutely! Azure Pipelines works with ANY cloud (AWS, Google Cloud, DigitalOcean) or on-premises servers. It can run any command, so if you can deploy something from a command line, Azure Pipelines can do it. Despite "Azure" in the name, it's cloud-agnostic. It's especially convenient for Azure deployments because of built-in tasks and service connections, but it's not limited to Azure.
