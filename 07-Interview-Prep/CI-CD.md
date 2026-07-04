---
tags: [interview, prep, ci-cd, devops, gitops, pipelines, questions]
source: devopsinsiders/batch-18
created: 2026-06-14
updated: 2026-06-14
---

# CI/CD Interview Questions

A comprehensive collection of interview questions covering Continuous Integration, Continuous Delivery, GitOps, and pipeline engineering for Azure/DevOps roles.

---

## Q1: What is the difference between CI and CD?
**A:**

| Term | Full Name | Purpose | Goal |
|---|---|---|---|
| **CI** | Continuous Integration | Automatically build and test every code commit | Detect integration bugs early; maintain a always-releasable main branch |
| **CD (Delivery)** | Continuous Delivery | Automatically deploy to staging/UAT; production deploy is a manual approval | Release is always *possible* on demand |
| **CD (Deployment)** | Continuous Deployment | Every passing commit is automatically deployed to production — no human gate | Maximum automation; used by high-maturity orgs (Netflix, Amazon) |

**The pipeline flow:**

```
Code Commit
    |
[CI: Build → Unit Tests → Code Quality → Security Scan]
    |
[CD: Deploy to Dev → Integration Tests → Deploy to Staging → E2E Tests]
    |
[Manual Approval Gate] (Continuous Delivery) OR [Auto] (Continuous Deployment)
    |
[Deploy to Production → Smoke Tests → Monitor]
```

> [!note]
> Most enterprise organizations practice **Continuous Delivery**, not Continuous Deployment. A human approval gate before production is a common compliance and risk management requirement.

---

## Q2: What is GitOps and how does ArgoCD implement it?
**A:**

**GitOps** is an operational framework where:
- A **Git repository is the single source of truth** for the desired state of infrastructure and applications.
- Any change to the system is made by opening a Pull Request — Git history becomes the audit log.
- An automated agent continuously **reconciles** the actual cluster state toward the desired state in Git.

**ArgoCD** is a GitOps continuous delivery tool for Kubernetes that implements this model:

```
[Developer PR merged to Git repo]
         |
[ArgoCD detects diff between Git state and cluster state]
         |
[ArgoCD applies manifests (Helm/Kustomize/plain YAML) to cluster]
         |
[ArgoCD reports sync status: Synced / OutOfSync / Degraded]
```

Key ArgoCD concepts:
- **Application**: An ArgoCD CR that links a Git repo path to a Kubernetes namespace/cluster.
- **Sync**: The act of applying the Git state to the cluster.
- **Self-Heal**: If someone manually changes a resource (kubectl edit), ArgoCD reverts it back to the Git state within seconds.
- **App of Apps**: A root Application that manages other Applications, enabling bootstrap of an entire cluster.

```yaml
# ArgoCD Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/my-app-config
    targetRevision: main
    path: k8s/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true      # Delete resources removed from Git
      selfHeal: true   # Revert manual changes
```

> [!tip]
> The key security benefit of GitOps is that **cluster credentials never leave the cluster**. ArgoCD runs inside the cluster and pulls from Git — you don't need to push credentials from a pipeline into kubectl.

---

## Q3: Explain trunk-based development vs GitFlow branching
**A:**

**Trunk-Based Development (TBD):**
- All developers commit directly to a single shared branch (`main` / `trunk`) — or use very short-lived feature branches (< 1 day).
- Enforces small, frequent commits and heavy use of feature flags to hide incomplete features.
- CI pipeline runs on every commit to trunk — keeps the branch always deployable.

**GitFlow:**
- Multiple long-lived branches: `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`.
- Feature branches live for days or weeks before merging to `develop`.
- A `release` branch is cut from `develop`, stabilized, then merged to `main` and tagged.

| Factor | Trunk-Based Development | GitFlow |
|---|---|---|
| **Branch lifetime** | Hours (< 1 day) | Days to weeks |
| **CI complexity** | Simple — one pipeline | Multiple pipelines per branch type |
| **Merge conflicts** | Rare (frequent small merges) | Common (long-lived divergence) |
| **Release cadence** | Continuous, multiple per day | Scheduled/batch releases |
| **Feature flags needed** | Yes | No (branches hide incomplete work) |
| **Best for** | SaaS, cloud-native, high-velocity teams | Versioned software releases, ISV products |

