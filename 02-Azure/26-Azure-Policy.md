---
category: Azure-Governance
tags: [azure, policy, governance, compliance, architecture]
type: enterprise-architect-guide
status: active
---

# 🛡️ Azure Policy - Enterprise Architect Guide

## 1. Introduction
Azure Policy is a governance service used to create, assign, and manage policies that enforce different rules and effects over your resources. It ensures your Azure environment remains compliant with your corporate standards, security baselines, and service level agreements (SLAs).

## 2. Why This Service Exists
While **Azure RBAC** controls *who* can perform actions (e.g., "John can create VMs"), **Azure Policy** controls *what* can be created and *how* it must be configured (e.g., "Any VM created must be in the East US region and must not use the expensive G-Series SKU"). Without Azure Policy, enforcing cost control, security standards, and naming conventions relies on humans remembering the rules—which leads to massive cloud sprawl and compliance failures.

## 3. Architecture
- **Scope:** **Global** (operates across Management Groups, Subscriptions, and Resource Groups).
- **Layer:** Control Plane (Azure Resource Manager - ARM).
- **Under the Hood:** Azure Policy intercepts requests made to Azure Resource Manager (PUT, PATCH) before they are executed. It also runs a background compliance evaluation cycle roughly every 24 hours to flag existing resources that have drifted out of compliance.

## 4. Core Components
- **Policy Definition:** The JSON document detailing the specific condition to evaluate and the effect to take (e.g., "If resource is a Storage Account AND HTTPS is disabled -> Deny").
- **Initiative (Policy Set):** A collection of multiple policy definitions grouped together to achieve a broader goal (e.g., a "PCI-DSS Compliance Initiative" containing 50 specific policies).
- **Assignment:** The process of applying a Policy or Initiative to a specific scope (Management Group, Subscription, or Resource Group).
- **Exemption:** A mechanism to exclude a specific resource or resource hierarchy from an assigned policy (e.g., a temporary waiver for a legacy system).

## 5. Step-by-Step Request Flow
**Scenario:** A developer tries to deploy a Storage Account without enforcing secure transfer (HTTPS), which violates a corporate policy.
1. The developer executes a Terraform script (or uses the Portal) to create the Storage Account.
2. The request is sent to the **Azure Resource Manager (ARM)** API.
3. Before processing the creation, ARM passes the request payload to the **Azure Policy Engine**.
4. The Policy Engine evaluates the payload against all policies assigned to that subscription.
5. It detects a violation of the "Secure Transfer Required" policy, which has a `Deny` effect.
6. The Policy Engine blocks the request. ARM returns a `403 Forbidden` error to the developer with the specific Policy ID that blocked it.

## 6. Real-World Production Use Cases
1. **Data Residency Enforcement:** Ensuring all resources are deployed only in `eu-west` or `eu-north` to comply with GDPR.
2. **Cost Control:** Blocking the creation of massively expensive GPU compute instances (e.g., ND-series) across the enterprise, except in a specific R&D subscription.
3. **Security Baselines:** Enforcing that all Storage Accounts disable public blob access, and all Key Vaults have Soft Delete enabled.
4. **Tagging Compliance:** Automatically appending a "CostCenter" tag to a resource upon creation if the user forgets it.

## 7. Architecture & Design Considerations
- **Scope Strategy:** Always assign policies at the highest appropriate level—ideally at the **Management Group** level. Assigning policies individually per subscription leads to management nightmares.
- **Initiatives over Definitions:** Never assign single policies if you can avoid it. Group related policies into an Initiative and assign the Initiative. If you need to add a rule later, you just update the Initiative.
- **Evaluation Delays:** New policy assignments take about 30 minutes to take effect. Full compliance scans of existing resources run every 24 hours, though you can manually trigger a scan via the REST API/CLI.

## 8. Microsoft Best Practices
- **Test with 'Audit' Mode:** When rolling out a new policy to a brownfield environment, always set the effect to `Audit` first. Let it run for a week, review the compliance dashboard to see what *would* be broken, fix those resources, and then flip the policy to `Deny`.
- **Use Built-in Policies:** Microsoft provides hundreds of built-in policies and initiatives (NIST, ISO 27001, CIS). Use these instead of writing custom JSON policies from scratch whenever possible.

## 9. Security Best Practices
- **Enforce Defender:** Use Azure Policy with the `DeployIfNotExists` effect to automatically enable Microsoft Defender for Cloud and the Azure Monitor Agent on all newly created VMs.
- **Network Isolation:** Use policy to mandate that PaaS services (SQL, Storage) are created with Private Endpoints and have public network access denied.

## 10. Monitoring & Observability
- **Compliance Dashboard:** The Azure Policy dashboard provides a central view of your compliance state.
- **Event Grid Integration:** Azure Policy compliance state changes can be routed to Azure Event Grid, which can trigger Logic Apps to automatically email resource owners when their resources become non-compliant.

