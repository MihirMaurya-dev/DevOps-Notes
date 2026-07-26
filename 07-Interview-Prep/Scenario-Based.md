---
tags: [interview, prep, scenario, troubleshooting, basics, advanced]
source: devopsinsiders/batch-18
updated: 2026-07-26
---

# Comprehensive DevOps Q&A

This guide contains exactly 26 essential DevOps interview questions, ranging from basic concepts to advanced troubleshooting scenarios.

## Basics

### 1. What is DevOps and what are its core principles?
DevOps is a cultural and technical movement aimed at breaking down silos between development and operations teams. Its core principles include automation, continuous measurement, and sharing of responsibilities. By fostering collaboration, organizations can deliver software faster and more reliably. It heavily relies on practices like CI/CD and Infrastructure as Code.

### 2. Explain Continuous Integration vs Continuous Delivery vs Continuous Deployment.
Continuous Integration (CI) is the practice of frequently merging code changes into a central repository, where automated builds and tests run. Continuous Delivery (CD) extends this by ensuring the code is always in a deployable state, though deployment to production requires manual approval. Continuous Deployment takes it a step further, where every change that passes all stages of the production pipeline is released to customers automatically, with no human intervention. 

### 3. What is Infrastructure as Code (IaC) and why is it important?
Infrastructure as Code (IaC) is the management and provisioning of infrastructure through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. It is crucial because it brings version control, reproducibility, and automation to infrastructure management. This allows teams to spin up environments rapidly and avoid manual configuration drift. Popular tools include Terraform and Ansible.

### 4. What is the difference between Git and GitHub?
Git is a distributed version control system installed locally on a developer's machine to track changes in source code. GitHub, on the other hand, is a cloud-based hosting service that lets you manage Git repositories collaboratively. While Git handles the versioning history locally, GitHub provides the remote server where teams can push their code, review pull requests, and manage projects.

### 5. Explain the concept of Containerization and how it differs from Virtualization.
Containerization packages an application and its dependencies into a single, lightweight executable called a container, which shares the host system's kernel. Virtualization, however, involves running multiple complete operating systems (Virtual Machines) on a single physical server using a hypervisor. Because containers share the OS kernel, they boot much faster and consume far fewer resources than traditional VMs. Docker is the most popular containerization platform.

### 6. What are the common default ports for HTTP, HTTPS, SSH, and RDP?
These are standard network ports essential for configuring firewalls and security groups. HTTP uses port 80 for unencrypted web traffic, while HTTPS uses port 443 for secure, encrypted web communication. For remote administration, SSH operates on port 22 (primarily for Linux systems), and RDP uses port 3389 (primarily for Windows environments). Knowing these defaults is fundamental for network troubleshooting.

## Intermediate

### 7. How does a CI/CD pipeline usually work?
A CI/CD pipeline automates the software delivery process from code commit to production release. It typically starts with a "build" stage where source code is compiled into artifacts. This is followed by a "test" stage running automated unit and integration tests to ensure code quality. Finally, the "deploy" stage pushes the validated artifacts to staging or production environments, often using tools like Jenkins, GitLab CI, or GitHub Actions.

### 8. Explain the difference between `terraform apply` and `terraform plan`.
The `terraform plan` command reads the current state and creates an execution plan, showing you exactly what changes Terraform will make to your infrastructure without actually applying them. It acts as a dry run for safety verification. Conversely, `terraform apply` takes that plan and makes the actual API calls to cloud providers to create, modify, or delete the resources. Always reviewing the plan before applying is a critical best practice.
```bash
terraform plan -out=tfplan
terraform apply "tfplan"
```

