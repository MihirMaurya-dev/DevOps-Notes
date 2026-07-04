---
tags: [gitops, continuous-deployment, flux, argocd]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# 🔄 GitOps Basics — Complete Guide in Simple Language

---

## 🤔 What is GitOps?

Imagine you're running an aquarium. You have a list of fish — the "perfect aquarium manifest" — written in a notebook. The goal is: the actual aquarium should ALWAYS match the notebook. 

If a fish dies (server crashes), you add the same species back (the "reconciler" restores it).  
If someone sneaks in and adds a fish that's not in the notebook, you remove it (drift correction).  
If you want to add a new fish, you **write it in the notebook first** — you never touch the aquarium directly.

**GitOps is exactly this for software infrastructure.** Git is the notebook. Your cluster is the aquarium. The GitOps agent (ArgoCD/Flux) is the keeper who continuously checks that reality matches the notebook.

> 🧠 **In simple words:** GitOps = using Git as the single source of truth for your entire infrastructure and application configuration. Any change to the system is made by changing Git, not by directly touching the system.

---

## ❌ The Problem Before GitOps (CIOps / Push-Based)

The old way of deploying is called **CIOps** (CI-driven Operations). Here's what it looks like:

```
Developer pushes code to Git
         ↓
CI pipeline (Jenkins/GitHub Actions) builds the app
         ↓
CI pipeline authenticates to the production Kubernetes cluster
         ↓
CI pipeline runs: kubectl apply -f deployment.yaml
         ↓
🚨 Problem: The CI system has full admin access to production!
```

**What can go wrong:**
1. **Security risk:** Your CI pipeline holds admin credentials for production. If the CI system is hacked, attackers own your entire production environment.
2. **No drift detection:** After the pipeline runs, if someone manually `kubectl edit`s a deployment to try something out, nobody knows. Reality and Git diverge silently.
3. **No automatic remediation:** If a pod crashes and disappears, nothing automatically puts it back from Git.

---

## ✅ The GitOps Way (Pull-Based)

```
Developer pushes code to Git
         ↓
CI pipeline builds the app → Docker image pushed to ACR
         ↓
CI pipeline ONLY updates the manifests repo in Git
(changes image: old-sha → image: new-sha in deployment.yaml)
         ↓
GitOps Agent (ArgoCD/Flux) inside the cluster
NOTICES the Git change → PULLS it → APPLIES it
         ↓
🎉 CI pipeline NEVER directly touches the cluster!
```

**Why this is better:**
- 🔒 **Security:** Your CI pipeline only has permission to push to a Git repo (not admin on production)
- 🔄 **Drift correction:** If someone manually changes a config, the agent reverts it within minutes
- 📋 **Audit trail:** Every change is a Git commit — you know WHO changed WHAT and WHEN
- 🔁 **Easy rollback:** `git revert` the commit, the agent automatically rolls back the deployment

---

## 📜 The 4 Official GitOps Principles

The **OpenGitOps** working group defines GitOps with exactly 4 principles:

### Principle 1: 📝 Declarative
> "A system managed by GitOps must have its desired state expressed declaratively."

**What "declarative" means:**
- **Declarative = Describe what you want** → "I want 3 replicas of nginx running"
- **Imperative = Describe how to do it** → "Start one nginx. Wait. Start another. Wait. Start a third."

In practice, Kubernetes YAML is declarative:
```yaml
# Declarative: "I want 3 nginx pods"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3          # ← I want 3. Kubernetes figures out HOW to get there.
  selector:
    matchLabels:
      app: nginx
  template:
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
```

Compare to imperative (not GitOps-friendly):
```bash
# Imperative: "Do these specific steps"
kubectl scale deployment nginx --replicas=3  # Step 1
kubectl set image deployment/nginx nginx=nginx:1.25  # Step 2
# Problem: These steps aren't stored. History is lost.
```

### Principle 2: 🔐 Versioned and Immutable
> "The desired state is stored in a way that enforces immutability, versioning, and retains a complete version history."

This means: **Store everything in Git.** Git naturally provides:
- **Immutability:** You can't secretly change the past (every commit is cryptographically hashed)
- **Versioning:** Every change creates a new commit with a timestamp and author
- **History:** `git log` shows you the complete story of your infrastructure

### Principle 3: 🤖 Pulled Automatically
> "Software agents automatically pull the desired state declarations from the source."

The key word is **PULL** — the agent inside the cluster reaches OUT to Git, not the other way around. Git never pushes anything into the cluster.

This is what eliminates the need for the CI system to have cluster credentials.

### Principle 4: 🔄 Continuously Reconciled
> "Software agents continuously observe actual system state and attempt to apply the desired state."

"Continuously" is the key. The agent doesn't just apply once. Every few minutes (configurable), it:
1. Reads the desired state from Git
2. Reads the actual state from the cluster
3. If they differ → applies the difference

This is how **drift is automatically corrected**:
```
Git says:  replicas: 3, image: nginx:1.25
Cluster:   replicas: 2, image: nginx:1.24  (← someone edited manually)

Agent detects the diff → applies → Cluster now: replicas: 3, image: nginx:1.25
```

