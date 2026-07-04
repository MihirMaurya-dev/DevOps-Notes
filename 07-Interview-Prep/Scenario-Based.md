---
tags: [interview, prep, scenario, troubleshooting]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Scenario-Based Interview Questions

Scenario questions test your ability to apply knowledge to solve realistic problems, demonstrating your troubleshooting methodology.

## Scenario 1: The "Cannot Connect" Problem
**Interviewer:** "A developer tells you they cannot connect from their local laptop to an Azure Linux VM over SSH. Walk me through exactly how you would troubleshoot this."

**Your Answer:**
1. **Verify the Basics:** I would ask the developer for the exact IP address they are trying to connect to, the username, and the exact error message (e.g., "Connection Refused" vs "Connection Timed Out").
2. **Check the Azure NSG:** I would go to the Azure Portal (or use CLI) and check the Network Security Group attached to the VM's NIC and Subnet. Is there an inbound rule allowing Port 22 (TCP) from the developer's public IP address?
3. **Check the VM State:** Is the VM actually running? Is it in a "Failed" state?
4. **Check Routing/Firewalls:** If the VM is on a private network, is the developer connected to the VPN? Does the Azure Firewall have a rule allowing this traffic?
5. **Check OS Level (Serial Console):** If the network looks perfect, I would use the Azure Serial Console to log into the VM locally. I would check if the `sshd` service is actually running (`systemctl status sshd`) and check the local OS firewall (`iptables` or `ufw`) to ensure port 22 isn't blocked locally.

## Scenario 2: The "Terraform State Conflict"
**Interviewer:** "Two developers on your team ran `terraform apply` at the same time. Now the pipeline is failing, saying the state is locked, but neither developer is running Terraform anymore. What happened and how do you fix it?"

**Your Answer:**
1. **What happened:** When Terraform runs, it creates a lock file in the remote backend (e.g., Azure Blob Storage) to prevent concurrent writes. If a pipeline is killed abruptly or a developer loses internet connection mid-apply, the lock might not be released automatically.
2. **How to fix it:** I would first verify with the team that no one is genuinely running an apply. Then, I would obtain the Lock ID from the error message. Finally, I would run `terraform force-unlock <Lock_ID>` to manually remove the lock and restore functionality.

## Scenario 3: The "Accidental Deletion"
**Interviewer:** "A junior engineer accidentally deleted a critical Resource Group containing a Production database. What could have prevented this, and what do you do now?"

**Your Answer:**
1. **Prevention:** This should have been prevented by a **Resource Lock**. A `CanNotDelete` lock should be applied to all production Resource Groups or critical resources. Additionally, the junior engineer's **RBAC role** was too broad; they should have had "Contributor" access scoped strictly to Dev/Test, or "Reader" access in Production.
2. **Reaction:** Once deleted, a Resource Group cannot be undeleted. I would immediately invoke our Disaster Recovery plan. I would use our Infrastructure as Code (Terraform) pipelines to recreate the infrastructure components. Then, I would restore the database from the latest automated Geo-Redundant backup. Finally, I would conduct a post-mortem to enforce locks and tighten RBAC.

## Scenario 4: The "Pipeline is Running Terraform but Nothing Changes"
**Interviewer:** "Your Terraform CI/CD pipeline runs successfully with exit code 0, but no infrastructure is being created or changed. The `terraform plan` output says '0 to add, 0 to change, 0 to destroy.' What could be happening?"

**Your Answer:**
This is a subtle but common issue. The most likely causes, in order of probability:
1. **Wrong State File:** The pipeline is pointing to a different backend (or workspace) than expected. I would check the `backend` configuration and the `TF_WORKSPACE` environment variable.
2. **Already Converged:** The real infrastructure already matches the code exactly (this is the correct behavior — Terraform is idempotent). I would check if someone recently applied the same changes manually.
3. **Wrong Directory:** The pipeline is running `terraform plan` in a directory with empty or already-applied `.tf` files. I would check the `working-directory` setting in the pipeline YAML.
4. **Conditional Logic Resolving to Empty:** A `count = 0` or `for_each = {}` in the code is producing zero resources. I would review the variable values being passed to the pipeline to ensure `environment = "prod"` (or whatever controls the count) is set correctly.

