---
category: Azure-Monitoring
tags: [azure, monitor, observability, alerts, metrics, architecture]
type: enterprise-architect-guide
status: active
---

# 📊 Azure Monitor - Enterprise Architect Guide

## 1. Introduction
Azure Monitor is the comprehensive, full-stack observability solution for collecting, analyzing, and acting on telemetry data from your cloud and on-premises environments. It provides a single pane of glass into the performance, health, and availability of applications and infrastructure.

## 2. Why This Service Exists
Without observability, you are flying blind. When an application crashes, you need to know *why*, *when*, and *where* it failed. Managing multiple disjointed monitoring tools (Nagios for infrastructure, New Relic for APM) is expensive and siloed. Azure Monitor exists to unify infrastructure metrics, application logs, and automated alerting into a single, deeply integrated platform.

## 3. Architecture
- **Scope:** Global data collection, Regional data storage (Log Analytics).
- **Layer:** Platform / Management.
- **Under the Hood:** Azure Monitor is an umbrella term. It ingests two fundamental types of data: **Metrics** (lightweight numerical data stored in a fast time-series database for near-real-time alerting) and **Logs** (rich, structured text data stored in a Log Analytics Workspace for deep querying via KQL).

## 4. Core Components
- **Metrics Explorer:** Tool to visualize real-time numerical data (e.g., CPU %, Network In/Out).
- **Application Insights:** Application Performance Management (APM) for code-level tracing (exceptions, slow SQL queries, dependency mapping).
- **Azure Monitor Agent (AMA):** The unified agent installed on VMs to collect guest OS metrics and event logs.
- **Data Collection Rules (DCR):** The configuration that tells the AMA exactly *what* to collect and *where* to send it.
- **Alert Rules & Action Groups:** The logic that evaluates metrics/logs and the actions to take when a threshold is breached (Email, SMS, Webhook).

## 5. Step-by-Step Request Flow
**Scenario:** Triggering an alert for high CPU on a VM.
1. The VM's CPU hits 95%.
2. The Azure Hypervisor (or the AMA agent) captures this data point and sends it to the **Azure Monitor Metrics** database.
3. An **Alert Rule** runs a query every 1 minute checking if `CPU > 90%`.
4. The condition is met, and the Alert fires, changing state to `Fired`.
5. The Alert triggers an **Action Group**.
6. The Action Group executes its defined actions: It sends an SMS to the on-call engineer and triggers a Webhook to create an incident in ServiceNow.

## 6. Real-World Production Use Cases
1. **Application Tracing:** Using Application Insights to map the topology of a microservices architecture, instantly identifying that an API is slow because it is waiting on a specific external third-party API.
2. **Autoscaling:** Using Azure Monitor metrics to feed the Virtual Machine Scale Set engine, triggering a scale-out event before users notice degradation.
3. **Audit & Compliance:** Archiving all Azure Key Vault and Entra ID access logs to Azure Storage via Monitor Diagnostic Settings for 7-year retention.

## 7. Architecture & Design Considerations
- **Diagnostic Settings:** By default, Azure resources only store basic metrics for 93 days, and they store ZERO logs. You **must** manually configure "Diagnostic Settings" on every resource to ship logs to a Log Analytics Workspace for retention and querying.
- **AMA vs MMA:** The legacy Log Analytics Agent (MMA/OMS) is deprecated. Always design new architectures using the **Azure Monitor Agent (AMA)** and Data Collection Rules (DCRs) for better filtering and performance.

## 8. Microsoft Best Practices
- **Use Data Collection Rules (DCRs) to Filter Noise:** Don't ingest every single Windows Event log. Use DCRs to only ingest "Error" and "Critical" logs. This saves massive amounts of money on ingestion costs.
- **Centralized Alerting:** Define alerts as code (Terraform) and use central Action Groups. Don't let developers click around creating random, undocumented email alerts that lead to alert fatigue.

## 9. Security Best Practices
- **Private Link for Monitor:** Use Azure Monitor Private Link Scope (AMPLS) to ensure that servers send their telemetry to Azure Monitor privately over the Microsoft backbone, rather than over the public internet.
- **RBAC:** Restrict who can view logs. Use Resource-Context RBAC so developers can query logs for their specific App Service, but cannot see logs for the core network firewalls.

## 10. Monitoring & Observability
- Azure Monitor *is* the observability platform. 
- Use **Azure Workbooks** to create beautiful, interactive, single-pane-of-glass dashboards combining Metrics, Logs, and Security data for executive summaries or NOC screens.