> [!important]
> Modern DevOps (DORA research) strongly favors **Trunk-Based Development** as a key predictor of elite software delivery performance. GitFlow is appropriate for products shipping versioned releases (e.g., open-source libraries, embedded software).

---

## Q4: What are the phases of a robust Terraform pipeline?
**A:** A production Terraform pipeline should validate, plan, and apply in structured stages with appropriate gates:

```yaml
# Azure DevOps Pipeline - Terraform phases
stages:
  - stage: Validate
    jobs:
      - job: Lint
        steps:
          - script: terraform fmt -check -recursive     # Format check
          - script: terraform validate                   # Syntax validation
          - script: tflint --recursive                   # Linting rules
          - script: checkov -d . --framework terraform   # Security scanning (SAST)

  - stage: Plan
    dependsOn: Validate
    jobs:
      - job: TerraformPlan
        steps:
          - script: terraform init -backend-config=...   # Init with remote backend
          - script: terraform plan -out=tfplan.binary    # Create plan artifact
          - script: terraform show -json tfplan.binary > tfplan.json
          - script: conftest test tfplan.json            # Policy as code (OPA)
          - publish: tfplan.binary                       # Save plan artifact

  - stage: ApproveAndApply
    dependsOn: Plan
    jobs:
      - deployment: ApplyProd                            # Deployment job = approval gate
        environment: production                          # Configured with manual approvers
        steps:
          - download: current                            # Download saved plan artifact
          - script: terraform apply tfplan.binary        # Apply EXACT plan reviewed
```

**Why save the plan artifact?** The `terraform apply` in the apply stage runs the *exact* plan that was reviewed — no re-planning. This prevents a TOCTOU (time-of-check vs time-of-use) attack where the environment changes between plan and apply.

> [!important]
> The **plan artifact** is the critical security control in a Terraform pipeline. Always apply the saved plan file, never re-run `terraform plan` in the apply stage.

---

## Q5: How do you manage environment-specific configuration in pipelines?
**A:** There are several standard patterns, often used in combination:

**1. Variable Groups / Library (Azure DevOps):**
Store environment-specific values (non-sensitive) as pipeline variable groups, swapped in per environment.

**2. `.tfvars` files per environment:**
```
terraform/
  environments/
    dev.tfvars
    staging.tfvars
    prod.tfvars
```
The pipeline selects the correct `.tfvars` based on the target environment: `terraform plan -var-file=environments/${ENVIRONMENT}.tfvars`

**3. Kustomize overlays (Kubernetes/GitOps):**
```
k8s/
  base/            # Shared base manifests
  overlays/
    dev/           # Dev-specific patches (replica count, image tag)
    staging/
    prod/
```

**4. Azure Key Vault for secrets:**
All environment-specific secrets are stored in per-environment Key Vaults, fetched dynamically at pipeline runtime — never stored in the repo.

```yaml
# Azure DevOps: Inject Key Vault secrets into pipeline
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'prod-service-connection'
    KeyVaultName: 'kv-prod-myapp'
    SecretsFilter: 'DB-CONNECTION-STRING,API-KEY'
    RunAsPreJob: true
```

> [!tip]
> The golden rule: **Config in files, secrets in Key Vault, environment selection by pipeline parameter**. Never use `if` branches in pipeline code to handle environment differences — use parameterization instead.

---

## Q6: How do you implement shift-left security in CI/CD?
**A:** "Shift-left" means moving security testing **earlier** in the development lifecycle — into the developer's workflow and CI pipeline — rather than only scanning at the end.

**Shift-left security toolchain:**

| Stage | Tool / Practice | What it catches |
|---|---|---|
| IDE / Pre-commit | `git-secrets`, `detect-secrets`, `tfsec` | Secrets in code before commit |
| PR / Code Review | Peer review, branch protection rules | Logic flaws, insecure patterns |
| CI - SAST | `Checkov`, `tfsec`, `Semgrep`, `SonarQube` | Insecure IaC config, code vulnerabilities |
| CI - Dependency Scan | `Trivy`, `Dependabot`, `OWASP Dependency-Check` | Vulnerable library versions (CVEs) |
| CI - Container Scan | `Trivy`, `Microsoft Defender for Containers` | OS/package vulns in Docker images |
| CD - DAST | `OWASP ZAP`, `Burp Suite Enterprise` | Runtime vulnerabilities in deployed app |
| Production | `Microsoft Defender for Cloud`, Sentinel | Active threat detection |