## Scenario 5: The "High Latency Between Azure and On-Premises"
**Interviewer:** "After migrating workloads to Azure, users at the headquarters office are complaining of high latency when accessing the new Azure-hosted application. Previously, everything was fast on-premises. What do you investigate?"

**Your Answer:**
1. **Validate the Route:** First, I'd confirm the traffic path. Is it going over a VPN Gateway (public internet, high latency) or ExpressRoute (private circuit, low latency)? Run `traceroute` from an on-premises machine to the Azure VM's private IP. If it's going over the internet, the fix is to configure ExpressRoute or optimize the VPN Gateway SKU.
2. **Check the Azure Region:** Is the Azure workload deployed in the region closest to headquarters? Deploying to `East US` for a UK-based office adds unnecessary latency. If so, I would evaluate a deployment to `UK South`.
3. **Check Bandwidth Utilization:** I would check the VPN or ExpressRoute circuit's bandwidth utilization. If the circuit is saturated, I need to upgrade the SKU.
4. **Check VM Performance:** I would check if the Azure VM itself is the bottleneck. Is it CPU or memory-bound? Use Azure Monitor metrics. If so, I would resize the VM.
5. **Check DNS Resolution:** If DNS queries are being sent back to on-premises DNS servers for name resolution of Azure resources (instead of using Azure Private DNS), each lookup adds significant latency. I would configure a DNS forwarder or Azure Private DNS Resolver.

## Scenario 6: The "AKS Pods in CrashLoopBackOff"
**Interviewer:** "Developers are reporting that pods in the production AKS cluster are in 'CrashLoopBackOff' status. How do you diagnose this?"

**Your Answer:**
`CrashLoopBackOff` means the pod starts, crashes, Kubernetes restarts it, it crashes again — in a loop.

```bash
# Step 1: Identify which pods are crashing
kubectl get pods -n production

# Step 2: Get the events for a specific crashing pod (look for error messages)
kubectl describe pod <pod-name> -n production

# Step 3: Get the logs from the CURRENT container instance
kubectl logs <pod-name> -n production

# Step 4: If the container exits too fast, get logs from the PREVIOUS failed instance
kubectl logs <pod-name> -n production --previous
```

Common root causes:
- **Application startup failure:** The application itself is crashing (check app logs). Common cause: wrong environment variable (e.g., pointing to a wrong database connection string).
- **Failed readiness probe:** The liveness probe is marking the container unhealthy before it's ready to serve traffic, causing Kubernetes to kill it.
- **OOMKilled:** The container exceeded its memory `limit` and was killed by the OOM (Out of Memory) killer. Check `kubectl describe pod` for `OOMKilled` in the Last State section.
- **Image pull error:** The wrong image tag was deployed, or the AKS cluster doesn't have permission to pull from the ACR. Check the pod events for `ErrImagePull`.

## Scenario 7: The "Azure Cost Spike"
**Interviewer:** "The Azure bill this month is 40% higher than last month. You have no obvious change deployed. How do you identify the cause?"

**Your Answer:**
1. **Azure Cost Analysis:** Go to Azure Cost Management + Billing → Cost Analysis. Filter by the spike period. Group by **Service**, then by **Resource**, to identify which specific resource type and resource caused the increase.
2. **Check Azure Advisor:** Azure Advisor often flags idle or underutilized resources. It might identify a large VM or an oversized AKS node pool that was spun up and never turned off.
3. **Check for Undeleted Dev Resources:** In many organizations, developers spin up expensive resources for testing and forget to delete them. I'd check the `Environment: Dev` tagged resources for anything large and idle.
4. **Check Data Egress:** Unexpected data transfer charges are a common culprit. I'd check Azure Front Door, VPN Gateways, and storage accounts for unusual outbound data transfer.
5. **Check for Runaway Autoscaling:** An AKS cluster with aggressive autoscaling may have scaled out to many nodes during a load test that was never decommissioned. Check the node count history.
6. **Set Up Budgets and Alerts:** As a preventive measure going forward, I would create Azure Budget Alerts to notify the team at 80% and 100% of the monthly budget threshold.