## 11. Backup & Disaster Recovery
- Monitor alerts, DCRs, and dashboards should be stored as Infrastructure as Code to ensure they can be redeployed if a region is lost.
- Log Analytics Workspaces (where logs are stored) cannot be easily failed over. In strict environments, configure diagnostic settings to send logs to *both* a primary and a secondary workspace.

## 12. Cost Optimization Techniques
- **Ingestion Costs:** Log Analytics charges per GB ingested. Turn off verbose debug logging in production. 
- **Basic Logs:** For high-volume, low-value logs (like NSG Flow Logs), route them to a table configured for "Basic Logs" which is significantly cheaper than standard "Analytics Logs", though it limits advanced querying.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Monitor?
   **A:** A comprehensive solution for collecting, analyzing, and acting on telemetry from cloud and on-premises environments.
2. **Q:** What are the two primary data types in Azure Monitor?
   **A:** Metrics (numerical, lightweight, real-time) and Logs (structured/unstructured text for deep analysis).

### Intermediate
3. **Q:** What is an Action Group?
   **A:** A collection of notification preferences (Email, SMS) and automated actions (Azure Functions, Logic Apps) that trigger when an alert fires.
4. **Q:** What is Application Insights?
   **A:** An APM (Application Performance Management) feature of Azure Monitor designed to monitor live web applications.
5. **Q:** What is the difference between Diagnostic Settings and Metrics?
   **A:** Metrics are collected automatically by default. Diagnostic Settings must be manually configured to send detailed resource logs and deeper metrics to a destination (like Log Analytics).

### Advanced
6. **Q:** How do you monitor network traffic entering and leaving a VNet?
   **A:** By enabling NSG Flow Logs, which capture IP traffic information and send it to Azure Storage or Log Analytics (Traffic Analytics) for visualization.
7. **Q:** What is Azure Monitor Agent (AMA)?
   **A:** The modern agent installed on VMs to collect monitoring data. It replaces the legacy Log Analytics agent (MMA) and uses Data Collection Rules (DCRs) to filter and route telemetry efficiently.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** An alert was supposed to fire, but didn't.
  - **Resolution:** 
    1. Check if the metric actually breached the threshold for the required duration (e.g., it spiked to 95% for 1 minute, but the rule requires 5 minutes sustained). 
    2. Check the Action Group configuration to ensure the email wasn't blocked or the webhook URL didn't expire.
- **Scenario:** Application Insights is not capturing SQL dependency times.
  - **Resolution:** Ensure the Application Insights SDK is installed properly in the code, or the auto-instrumentation agent (for .NET/Java) is enabled on the App Service. Basic ping tests won't capture deep SQL calls without the agent.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create an Action Group
az monitor action-group create \
  --resource-group rg-monitor \
  --name ag-critical-alerts \
  --action email admin admin@contoso.com

# Create a Metric Alert for High CPU
az monitor metrics alert create \
  -n "alert-high-cpu" \
  -g rg-monitor \
  --scopes /subscriptions/.../virtualMachines/vm-prod \
  --condition "avg Percentage CPU > 90" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action /subscriptions/.../actionGroups/ag-critical-alerts
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_monitor_action_group" "ag" {
  name                = "ag-critical-alerts"
  resource_group_name = azurerm_resource_group.rg.name
  short_name          = "crit-alerts"

  email_receiver {
    name          = "sendtodevops"
    email_address = "devops@contoso.com"
  }
}

resource "azurerm_monitor_metric_alert" "cpu" {
  name                = "alert-high-cpu"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [azurerm_linux_virtual_machine.vm.id]
  description         = "Action will be triggered when CPU is greater than 90."

  criteria {
    metric_namespace = "Microsoft.Compute/virtualMachines"
    metric_name      = "Percentage CPU"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 90
  }

  action {
    action_group_id = azurerm_monitor_action_group.ag.id
  }
}
```

## 17. Production Readiness Checklist
- [ ] Are Diagnostic Settings enforced via Azure Policy on all resources?
- [ ] Are Action Groups mapped to a PagerDuty or ITIL system rather than individual emails?
- [ ] Is Application Insights enabled for all custom-developed PaaS applications?
- [ ] Are alerts tuned to prevent alert fatigue (e.g., ignoring 10-second CPU spikes)?
- [ ] Is the Azure Monitor Agent (AMA) and DCRs being used instead of the legacy MMA?