```yaml
# CI Pipeline: Shift-Left Security stages
- stage: SecurityScan
  jobs:
    - job: SAST
      steps:
        - script: checkov -d . --framework terraform --soft-fail
        - script: trivy fs . --exit-code 1 --severity HIGH,CRITICAL
        - script: trivy image myregistry.azurecr.io/myapp:$(Build.BuildId) \
                    --exit-code 1 --severity CRITICAL
```

> [!warning]
> Use `--soft-fail` (or equivalent) judiciously — it allows the pipeline to continue despite findings. In early adoption, use `--soft-fail` with results reported to a dashboard. Switch to `--exit-code 1` (hard fail) once the team has addressed baseline findings.

---

## Q7: What is the difference between Blue/Green and Canary deployments?
**A:**

**Blue/Green Deployment:**
- Two identical production environments exist simultaneously: **Blue** (current live) and **Green** (new version).
- The new version is deployed to **Green** and fully tested.
- Traffic is switched **100% at once** from Blue to Green via a DNS swap or load balancer routing rule change.
- Rollback is instant — just switch traffic back to Blue.

**Canary Deployment:**
- The new version is deployed to a **small subset** of production infrastructure (e.g., 5% of pods, or 5% of traffic).
- Real user traffic is **gradually shifted** to the new version (5% → 25% → 50% → 100%) while metrics are monitored.
- If error rates or latency increase, traffic is automatically rolled back to 0% on the new version.

| Feature | Blue/Green | Canary |
|---|---|---|
| **Traffic shift** | All-at-once (binary switch) | Gradual (percentage-based) |
| **Rollback speed** | Instant | Gradual or instant |
| **Infrastructure cost** | Double (two full environments) | Minimal (small % of infra) |
| **Risk** | Higher (all users hit new version at once) | Lower (limited blast radius) |
| **Use case** | Schema migrations, major version changes | Feature releases with metric validation |

```yaml
# AKS Canary with NGINX Ingress (weight-based routing)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"  # 10% to canary
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-canary-svc
                port:
                  number: 80
```

---

## Q8: How do you handle database migrations in a zero-downtime deployment?
**A:** Database migrations are the hardest part of zero-downtime deployments because schemas and data are shared between old and new code versions. The key principle is **backward-compatible, expand-contract migrations**:

**The Expand-Contract Pattern (3 phases across 3 deployments):**

```
Phase 1 - Expand (Add):
  - Add new column as NULLABLE (old code ignores it, new code writes to it)
  - Deploy new app version (both old and new code work simultaneously)

Phase 2 - Migrate (Backfill):
  - Run a background job to populate the new column for existing rows
  - Once complete, add NOT NULL constraint

Phase 3 - Contract (Remove):
  - Remove the old column (only after verifying new code exclusively uses new column)
  - Deploy cleanup
```

**Tooling:** Use a migration framework that is integrated into the pipeline:
- **Flyway** or **Liquibase** for SQL databases — run migrations as a pipeline step before deploying the application.
- **EF Core Migrations** for .NET applications.

```yaml
# Pipeline: Run DB migration before app deployment
- job: DatabaseMigration
  steps:
    - script: |
        flyway -url=jdbc:sqlserver://$(DB_HOST) \
               -user=$(DB_USER) \
               -password=$(DB_PASSWORD) \
               migrate
      displayName: 'Apply DB Migrations'

- job: DeployApplication
  dependsOn: DatabaseMigration
  steps:
    - script: kubectl set image deployment/my-app app=myregistry/myapp:$(Build.BuildId)
```

> [!warning]
> **Never** deploy application code and breaking schema changes simultaneously. A breaking change (renaming/dropping a column) must be split across multiple deployments with a deprecation period in between.

---

## Q9: What is DORA metrics and why do they matter?
**A:** DORA (DevOps Research and Assessment) metrics are the four key indicators that the DORA research team identified as predictors of software delivery performance and organizational performance.

| Metric | Definition | Elite Performers |
|---|---|---|
| **Deployment Frequency** | How often do you deploy to production? | Multiple times per day |
| **Lead Time for Changes** | Time from code commit to production | Less than 1 hour |
| **Change Failure Rate** | What % of deployments cause a production failure? | 0–15% |
| **Mean Time to Restore (MTTR)** | How long to recover from a production failure? | Less than 1 hour |