## 11. Backup & Disaster Recovery
- **Policy as Code:** Do not create policies manually in the Azure Portal. Policies should be treated as code (JSON definitions, Terraform, Bicep) and stored in Git. If a tenant is compromised or policies are deleted, you simply rerun your CI/CD pipeline to restore the governance framework.

## 12. Cost Optimization Techniques
- Azure Policy is inherently a cost-optimization tool. Use it to restrict allowable VM SKUs, enforce auto-shutdown schedules (via tags), and prevent the deployment of expensive load balancers where not needed.
- Azure Policy itself is a **Free** service in Azure.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Policy?
   **A:** A service to enforce organizational standards and assess compliance at scale.
2. **Q:** How is Azure Policy different from RBAC?
   **A:** RBAC focuses on user actions (who can do what), while Policy focuses on resource properties (what can be created and how).

### Intermediate
3. **Q:** What is an Initiative in Azure Policy?
   **A:** A collection of policy definitions grouped together to achieve a single broader goal (e.g., PCI-DSS compliance).
4. **Q:** Name four common Azure Policy effects.
   **A:** `Deny`, `Audit`, `Append`, and `DeployIfNotExists`. Other effects include `Modify`, `AuditIfNotExists`, and `Disabled`.
5. **Q:** How do you test a new policy without breaking existing deployments?
   **A:** Assign the policy with an `Audit` effect first. It flags non-compliant resources without blocking them.

### Advanced
6. **Q:** Explain how `DeployIfNotExists` works.
   **A:** If a resource is created but is missing a related required resource or property (like a diagnostic setting), the policy automatically deploys a template to remediate it.
7. **Q:** How can you exempt a specific resource from a broader Management Group policy assignment?
   **A:** By creating a Policy Exemption specifically for that resource's scope, optionally with a time limit.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** An infrastructure pipeline (Terraform) fails with a `403 Forbidden - Request Disallowed by Policy`.
  - **Resolution:** Review the error message, which will provide the specific Policy Definition ID. Check the policy rules. Usually, the resource payload is missing a required tag or is using a forbidden property. Update the Terraform code to comply with the policy.
- **Scenario:** A `DeployIfNotExists` policy is not automatically remediating resources.
  - **Resolution:** `DeployIfNotExists` requires Azure Policy to perform actions (like creating a diagnostic setting). It does this using a **Managed Identity**. Ensure the Policy Assignment was given a Managed Identity and that the identity has the correct RBAC role (e.g., Contributor) on the target scope.

## 15. Hands-on Implementation
**Azure CLI Example (Assigning a built-in policy):**
```bash
# Assign the "Require a tag on resources" policy to a Resource Group
az policy assignment create \
  --name "require-costcenter-tag" \
  --display-name "Require CostCenter Tag" \
  --policy "1e30110a-5ceb-460c-a204-c1c3969c6d62" \
  --params "{ \"tagName\": { \"value\": \"CostCenter\" } }" \
  --resource-group rg-production
```

## 16. Terraform Implementation (IaC)
```hcl
# 1. Define a Custom Policy
resource "azurerm_policy_definition" "restrict_locations" {
  name         = "restrict-locations"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Allowed resource locations"

  policy_rule = <<POLICY_RULE
    {
      "if": {
        "not": {
          "field": "location",
          "in": "[parameters('allowedLocations')]"
        }
      },
      "then": {
        "effect": "Deny"
      }
    }
  POLICY_RULE

  parameters = <<PARAMETERS
    {
      "allowedLocations": {
        "type": "Array",
        "metadata": {
          "description": "The list of allowed locations for resources.",
          "displayName": "Allowed locations",
          "strongType": "location"
        }
      }
    }
  PARAMETERS
}

# 2. Assign the Policy to a Subscription
resource "azurerm_subscription_policy_assignment" "location_assignment" {
  name                 = "enforce-eu-locations"
  policy_definition_id = azurerm_policy_definition.restrict_locations.id
  subscription_id      = "/subscriptions/00000000-0000-0000-0000-000000000000"

  parameters = <<PARAMS
    {
      "allowedLocations": {
        "value": [ "westeurope", "northeurope" ]
      }
    }
  PARAMS
}
```

## 17. Production Readiness Checklist
- [ ] Are policies assigned at the Management Group level rather than Subscription level?
- [ ] Are custom policies grouped into Initiatives?
- [ ] Were all `Deny` policies thoroughly tested in `Audit` mode first?
- [ ] Do all `DeployIfNotExists` and `Modify` policy assignments have the correct Managed Identities configured?
- [ ] Is the entire policy framework managed as code in source control?