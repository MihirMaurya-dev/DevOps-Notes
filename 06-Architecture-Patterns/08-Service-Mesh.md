---
tags: [architecture, patterns, kubernetes, service-mesh]
source: devopsinsiders/batch-18
created: 2026-06-14
updated: 2026-06-14
---

# Architecture Pattern: Service Mesh

As microservices architectures grow on platforms like Azure Kubernetes Service (AKS), managing the communication, security, and observability between hundreds of small services becomes incredibly complex. A Service Mesh solves this by abstracting network communication away from the application code.

## What is a Service Mesh?
A service mesh is a dedicated infrastructure layer that controls service-to-service communication over a network. 

It typically works by injecting a "sidecar" proxy (like Envoy) into every Kubernetes pod. The application container talks only to its local proxy via localhost, and the proxies handle all the complex networking tasks across the cluster. The central control plane manages the configuration of all these proxies.

## Key Capabilities

### 1. Security (mTLS)
- **Mutual TLS (mTLS):** Automatically encrypts all traffic between pods in the cluster, without developers writing any crypto code. 
- It also verifies identity (Pod A is cryptographically proven to be allowed to talk to Pod B), implementing Zero Trust inside the cluster.

### 2. Traffic Management
- **Circuit Breaking:** If Service B is failing, the mesh stops sending traffic to it from Service A immediately, preventing cascading failures across the system.
- **Retries and Timeouts:** The proxy can automatically retry failed HTTP requests a configurable number of times before returning an error to the user.
- **Advanced Routing:** Enables Canary deployments (send 5% of traffic to v2 of a pod) and A/B testing based on HTTP headers (e.g., if header `user-type: beta`, route to the new service).

### 3. Observability
Because all traffic flows through the proxies, the mesh has full visibility into network performance.
- **Distributed Tracing:** Integrates with tools like Jaeger or Zipkin to track a single user request as it hops across 15 different microservices, showing exactly where latency occurs.
- **Metrics:** Automatically generates detailed HTTP metrics (Golden Signals: Latency, Traffic, Errors, Saturation) for dashboards like Grafana.

## Leading Service Mesh Options

1. **Istio:** The most feature-rich and widely adopted. Uses Envoy proxy. Highly customizable but has a steep learning curve and significant resource overhead.
2. **Linkerd:** Focuses on simplicity and low resource usage. Built in Rust (proxy) and Go (control plane). Extremely fast but fewer advanced routing features than Istio.
3. **Open Service Mesh (OSM):** A lightweight mesh built by Microsoft using Envoy. It implements the standard Service Mesh Interface (SMI) APIs.
4. **Cilium:** Uses eBPF (Extended Berkeley Packet Filter) at the Linux kernel level instead of sidecar proxies, making it incredibly high-performance.

## Istio on AKS

Microsoft now provides an **AKS managed Istio add-on**. This is a massive advantage as Microsoft handles the lifecycle, patching, and upgrades of the Istio control plane.

```bash
# Enable the Istio addon on an existing AKS cluster
az aks mesh enable --resource-group myResourceGroup --name myAKSCluster

# Enable sidecar injection for a specific namespace
kubectl label namespace my-namespace istio-injection=enabled
```

## When to Use vs Not Use a Service Mesh

### Use a Service Mesh when:
- You have many microservices written in different languages (avoiding the need to write retry/mTLS libraries in Python, Go, Node, Java).
- You have strict compliance requirements for end-to-end encryption inside the cluster.
- You need advanced canary release routing beyond what basic Kubernetes deployments offer.

### Do NOT use a Service Mesh when:
- You have a simple architecture (e.g., a monolith and a database, or just 2-3 services).
- Your team lacks Kubernetes maturity. A mesh introduces massive complexity; troubleshooting a broken mesh requires deep networking knowledge.
- You are highly resource-constrained (sidecar proxies consume CPU and Memory on every node).
