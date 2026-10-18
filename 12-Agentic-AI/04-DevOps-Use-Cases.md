---
tags: [ai, devops, automation, use-cases]
source: devopsinsiders/batch-18
created: 2026-06-14
updated: 2026-06-20
---

# 🤖 Agentic AI Use Cases in DevOps — Complete Guide in Simple Language

---

## 🤔 The Big Picture

Before we dive in, let's set expectations. Agentic AI in DevOps is NOT about AI replacing engineers overnight. Think of it this way:

- **You are the Senior Engineer** — You set goals, review changes, design architectures
- **The AI Agent is the Junior Engineer** — It does the repetitive, investigative, grunt work at machine speed, 24 hours a day, 7 days a week, without getting tired or needing sleep

---

## 🚨 Use Case 1: Automated Incident Remediation (AIOps 2.0)

### The Problem Today
A Datadog alert fires at 3:17 AM — "Disk usage on prod-db-01 is 95%." 

PagerDuty wakes up an on-call engineer. They groan, open their laptop, SSH into the server, run `df -h`, find `/var/log` is full, clear old logs, verify disk is back to normal, update the ticket, and go back to sleep.

This whole process took 25 minutes and interrupted someone's sleep.

### With an Agent

```
Alert fires at 3:17 AM: "prod-db-01 disk at 95%"
         ↓
Incident Response Agent wakes up (not a human — an AI)
         ↓
THINK: I need to diagnose this disk issue.
ACT:   run_bash_command("ssh prod-db-01 'df -h'")
       run_bash_command("ssh prod-db-01 'du -sh /var/log/* | sort -rh | head -20'")
OBSERVE: /var/log/app.log is 8.2GB (10 days of unrotated logs)
         ↓
THINK: This is a log rotation issue. Safe to compress/archive old logs.
       But let me check the runbook first.
ACT:   search_knowledge_base("log rotation procedures for prod-db-01")
OBSERVE: Runbook says: "Safe to gzip logs older than 3 days. Do NOT delete within 48h"
         ↓
THINK: I'll compress logs older than 3 days.
ACT:   run_bash_command("ssh prod-db-01 'find /var/log -name \"*.log\" -mtime +3 -exec gzip {} \\;'")
OBSERVE: Success. Disk now at 67%.
         ↓
THINK: Issue resolved. I should fix the log rotation config so this doesn't happen again.
ACT:   create_github_pr(
         title="fix: enable logrotate for app.log on prod-db-01",
         description="Log rotation was not configured. Created /etc/logrotate.d/app config."
       )
         ↓
ACT:   update_pagerduty_ticket(
         status="resolved",
         summary="Disk full due to missing log rotation. Compressed old logs. 
                  PR #391 created to permanently fix log rotation config."
       )
         ↓
Engineer wakes up in the morning to a resolved ticket and a PR to review.
```

**Time saved:** 25+ minutes of interrupted sleep → 0 minutes. The human just reviews the PR in the morning.

---

## 🔧 Use Case 2: CI/CD Pipeline Self-Healing

### The Problem Today
A developer pushes code, the GitHub Actions pipeline fails. They get a Slack notification. They open the pipeline logs, scroll through 2,000 lines of output, find the error on line 1,547: `npm ERR! peer dep missing: react@^17.0.0`.

They figure out the fix, update `package.json`, push again, wait for the pipeline to run...

### With an Agent

