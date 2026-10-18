---
tags: [aks, kubernetes, deployment, helm, acr]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# ☸️ Deploying to Azure Kubernetes Service (AKS) — Complete Guide

---

## 🤔 The Big Picture: What Happens When You Deploy to AKS?

Think of deploying to AKS like sending a package through a secure delivery company:
1. You **build the package** (your app → a Docker container image)
2. You **store it in a warehouse** (push the image to Azure Container Registry — ACR)
3. **AKS picks it up from the warehouse** and runs it inside the cluster

The pipeline automates all 3 steps so you just push code and the rest happens automatically.

```
Developer pushes code to Git
          ↓
CI Pipeline: Build & Test app → Build Docker Image → Push to ACR
          ↓
CD Pipeline: Tell Kubernetes "use the new image"
          ↓
AKS pulls the new image from ACR & updates pods (zero downtime rolling update)
          ↓
Users see the new version ✅
```

---

## 🏗️ Step 1: Azure Container Registry (ACR) — The Image Warehouse

Before deploying to AKS, your Docker image must live somewhere AKS can pull it from. **Azure Container Registry (ACR)** is Microsoft's private Docker image registry — like a private Docker Hub that lives inside your Azure subscription.

### Why ACR over Docker Hub?
- **Private** — Your images are not public
- **In Azure** — Pulling images from ACR to AKS is fast (same network) and costs no egress fees
- **RBAC integrated** — Use Azure managed identities (no passwords!) for pull access
- **Geo-replication** — Replicate images to multiple Azure regions for multi-region clusters

### Authentication to ACR — The Right Way

```bash
# ❌ WRONG — Using admin credentials (insecure, stores a long-lived password)
docker login myregistry.azurecr.io -u myregistry -p <admin-password>

# ✅ CORRECT — Using Azure CLI (uses your current Azure identity — OIDC in a pipeline)
az acr login --name myregistry
# This uses your already-authenticated Azure session — no passwords!

# ✅ ALSO CORRECT — Grant AKS's managed identity permission to pull from ACR
# (Do this once with Terraform, then AKS can always pull without login steps)
az aks update -n myAKSCluster -g myRG --attach-acr myACR
```

### Image Tagging Strategy

**Never use `latest` as your Docker image tag in production!**

Why? `latest` doesn't tell you WHICH version is running. If something breaks, you can't trace which code change caused it.

**Use the Git commit SHA (the unique fingerprint of the code):**

```bash
# GitHub Actions environment variables:
IMAGE_TAG = ${{ github.sha }}   # e.g., "a1b2c3d4e5f6..."

# Azure Pipelines:
IMAGE_TAG = $(Build.SourceVersion)  # Same concept

# Build and tag with the SHA:
docker build -t myregistry.azurecr.io/myapp:${IMAGE_TAG} .
docker push myregistry.azurecr.io/myapp:${IMAGE_TAG}
```

This means you can always trace: "We're running commit `a1b2c3d`, which was a PR merged on June 15 by John."

---

## 🔄 Step 2: CI Pipeline — Build & Push the Image

Here's a complete GitHub Actions CI pipeline:

```yaml
# .github/workflows/ci.yml
name: CI — Build & Push Docker Image

on:
  push:
    branches: [ "main" ]

env:
  ACR_NAME: mycompanyacr
  IMAGE_NAME: myapp

jobs:
  build-and-push:
    name: 🔨 Build & Push
    runs-on: ubuntu-latest

    permissions:
      id-token: write    # Required for OIDC Azure login
      contents: read

    steps:
      - name: 📥 Checkout Code
        uses: actions/checkout@v4

      - name: 🔐 Login to Azure (OIDC — no passwords!)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: 🔐 Login to ACR
        run: az acr login --name ${{ env.ACR_NAME }}

      - name: 🏗️ Build & Push Docker Image
        run: |
          IMAGE_TAG=${{ github.sha }}
          FULL_IMAGE=${{ env.ACR_NAME }}.azurecr.io/${{ env.IMAGE_NAME }}:${IMAGE_TAG}

          docker build -t $FULL_IMAGE .
          docker push $FULL_IMAGE

          echo "✅ Image pushed: $FULL_IMAGE"
```

---

## 🚀 Step 3: CD Pipeline — Deploy to AKS

There are two approaches: **Push-based** (traditional) and **Pull-based** (GitOps — recommended).

### Approach A: Push-Based Deployment (kubectl / Helm)

The pipeline connects directly to AKS and pushes the update.

```yaml
# .github/workflows/cd.yml
name: CD — Deploy to AKS

on:
  workflow_run:
    workflows: ["CI — Build & Push Docker Image"]
    types: [completed]

jobs:
  deploy:
    name: 🚀 Deploy to AKS
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    permissions:
      id-token: write
      contents: read

    steps:
      - name: 🔐 Login to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: ⚙️ Get AKS Credentials
        # This downloads the kubectl config so we can talk to the AKS cluster
        run: |
          az aks get-credentials \
            --resource-group myResourceGroup \
            --name myAKSCluster \
            --overwrite-existing

      - name: 🔄 Update Kubernetes Deployment
        run: |
          IMAGE_TAG=${{ github.event.workflow_run.head_sha }}
          FULL_IMAGE=mycompanyacr.azurecr.io/myapp:${IMAGE_TAG}

          # Option 1: Direct kubectl update (quick and simple)
          kubectl set image deployment/myapp-deploy \
            myapp=${FULL_IMAGE} \
            --namespace production

          # Wait for rollout to complete
          kubectl rollout status deployment/myapp-deploy \
            --namespace production \
            --timeout=5m

      # --- OR: Use Helm (for complex apps) ---
      - name: 🎡 Deploy with Helm
        run: |
          IMAGE_TAG=${{ github.event.workflow_run.head_sha }}
          
          helm upgrade --install myapp ./helm/myapp \
            --namespace production \
            --set image.tag=${IMAGE_TAG} \
            --set image.repository=mycompanyacr.azurecr.io/myapp \
            --wait \
            --timeout 5m
```