**Why they matter:**
- DORA research (State of DevOps Report) consistently shows that **elite performers** outperform low performers by 127x more frequent deployments, 2,604x faster recovery times, and 7x lower change failure rates.
- These metrics quantify the balance between **speed** (Deployment Frequency, Lead Time) and **stability** (Change Failure Rate, MTTR).
- They provide objective, outcome-focused goals for DevOps transformation — moving teams away from vanity metrics (lines of code, story points).

**How to improve them:**
- Deployment Frequency → Trunk-Based Development, feature flags, automated deployment pipelines.
- Lead Time → Reduce batch size, automate CI, eliminate manual handoffs.
- Change Failure Rate → Shift-left testing, automated rollbacks, canary deployments.
- MTTR → Observability (logs/metrics/traces), runbooks, automated alerting.

> [!tip]
> Track DORA metrics in Azure DevOps using the **DORA Metrics extension** or build custom dashboards in **Azure Monitor + Log Analytics** by querying pipeline run data and deployment records.

---

## Q10: How do you implement pipeline as code?
**A:** Pipeline as Code means defining your CI/CD pipeline configuration in a file committed to the same repository as the application source code, rather than configuring it through a UI.

**Benefits:**
- Pipeline changes go through the same **PR review process** as application code.
- The pipeline definition is **versioned** alongside the code — you can check out any commit and know exactly what pipeline ran it.
- **Reusable** — templates and shared library patterns reduce duplication.

**Implementation in Azure DevOps (YAML pipelines):**

```yaml
# azure-pipelines.yml — committed to the repo root
trigger:
  branches:
    include:
      - main
  paths:
    exclude:
      - docs/**
      - '*.md'

parameters:
  - name: environment
    type: string
    default: dev
    values: [dev, staging, prod]

stages:
  - template: pipelines/templates/build-stage.yml       # Reusable template
  - template: pipelines/templates/test-stage.yml
  - template: pipelines/templates/deploy-stage.yml
    parameters:
      environment: ${{ parameters.environment }}
```

**Reusable step template example:**
```yaml
# pipelines/templates/build-stage.yml
stages:
  - stage: Build
    jobs:
      - job: BuildAndPush
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
            inputs:
              command: buildAndPush
              repository: $(ACR_REPO)
              dockerfile: Dockerfile
              tags: |
                $(Build.BuildId)
                latest
```

> [!important]
> Enforce **branch protection rules** so that pipeline YAML changes on `main` require at least one reviewer approval. A malicious or accidental change to the pipeline file is as dangerous as a change to the application code itself.

---

## Q11: What are the key differences between Azure DevOps Pipelines and GitHub Actions?
**A:**

| Feature | Azure DevOps Pipelines | GitHub Actions |
|---|---|---|
| **Trigger source** | Azure Repos, GitHub, Bitbucket | GitHub repositories |
| **Runner** | Microsoft-hosted or self-hosted agents | GitHub-hosted or self-hosted runners |
| **Marketplace** | Azure DevOps Marketplace (Tasks) | GitHub Marketplace (Actions) |
| **Secrets management** | Variable Groups + Azure Key Vault task | GitHub Secrets + OIDC for Azure |
| **Approval gates** | Environments with Approvals and Checks | Environments with Required Reviewers |
| **Pipeline as Code** | YAML (`azure-pipelines.yml`) | YAML (`.github/workflows/*.yml`) |
| **Parallel jobs** | Configurable, paid tiers | Free tier (2,000 min/month), paid tiers |
| **Integration** | Deep Azure DevOps ecosystem (Boards, Artifacts) | Deep GitHub ecosystem (Issues, Packages) |

> [!note]
> For organizations standardized on **Azure DevOps** for project management, Azure Pipelines integrates natively with Boards, Repos, and Artifacts. For open-source or GitHub-native teams, **GitHub Actions** is the natural choice. Both support Workload Identity Federation for secure Azure deployments.

---

## Related Notes
- [[Azure]] — Azure services used in pipelines (Key Vault, ACR, AKS)
- [[Terraform]] — IaC pipeline patterns
- [[Security]] — Shift-left, OIDC, secrets management
- [[AKS]] — Kubernetes deployment strategies