```
GitHub Actions pipeline fails
         ↓
Pipeline Healing Agent is triggered by webhook
         ↓
ACT:   read_pipeline_logs(job_id="build-and-test", last_n_lines=100)
OBSERVE: "npm ERR! peer dep missing: react@^17.0.0. Found: react@18.2.0"
         ↓
THINK: Package 'some-library' requires react@17 but the project uses react@18.
       I should check if this library has a newer version compatible with react@18.
ACT:   run_bash_command("npm info some-library versions")
OBSERVE: "1.0.0, 1.0.1, 1.1.0, 2.0.0-beta (supports react@18)"
         ↓
THINK: Version 2.0.0-beta supports react@18. Let me check if there's a stable release.
ACT:   search_web("some-library npm react 18 compatible stable version")
OBSERVE: v2.0.0 stable was released 3 days ago with react@18 support.
         ↓
THINK: I'll update package.json to use some-library@^2.0.0
ACT:   clone_repo("myorg/myapp")
       edit_file("package.json", change "some-library": "^1.1.0" → "^2.0.0")
       run_bash_command("npm install")   # Test locally in sandbox
OBSERVE: npm install succeeds
         ↓
ACT:   create_github_pr(
         title="fix: upgrade some-library to v2.0.0 for react@18 compatibility",
         reviewers=["original-author@company.com"],
         description="Pipeline failed because some-library@1.x requires react@17. 
                      Updated to v2.0.0 which supports react@18."
       )
```

**Developer gets a Slack DM:** "Pipeline failed. I found a dependency conflict and opened PR #88 with a fix. Please review."

---

## 🏗️ Use Case 3: IaC Generation & Refactoring

### The Problem Today
A new team needs a Kubernetes cluster in Azure. The Platform Engineer writes 300+ lines of Terraform across 5 files — `main.tf`, `variables.tf`, `outputs.tf`, `network.tf`, `providers.tf`. This takes 2-3 hours.

### With an Agent

```
Engineer prompts: "Create a production-grade AKS cluster in East US with:
- Private cluster (API server not public)
- Azure CNI networking
- System + User node pools
- Managed identity for auth
- Integration with our existing hub-spoke network (Hub VNet ID: /subscriptions/.../vnet-hub)
- Key Vault integration
- Container Insights monitoring"
         ↓
IaC Generation Agent:
         ↓
THINK: I need to generate a Terraform module for AKS. Let me check the latest 
       AzureRM provider docs for the azurerm_kubernetes_cluster resource.
ACT:   search_web("azurerm_kubernetes_cluster terraform azurerm 3.x latest")
ACT:   read_url("https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster")
         ↓
THINK: I'll generate the module. I need to use use Azure CNI (not kubenet) for 
       advanced network policies, and configure private_cluster_enabled = true.
ACT:   write_to_file("modules/aks/main.tf", <generated terraform code>)
       write_to_file("modules/aks/variables.tf", <variable definitions>)
       write_to_file("modules/aks/outputs.tf", <outputs>)
         ↓
THINK: Let me validate this code before presenting it.
ACT:   run_bash_command("terraform init && terraform validate")
OBSERVE: "Error: argument 'docker_bridge_cidr' is deprecated in AzureRM 3.x"
         ↓
THINK: I used a deprecated argument. Let me fix it.
ACT:   edit_file("modules/aks/main.tf", remove docker_bridge_cidr line)
       run_bash_command("terraform validate")
OBSERVE: "Success! The configuration is valid."
         ↓
ACT:   run_bash_command("terraform plan")
OBSERVE: Plan shows correct resources
         ↓
RESPONSE: "Done! I've generated the AKS Terraform module in modules/aks/. 
           Key decisions: Azure CNI (network_plugin = azure), private cluster,
           system node pool (3x Standard_DS2_v2), user node pool (Standard_D4s_v3).
           The code passed `terraform validate` and `terraform plan` successfully.
           One thing I noticed: I removed the deprecated docker_bridge_cidr argument.
           Please review the code in modules/aks/ before applying."
```

---

## 📊 Use Case 4: Intelligent Post-Mortem & Root Cause Analysis

### The Problem Today
After a production outage, a senior engineer spends 3-4 hours:
- Reviewing Slack incident channels to build a timeline
- Pulling metrics from Datadog
- Checking Git commits for recent changes
- Writing the post-mortem document

### With an Agent