### Approach B: Pull-Based Deployment (GitOps with ArgoCD — Recommended)

In this model, your pipeline doesn't directly touch AKS. Instead:
1. CI builds the image and pushes it to ACR ✅
2. CI **updates a manifest file in a separate Git repo** with the new image tag ✅
3. ArgoCD (running inside AKS) **notices the Git change** and automatically updates the pods ✅

```
CI Pipeline: Build image → push to ACR
                  ↓
          Update manifests repo:
          (change image tag from old-sha to new-sha)
                  ↓
          ArgoCD in AKS detects the Git change
                  ↓
          ArgoCD pulls new image from ACR → Updates pods
```

**Why GitOps is better:**
- 🔒 The pipeline doesn't need direct access to AKS (more secure)
- 📋 All changes are tracked in Git (full audit trail)
- 🔄 Easy rollback: just `git revert` the tag change

```python
# Example: CI pipeline step to update the manifests repo
- name: 📝 Update Image Tag in Manifests Repo
  run: |
    # Clone the separate manifests repository
    git clone https://github.com/myorg/k8s-manifests.git
    cd k8s-manifests
    
    # Update the image tag in the deployment file
    OLD_TAG=$(cat apps/myapp/deployment.yaml | grep "image:" | awk '{print $2}')
    NEW_TAG="mycompanyacr.azurecr.io/myapp:${{ github.sha }}"
    
    sed -i "s|${OLD_TAG}|${NEW_TAG}|g" apps/myapp/deployment.yaml
    
    # Commit and push the change
    git config user.email "ci@mycompany.com"
    git config user.name "CI Bot"
    git add .
    git commit -m "chore: update myapp image to ${{ github.sha }}"
    git push
    
    # ArgoCD will detect this push and automatically deploy!
```

---

## 🔒 Security: Container Security Context

When pods run in AKS, they run as Linux processes. By default, they might run as `root` (the most powerful user) — this is dangerous!

**Always apply a Security Context to your pods:**

```yaml
# In your Kubernetes Deployment manifest
spec:
  template:
    spec:
      # Pod-level security (applies to all containers in the pod)
      securityContext:
        runAsNonRoot: true        # ← Never run as root user
        runAsUser: 1000           # ← Run as user ID 1000 (a non-privileged user)
        fsGroup: 2000             # ← File system group for mounted volumes

      containers:
      - name: myapp
        image: mycompanyacr.azurecr.io/myapp:latest
        
        # Container-level security
        securityContext:
          allowPrivilegeEscalation: false  # ← Cannot gain more privileges at runtime
          readOnlyRootFilesystem: true     # ← Cannot write to filesystem (prevents file-based attacks)
          capabilities:
            drop:
              - ALL                        # ← Drop ALL Linux capabilities (like network admin, raw sockets)
            add:
              - NET_BIND_SERVICE           # ← Only add back what's needed (e.g., bind to port 80)
```

**Why does this matter?** If your container is compromised (e.g., via a security vulnerability), running as root gives the attacker maximum power. Running as a non-root user with no capabilities limits the "blast radius" of an attack.

---

## 📦 Helm — "Kubernetes Package Manager"

Helm is like `apt` or `npm` but for Kubernetes. Instead of managing dozens of individual YAML files, you define your app as a **Chart** (a template package).

```
my-app/                     ← Helm Chart directory
├── Chart.yaml              ← Chart metadata (name, version, description)
├── values.yaml             ← Default configuration values
└── templates/              ← Kubernetes YAML templates
    ├── deployment.yaml     ← Deployment template
    ├── service.yaml        ← Service template
    └── ingress.yaml        ← Ingress template
```

**values.yaml:**
```yaml
# Default values — override these in your pipeline
image:
  repository: mycompanyacr.azurecr.io/myapp
  tag: latest
  pullPolicy: IfNotPresent

replicaCount: 3

service:
  type: ClusterIP
  port: 80
```

**Deploy or upgrade with Helm:**
```bash
# Install (first time) or Upgrade (subsequent releases)
helm upgrade --install myapp ./my-app \
  --namespace production \
  --create-namespace \
  --set image.tag=a1b2c3d4    # Override the image tag with the current commit SHA
  --wait                       # Wait for all pods to be ready before exiting
  --atomic                     # Rollback automatically if the upgrade fails
```

---

## 🔑 Key Design Decisions for AKS Deployments

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| **Image tagging** | `latest` | Git SHA (`a1b2c3d`) | ✅ Always use Git SHA |
| **ACR auth** | Admin credentials | Managed Identity | ✅ Always use Managed Identity |
| **Deployment method** | kubectl set image | Helm upgrade | ✅ Helm for anything complex |
| **CD approach** | Push-based (pipeline → kubectl) | Pull-based (GitOps/ArgoCD) | ✅ GitOps for production |
| **Security context** | Run as root | Run as non-root | ✅ Always non-root |
| **Cluster type** | Public API server | Private cluster | ✅ Private for production |

---

## 🎯 Key Takeaways

1. **Build once, deploy many times** — The Docker image is the artifact. Build it once in CI, deploy it to dev/staging/prod without rebuilding.
2. **Never use `latest` tag** — Tag images with the Git commit SHA for traceability.
3. **Use Managed Identity for ACR** — No credentials, no expiry, no headaches.
4. **GitOps (Pull-based) is the gold standard** — More secure, fully auditable, easy rollback.
5. **Always set a Security Context** — Run as non-root, drop all capabilities, read-only filesystem.
