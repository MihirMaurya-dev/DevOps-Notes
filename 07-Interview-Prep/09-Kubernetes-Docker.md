---
tags: [interview, prep, kubernetes, docker, containers, questions]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Kubernetes & Docker Interview Questions

A comprehensive collection of questions from recent interviews covering Docker fundamentals, Kubernetes operations, troubleshooting, and scaling.

---

## Docker Basics

### Q1: What happens internally when you run `docker run`?
**A:** Docker first checks if the image exists locally. If not, it pulls it from the registry (DockerHub/ACR). It then creates a new container layer on top of the image layers, allocates a network namespace and IP, mounts volumes, and finally executes the `ENTRYPOINT`/`CMD` process as PID 1 inside the container.

### Q2: What is the difference between `CMD` and `ENTRYPOINT` in a Dockerfile?
**A:**
- `ENTRYPOINT` defines the fixed executable that always runs. It is not easily overridden (`docker run myimage` runs the entrypoint).
- `CMD` provides default arguments passed to the `ENTRYPOINT`, and can be completely overridden at runtime (`docker run myimage <custom_args>`).
- Best practice: Use `ENTRYPOINT` for the main process, `CMD` for default flags.

```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
```

### Q3: What is a Docker Volume, and why do we use it?
**A:** A volume is a persistent storage mechanism that lives outside the container's writable layer. Since a container's file system is ephemeral (destroyed on removal), volumes ensure data (like DB files or uploaded files) survives container restarts and deletions. Volumes are also shared between containers and are faster than bind mounts for I/O.

### Q4: Where are Docker images stored?
**A:** Images are stored in a Container Registry. Common registries include DockerHub (public), Azure Container Registry (ACR), Amazon ECR, and Google Artifact Registry. Locally, Docker caches pulled images in `/var/lib/docker/`.

---

## Kubernetes Fundamentals

### Q5: Explain the complete request flow from a browser to a Kubernetes pod.
**A:**
1. User's DNS resolves the domain → gets the Load Balancer's IP.
2. Traffic hits the **Cloud Load Balancer** (e.g., Azure LB / AWS ALB).
3. Traffic reaches the **Ingress Controller** (e.g., NGINX) inside the cluster.
4. Ingress matches the host/path rule and forwards to the correct **Service**.
5. The **Service** (ClusterIP) uses iptables/kube-proxy to select a healthy **Pod** endpoint.
6. The **Pod** receives the request on its container port and responds.

### Q6: Difference between Deployment, StatefulSet, DaemonSet, and Job.
**A:**
| Kind | Use Case | Key Feature |
|------|----------|-------------|
| **Deployment** | Stateless apps (web servers, APIs) | Manages replicas; rolling updates |
| **StatefulSet** | Stateful apps (DBs, Kafka) | Stable network IDs, ordered pod startup, persistent volume per pod |
| **DaemonSet** | Node-level agents (Fluentd, Prometheus node-exporter) | Exactly one pod per node |
| **Job / CronJob** | Batch tasks (data migrations, reports) | Runs to completion; terminates on success |

### Q7: What is the difference between stateless and stateful applications in Kubernetes?
**A:** A **stateless** app does not store any session or data on the pod itself. Every pod is identical and replaceable (e.g., a web API). A **stateful** app requires its identity and data to persist (e.g., a MySQL pod must retain its database files). Kubernetes uses `StatefulSet` + `PersistentVolumeClaims (PVC)` for stateful workloads.

### Q8: Readiness Probe vs Liveness Probe.
**A:**
- **Liveness Probe**: "Is the app still alive?" If it fails, Kubernetes **kills and restarts** the pod. Detects deadlocks.
- **Readiness Probe**: "Is the app ready to serve traffic?" If it fails, Kubernetes **removes the pod from the Service endpoints** but does NOT restart it. Prevents traffic during startup or temporary unreadiness.

### Q9: What is Kubernetes Service Discovery? How does it work?
**A:** Kubernetes injects DNS names for every Service into the cluster DNS (CoreDNS). A pod can reach another service using `<service-name>.<namespace>.svc.cluster.local`. Kube-proxy on each node programs iptables rules to forward traffic from the ClusterIP to the healthy pod IP endpoints backing that service.

### Q10: What are ConfigMaps and Secrets? How do you manage them across environments?
**A:**
- **ConfigMap**: Stores non-sensitive config (env vars, config files).
- **Secret**: Stores sensitive data (passwords, tokens) base64-encoded.
- **Cross-environment management**: Use separate namespaces or clusters per environment. Use tools like **External Secrets Operator** to sync secrets from Azure Key Vault into K8s secrets dynamically. Use Helm values files or Kustomize overlays to inject environment-specific configs.

---

## Scaling & High Availability

### Q11: What is HPA (Horizontal Pod Autoscaler)?
**A:** HPA automatically increases or decreases the number of pod **replicas** in a Deployment based on CPU/memory utilization or custom metrics (e.g., request queue length). It queries the Metrics Server and adjusts replica count to maintain the target utilization threshold.

### Q12: What is VPA (Vertical Pod Autoscaler)?
**A:** VPA adjusts the CPU and memory **resource requests/limits** of existing pods based on observed usage. It can recommend, or automatically apply, the right resource sizing. Useful for pods that can't scale horizontally (e.g., single-instance DBs).