```
Engineer prompts: "Analyze the production outage that occurred yesterday between 
                  14:30 and 16:45 UTC and write a post-mortem."
         ↓
RCA Agent:
ACT:   get_slack_messages(channel="#incidents", from="14:00 UTC", to="17:00 UTC yesterday")
ACT:   query_datadog_metrics(service="payment-api", from="13:00 UTC", to="17:00 UTC")
ACT:   get_git_commits(repo="payment-service", from="12:00 UTC", to="14:30 UTC")
ACT:   get_pagerduty_timeline(incident_id="INC-2847")
         ↓
THINK: I can see: 
       - A deployment at 14:22 UTC introduced commit abc123 (changed DB connection pool size from 10 to 50)
       - Database CPU spiked to 100% at 14:31 UTC
       - Payment API error rate went from 0.01% to 47% at 14:33 UTC
       - First alert fired at 14:35 UTC
       - Rollback was executed at 15:52 UTC (taking 82 minutes from first alert!)
       - Error rate returned to normal at 16:45 UTC
         ↓
ACT:   write_to_file("post-mortem-2024-06-19.md", <comprehensive post-mortem>)
         ↓
Post-mortem includes:
- Timeline with exact timestamps
- Root cause: Connection pool exhaustion due to config change in commit abc123
- Impact: 47% error rate for 2h15m, affecting ~12,000 payment transactions  
- 5 Whys analysis
- Action items:
  1. Add connection pool limit alerting
  2. Add automated rollback on error rate spike
  3. Require load testing for DB config changes
  4. Reduce MTTD (Mean Time to Detect) target
```

---

## 🔄 Use Case 5: Cost Optimization Agent

```
Prompt: "Analyze our Azure costs for the last 30 days and find savings opportunities."
         ↓
FinOps Agent:
ACT:   query_azure_cost_api(subscription="prod", days=30)
ACT:   run_bash_command("az vm list --output json")
ACT:   run_bash_command("az monitor metrics list --resource <each-vm> --metric 'Percentage CPU'")
         ↓
OBSERVE: 
- vm-batch-processor-01: 4-core VM, average CPU: 1.2% over 30 days (massively over-provisioned)
- dev-jumpbox-01: VM running 24/7, 0% weekend usage (no one uses it on weekends)
- 3 "orphaned" disks attached to deleted VMs (paying $45/month for nothing)
         ↓
RESPONSE: "Found 3 savings opportunities totaling ~$320/month:
1. Rightsize vm-batch-processor-01: Downgrade from Standard_D4s_v3 to Standard_B2s ($127/mo savings)
2. Auto-shutdown dev-jumpbox-01 on weekends (Fri 8PM - Mon 8AM): $67/mo savings  
3. Delete 3 orphaned disks: $45/mo savings
I've created tickets in Jira for each optimization. Shall I proceed with any of these?"
```

---

## 🛡️ Safety & Guardrails (Critical!)

AI agents that can run commands on production systems are powerful — and dangerous. These guardrails are non-negotiable:

### 1. Human-in-the-Loop (HITL) — For Destructive Actions
```
Safe (Agent can do automatically):
- Read files, read logs, read metrics
- Run read-only queries
- Create PRs (human still reviews before merge)
- Create tickets

Requires Human Approval:
- terraform apply
- kubectl delete
- DROP TABLE, DELETE FROM
- Scaling resources up/down
- Any production configuration changes
```

### 2. Sandboxed Execution
Commands run inside isolated Docker containers with:
- No access to production credentials
- Filtered network egress (can only call allowed APIs)
- If the agent hallucinates a malicious command, it runs harmlessly in the sandbox

### 3. Audit Logging
Every tool call is logged: what was called, what arguments, what the result was, at what time, with what user-given goal. Full accountability.

---

## 🎯 Key Takeaways

1. **Incidents:** AI agents can resolve common incidents (disk full, memory issues, dependency conflicts) automatically — you review in the morning
2. **CI/CD:** Agents can diagnose failing pipelines, find fixes, and open PRs automatically
3. **IaC:** Agents can generate, validate, and iterate on Terraform/Kubernetes code
4. **Post-mortems:** Agents can synthesize data from multiple sources into a complete incident report
5. **FinOps:** Agents can continuously scan for wasted spend and recommend specific savings
6. **Human oversight is essential** — agents should propose, humans approve anything destructive