---

## 🛠️ The Two Main GitOps Tools

### ArgoCD 🦑
- Developed by Intuit, donated to CNCF
- Strong on the **UI** — beautiful visual dashboard showing sync status
- Works per-cluster (one ArgoCD per cluster, or multi-cluster with hub-and-spoke)
- Preferred for teams that want visibility

**ArgoCD Application manifest:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/myorg/k8s-manifests.git  # Watch this Git repo
    targetRevision: HEAD                                   # Track main branch
    path: apps/myapp                                       # Folder within the repo
  
  destination:
    server: https://kubernetes.default.svc               # This cluster
    namespace: production
  
  syncPolicy:
    automated:
      prune: true        # Delete resources removed from Git
      selfHeal: true     # Revert manual changes (drift correction!)
    syncOptions:
    - CreateNamespace=true
```

**ArgoCD will:**
- Watch `github.com/myorg/k8s-manifests` every 3 minutes (or via webhook for instant sync)
- If Git changes → automatically apply changes to the cluster
- If someone manually edits the cluster → automatically revert within 3 minutes

### Flux 🌊
- Developed by Weaveworks (the company that coined the term "GitOps")
- **CLI-first, Git-native** — very tightly integrated with Git
- Supports Helm releases and Kustomize natively
- Preferred for teams that prefer IaC-like management

```bash
# Install Flux and connect to your repo (one command!)
flux bootstrap github \
  --owner=myorg \
  --repository=k8s-manifests \
  --branch=main \
  --path=./clusters/production
```

---

## 🏗️ The Repository Strategy — App Repo vs. Manifests Repo

A key GitOps pattern is separating your **code** from your **manifests**:

```
myapp-code repo              k8s-manifests repo
(Application code)           (Kubernetes YAML configs)
├── src/                     ├── apps/
│   └── main.go              │   ├── myapp/
├── Dockerfile               │   │   ├── deployment.yaml  ← image: acr.io/myapp:abc123
└── .github/workflows/       │   │   ├── service.yaml
    └── ci.yml               │   │   └── ingress.yaml
                             └── infrastructure/
                                 └── ...
```

**Why separate repos?**
- The CI pipeline (in the code repo) only needs to update the manifests repo after building
- Security teams control who can merge changes to the manifests repo
- Different teams can own different parts: app team owns `apps/myapp/`, platform team owns `infrastructure/`
- Rollback is simpler: revert the image tag in the manifests repo

---

## 📊 GitOps vs CIOps Comparison Table

| Aspect | CIOps (Push-Based) | GitOps (Pull-Based) |
|--------|-------------------|---------------------|
| **Deployment trigger** | CI pipeline pushes after build | Agent pulls when Git changes |
| **Cluster credentials** | CI system holds admin creds | CI has NO cluster access |
| **Drift detection** | ❌ No automatic detection | ✅ Detected and corrected every ~3 min |
| **Rollback** | Re-run old pipeline | `git revert` → agent auto-rolls back |
| **Audit trail** | CI system logs | Git commit history |
| **Secret exposure** | High (CI holds cluster creds) | Low (agent inside cluster, no inbound) |
| **Tools** | Jenkins, GitHub Actions (direct kubectl) | ArgoCD, Flux |

---

## 🔄 Complete GitOps Flow — Step by Step

```
1. DEVELOPER writes feature code, pushes to feature branch

2. PULL REQUEST opened to main branch

3. CI PIPELINE runs (tests, security scans, build):
   - Run unit tests
   - Build Docker image
   - Tag image: myacr.io/myapp:abc123def
   - Push image to ACR

4. CI PIPELINE updates the manifests repo:
   - Clone k8s-manifests repo
   - Edit apps/myapp/deployment.yaml:
     - Change: image: myacr.io/myapp:OLD_SHA
     - To:     image: myacr.io/myapp:abc123def
   - Commit and push: "chore: bump myapp to abc123def"

5. ARGOCD/FLUX (inside the cluster) polls Git every 3 minutes
   (or gets notified instantly via webhook)

6. AGENT detects the change in Git:
   - Git desired state:  image: myacr.io/myapp:abc123def
   - Cluster actual state: image: myacr.io/myapp:OLD_SHA
   - Diff detected!

7. AGENT applies the change:
   - kubectl apply the updated deployment
   - Kubernetes performs rolling update

8. AGENT reports: "myapp is now SYNCED ✅"

9. DEVELOPER sees the app is deployed — no direct cluster access needed!
```

---

## 🎯 Key Takeaways

1. **GitOps = Git as Single Source of Truth** — if it's not in Git, it shouldn't exist
2. **Pull > Push** — agents pull from Git; CI pipelines don't push to clusters
3. **4 Principles:** Declarative, Versioned, Pulled Automatically, Continuously Reconciled
4. **Drift correction is automatic** — manual cluster changes are reverted within minutes
5. **ArgoCD** = UI-rich, per-cluster; **Flux** = CLI-native, Git-first
6. **Separate your code repo from your manifests repo** — cleaner ownership and security
7. **Rollback is just `git revert`** — the agent does the rest automatically