### 9. What is a Dockerfile and what are its key instructions?
A Dockerfile is a text document containing all the commands a user could call on the command line to assemble a Docker image. Key instructions include `FROM` to specify the base image, and `RUN` to execute commands during the build process. `COPY` or `ADD` is used to bring local files into the image, while `CMD` or `ENTRYPOINT` defines the default executable that runs when a container starts.
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y nginx
COPY ./index.html /var/www/html/
CMD ["nginx", "-g", "daemon off;"]
```

### 10. Describe the basic architecture of Kubernetes.
Kubernetes architecture consists of a Control Plane (Master) and Worker Nodes. The Control Plane manages the cluster state, featuring components like the API Server (for communication), etcd (key-value store for state), Scheduler (assigns workloads), and Controller Manager (maintains desired state). Worker Nodes run the actual applications and contain the Kubelet (node agent), Kube-Proxy (networking), and a container runtime like containerd.

### 11. How do you handle secrets management in a DevOps pipeline?
Secrets like API keys, database passwords, and certificates should never be hardcoded or committed to source control. Instead, I use a dedicated secrets management tool like HashiCorp Vault, Azure Key Vault, or AWS Secrets Manager. During pipeline execution, tools retrieve these secrets dynamically and inject them as environment variables or temporary files. It is also important to ensure pipeline logs mask any sensitive values that might accidentally be printed.

### 12. What is a Blue-Green deployment strategy?
Blue-Green deployment is a technique that reduces downtime and risk by running two identical production environments called Blue and Green. At any time, only one environment (e.g., Blue) is live and serving all production traffic. The new version of the application is deployed and tested in the idle environment (Green). Once validated, a load balancer or router simply switches traffic to Green, making rollbacks instantaneous if issues occur.

### 13. Explain the purpose of a Load Balancer in web architecture.
A Load Balancer distributes incoming network traffic across a group of backend servers or instances. Its primary purpose is to ensure high availability and reliability by routing requests only to healthy servers. It prevents any single server from becoming a bottleneck, effectively managing capacity and load. Modern load balancers also handle SSL termination and provide advanced routing based on URL paths.

## Advanced

### 14. How would you design a Highly Available (HA) architecture in the cloud?
A Highly Available architecture eliminates single points of failure across the entire stack. I would deploy compute instances across multiple Availability Zones (AZs) behind an Application Load Balancer to ensure localized outages don't bring down the app. The database would be configured in a multi-AZ active-standby setup or a globally distributed NoSQL database. Additionally, I would implement auto-scaling groups to automatically replace unhealthy instances and handle traffic spikes.

### 15. Explain how Kubernetes handles service discovery and internal routing.
Kubernetes uses Services to expose applications running on a set of Pods as a network service. When a Service is created, Kubernetes assigns it a stable internal IP address (ClusterIP) and a DNS name via CoreDNS. Pods can then communicate with each other using these reliable DNS names, even though individual Pod IPs constantly change. The Kube-Proxy component running on each node implements this routing by updating local iptables or IPVS rules.

### 16. Discuss the differences between mutable and immutable infrastructure.
Mutable infrastructure allows servers to be updated and modified in place, meaning patches or configuration changes are applied directly to running servers. This often leads to configuration drift and inconsistent environments. Immutable infrastructure, however, dictates that servers are never modified after they are deployed. If an update is needed, a new image is built and fresh instances are provisioned to replace the old ones, ensuring strict consistency and easier rollbacks.

### 17. How do you implement Zero Downtime Deployments?
Zero downtime deployments ensure an application remains continuously available to users during an upgrade. I implement this using strategies like Blue-Green deployments or Canary releases. In Kubernetes, this is achieved natively using Rolling Updates, where new Pods are spun up and verified via readiness probes before old Pods are terminated. The load balancer continues serving traffic without interruption as the rollout progresses.

### 18. Explain Terraform state management in a team environment.
In a team environment, storing the Terraform state file locally is dangerous and prevents collaboration. The state file must be stored in a remote backend like AWS S3, Azure Blob Storage, or HashiCorp Terraform Cloud. Crucially, state locking must be enabled (e.g., via a DynamoDB table for S3 backends) to prevent multiple engineers or CI/CD pipelines from modifying infrastructure concurrently, which would corrupt the state.

### 19. How do you monitor and observe microservices effectively?
Observability in microservices requires three pillars: metrics, logs, and traces. I use Prometheus for collecting numeric metrics (like CPU usage or request rates) and Grafana for visualizing them. Centralized logging via the ELK stack or Fluentd aggregates logs from all microservices into one searchable location. Finally, distributed tracing with tools like Jaeger or OpenTelemetry is critical for tracking a single request as it jumps across multiple asynchronous services.

## Scenario-Based

### 20. Scenario: The "Cannot Connect" Problem
**Interviewer:** "A developer tells you they cannot connect from their local laptop to an Azure Linux VM over SSH. Walk me through exactly how you would troubleshoot this."
**Your Answer:**
First, I verify the basics by asking the developer for the exact IP address, username, and error message (e.g., "Connection Refused" vs "Connection Timed Out"). Next, I check the cloud Network Security Group (NSG) attached to the VM's NIC to ensure port 22 is open to their IP. Then, I verify if the VM is actually running and if any enterprise firewalls or VPNs are blocking the route. Finally, if the network is clear, I use the cloud provider's serial console to log into the VM locally and check if the `sshd` service is active and listening.

### 21. Scenario: The "Terraform State Conflict"
**Interviewer:** "Two developers on your team ran `terraform apply` at the same time. Now the pipeline is failing, saying the state is locked. What happened and how do you fix it?"
**Your Answer:**
When Terraform runs, it creates a lock file in the remote backend to prevent concurrent writes, which protects state integrity. If a process is killed abruptly, this lock might not be released automatically. To fix it, I first confirm with the entire team that no active applies are running. Then, I retrieve the Lock ID from the error message and run `terraform force-unlock <Lock_ID>` to manually clear the lock and restore functionality.

### 22. Scenario: The "Accidental Deletion"
**Interviewer:** "A junior engineer accidentally deleted a critical Resource Group containing a Production database. What could have prevented this, and what do you do now?"
**Your Answer:**
This disaster should have been prevented by implementing a Resource Lock (specifically `CanNotDelete`) on production environments, combined with stricter RBAC policies limiting destructive permissions. To react, I would immediately declare a Sev-1 incident and invoke the Disaster Recovery plan. I would use our IaC pipelines to recreate the infrastructure, and then restore the database from the most recent automated backup snapshot. Finally, a blameless post-mortem would be conducted to enforce these safeguards.

### 23. Scenario: The "Pipeline is Running Terraform but Nothing Changes"
**Interviewer:** "Your CI/CD pipeline runs `terraform apply` successfully with exit code 0, but no infrastructure changes. The plan says '0 to add, 0 to change, 0 to destroy.' Why?"
**Your Answer:**
The most likely reason is that the pipeline is pointing to a different state file or workspace than intended, meaning it's comparing the code to the wrong environment. Another possibility is that someone already applied these exact changes manually, so the state is already converged. I would also check if the working directory in the pipeline YAML is correct, or if conditional logic (like `count = 0`) is skipping the resources dynamically.

### 24. Scenario: The "High Latency Between Cloud and On-Premises"
**Interviewer:** "Users at headquarters complain of high latency accessing a newly migrated cloud application. What do you investigate?"
**Your Answer:**
I would first use `traceroute` or `mtr` to validate the network path to see if traffic is taking a sub-optimal internet route instead of a dedicated private link (like ExpressRoute). Next, I check if the application was accidentally deployed to a region physically distant from headquarters. I also review network bandwidth utilization to ensure the VPN isn't saturated, and verify that DNS lookups aren't unnecessarily bouncing back and forth between on-prem and cloud servers.

### 25. Scenario: The "AKS Pods in CrashLoopBackOff"
**Interviewer:** "Developers report production AKS pods are in 'CrashLoopBackOff'. How do you diagnose this?"
**Your Answer:**
`CrashLoopBackOff` means the container starts, crashes, and Kubernetes continuously attempts to restart it. First, I run `kubectl get pods` to identify the failing pod, then `kubectl describe pod <pod-name>` to check events for errors like `OOMKilled` or failed probes. Finally, I check the application logs using `kubectl logs <pod-name> --previous` to see why the application process is fatally exiting. Common causes are missing environment variables or bad database connection strings.
```bash
kubectl logs <pod-name> --previous
```

### 26. Scenario: The "Cloud Cost Spike"
**Interviewer:** "The cloud bill this month spiked by 40% with no major releases. How do you find the cause?"
**Your Answer:**
I start by opening the cloud provider's Cost Management dashboard and grouping the charges by Service and Resource to pinpoint exactly what is driving the cost. I check for orphaned resources, like oversized test VMs or unattached premium disks that developers forgot to delete. I also investigate data egress fees, as unexpected outbound traffic can cause massive spikes. Moving forward, I would set up strict billing alarms and implement auto-shutdown policies for non-production environments.