### Q13: What is Cluster Autoscaler?
**A:** Cluster Autoscaler automatically adds or removes **worker nodes (VMs)** from the cluster. When pods are `Pending` because no node has enough resources, it provisions a new node. When nodes are underutilized, it safely drains and removes them to reduce cloud costs.

### Q14: How do you set up HPA and VPA?
**A:**
```yaml
# HPA Example
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```
VPA is installed as a separate controller. You create a `VerticalPodAutoscaler` object and set `updateMode: "Auto"` for automatic adjustment.

---

## Troubleshooting

### Q15: Why is a pod stuck in `CrashLoopBackOff`? How do you debug it?
**A:** The container starts but crashes repeatedly. Kubernetes backs off with increasing delays. Debug steps:
1. `kubectl describe pod <name>` → check `Events` section for OOMKilled, failed probes, or image pull errors.
2. `kubectl logs <name> --previous` → check the application's crash output.
3. Common causes: missing env vars, wrong DB connection string, permission errors, insufficient memory limits.

### Q16: Why is a pod stuck in `Pending` state? How do you fix it?
**A:** Debug with `kubectl describe pod <name>` and check Events. Common causes:
- **Insufficient resources**: No node has enough CPU/memory → scale up nodes or reduce resource requests.
- **No matching node**: `nodeSelector` or `affinity` rules can't be satisfied.
- **PVC not bound**: The PersistentVolumeClaim is waiting for a matching PV to be provisioned.
- **Image pull backoff**: Wrong image name, registry auth issue.

### Q17: Kubernetes pods are Running but users receive 503 errors. What will you check?
**A:**
1. Check **Readiness Probes**: `kubectl describe pod` → pod may be Running but not Ready.
2. Check **Service selector**: `kubectl describe svc` → ensure the `selector` labels match the pod labels.
3. Check **Ingress rules**: `kubectl describe ingress` → verify backend service and port.
4. Check **Endpoints**: `kubectl get endpoints <svc-name>` → if empty, no pods are matching the service selector.
5. Check **Pod resource limits**: App may be throttled or OOMKilled after startup.

### Q18: What is `CrashLoopBackOff` vs `OOMKilled` vs `ImagePullBackOff`?
**A:**
- **CrashLoopBackOff**: Application crashes repeatedly; Kubernetes keeps restarting it with delays.
- **OOMKilled**: Container exceeded its memory limit; the kernel killed it. Fix: increase memory limit or fix memory leak.
- **ImagePullBackOff**: Kubernetes cannot pull the container image (wrong name, wrong tag, or missing registry credentials).

### Q19: How do you prevent pod flapping (rapid scaling up/down)?
**A:** Configure `stabilizationWindowSeconds` in the HPA spec to prevent scaling decisions from reacting to short spikes. Also set appropriate `minReplicas` so it doesn't scale down to zero under low load. Use proper resource requests so pods have enough headroom.

---

## Deployment Strategies in K8s

### Q20: What deployment strategies are available in Kubernetes?
**A:**
| Strategy | Description | Downtime |
|----------|-------------|----------|
| **Rolling Update** (default) | Replaces old pods incrementally | Zero |
| **Recreate** | Kills all old pods, then creates new ones | Brief downtime |
| **Blue-Green** | Two identical environments; switch traffic via Ingress/Service | Zero |
| **Canary** | Route small % of traffic to new version (via Ingress weight annotations) | Zero |

### Q21: Explain Blue-Green, Canary, and Rolling Update. Which is most cost-effective?
**A:**
- **Rolling Update**: Replaces pods one by one. **Most cost-effective** — no extra infra needed.
- **Blue-Green**: Two full environments run simultaneously. Safe and instant rollback, but **double the cost** during the transition.
- **Canary**: Small percentage of traffic (e.g., 5%) goes to new version. Gradual, low-risk. Slightly higher cost but much less than Blue-Green.

---

## GitOps & ArgoCD

### Q22: What is GitOps, and how does ArgoCD implement it?
**A:** GitOps uses Git as the single source of truth for infrastructure and application state. ArgoCD is a Kubernetes-native GitOps controller. It continuously watches a Git repository and automatically applies any changes (Helm charts, manifests) to the cluster. If someone manually changes a resource in the cluster, ArgoCD detects the drift and can automatically revert it to match Git.

### Q23: Suppose a Helm chart change impacts all production clusters. What will you do?
**A:**
1. Immediately roll back using `helm rollback <release> <revision>` or via ArgoCD's UI.
2. Revert the bad commit in Git (ArgoCD will auto-sync the revert).
3. Investigate the impact using `kubectl get pods -A` and logs.
4. Fix the chart in a feature branch, test in dev/staging.
5. Re-promote with a controlled canary rollout.

### Q24: What is your experience with Kubernetes (AKS)?
**A:**
- Cluster provisioning using Terraform
- Autoscaling (HPA, cluster autoscaler)
- Ingress controllers (NGINX/App Gateway)
- Networking (CNI, Calico)
- Secrets, ConfigMaps, RBAC
- Monitoring using Prometheus/Grafana and Azure Monitor

---

## Related Notes
- [[08-CI-CD|CI-CD]] - Deployment pipelines to AKS
- [[Security]] — Container image scanning, RBAC in K8s
- [[01-Azure|Azure]] — AKS networking, ACR
