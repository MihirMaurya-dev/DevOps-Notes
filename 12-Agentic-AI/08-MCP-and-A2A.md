---
tags: [mcp, a2a, protocol, tools, agentic-ai, multi-agent]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🔌 Step 4 — MCP Tools & A2A Protocol

You can build agents. Now make them connect to real-world tools using a **standard protocol (MCP)** and collaborate with other agents using a **communication protocol (A2A)**.

---

## 🔌 Part 1: MCP (Model Context Protocol)

### What Is MCP?

**MCP (Model Context Protocol)** is an open standard created by Anthropic. It defines a universal, standardized way for AI agents to connect to external tools and data sources.

**The Problem MCP Solves:**

```
Without MCP:
  Agent A needs GitHub     → Write custom GitHub integration code
  Agent A needs Azure      → Write custom Azure integration code
  Agent A needs Kubernetes → Write custom K8s integration code
  Agent B also needs GitHub → Write it AGAIN from scratch

  Result: Every team writes their own integrations. No reuse. Huge effort.

With MCP:
  GitHub MCP Server exists  → Any MCP agent can use it instantly
  Azure MCP Server exists   → Any MCP agent can use it instantly
  K8s MCP Server exists     → Any MCP agent can use it instantly

  Result: Write the MCP Server once, all agents can use it.
```

> 🔌 **The USB-C analogy:** Before USB-C, every phone had a different charger. MCP is the USB-C for AI agents — one standard that connects everything.

---

### How MCP Works

```
┌─────────────────┐         MCP Protocol          ┌──────────────────────┐
│   AI Agent      │ ◄───────────────────────────► │   MCP Server         │
│  (LangGraph,    │                               │  (exposes tools as   │
│   Claude, etc.) │   1. List available tools     │   standardized API)  │
│                 │   2. Call a tool with args    │                      │
│                 │   3. Receive structured result│                      │
└─────────────────┘                               └──────────────────────┘
```

**MCP Server** = A small service that exposes tools in a standardized format. It can be:
- A local process (running on the same machine)
- A remote HTTP server
- A Docker container in your Kubernetes cluster

---

### MCP Servers for DevOps

| MCP Server | What Tools It Exposes |
|-----------|----------------------|
| **GitHub MCP** | `list_repos`, `create_pr`, `get_file`, `list_issues`, `merge_pr` |
| **Azure MCP** | `list_vms`, `start_vm`, `get_logs`, `list_resource_groups` |
| **Kubernetes MCP** | `get_pods`, `describe_pod`, `get_logs`, `scale_deployment` |
| **Terraform MCP** | `terraform_plan`, `terraform_validate`, `terraform_fmt` |
| **Prometheus MCP** | `query_metrics`, `list_alerts`, `get_alert_details` |
| **Jira MCP** | `create_ticket`, `update_ticket`, `get_sprint_issues` |

---

### Building a Simple MCP Server

```python
# mcp_server_kubernetes.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import subprocess
import json

server = Server("kubernetes-devops-tools")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Tell agents what tools this server provides."""
    return [
        Tool(
            name="get_pod_status",
            description="Get the status of all pods in a Kubernetes namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "The Kubernetes namespace to check"
                    }
                },
                "required": ["namespace"]
            }
        ),
        Tool(
            name="get_pod_logs",
            description="Get recent logs from a specific pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {"type": "string"},
                    "namespace": {"type": "string"},
                    "lines": {"type": "integer", "default": 100}
                },
                "required": ["pod_name", "namespace"]
            }
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool when the agent calls it."""
    if name == "get_pod_status":
        result = subprocess.run(
            ["kubectl", "get", "pods", "-n", arguments["namespace"]],
            capture_output=True, text=True
        )
        return [TextContent(type="text", text=result.stdout)]

    elif name == "get_pod_logs":
        lines = arguments.get("lines", 100)
        result = subprocess.run(
            ["kubectl", "logs", arguments["pod_name"],
             "-n", arguments["namespace"], f"--tail={lines}"],
            capture_output=True, text=True
        )
        return [TextContent(type="text", text=result.stdout)]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]

# Run the MCP server
if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(server))
```

**Run it:**
```bash
pip install mcp
python mcp_server_kubernetes.py
```

Now any MCP-compatible agent (Claude Desktop, LangChain with MCP adapter, etc.) can use your Kubernetes tools.

---

### Using MCP Tools in LangChain

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

async def main():
    # Connect to multiple MCP servers at once
    async with MultiServerMCPClient({
        "kubernetes": {
            "command": "python",
            "args": ["mcp_server_kubernetes.py"],
            "transport": "stdio",
        },
        "github": {
            "url": "http://github-mcp-server:3000/mcp",
            "transport": "streamable_http",
        }
    }) as client:
        tools = await client.get_tools()

        llm = ChatOpenAI(model="gpt-4o")
        agent = create_react_agent(llm, tools)

        result = await agent.ainvoke({
            "messages": [{"role": "user", "content":
                "Check production pods status and if any are failing, open a GitHub issue"}]
        })
        print(result)
```

---

## 🤝 Part 2: A2A (Agent-to-Agent Protocol)

### What Is A2A?

**A2A (Agent-to-Agent Protocol)** is an open standard by Google that allows AI agents from **different frameworks, vendors, and teams** to discover each other and collaborate.

**The Problem A2A Solves:**

```
Without A2A:
  All logic in one giant agent
  → Too complex, fragile, hard to maintain
  → LangGraph agent can't work with a CrewAI agent
  → Your agent can't delegate to a partner company's agent

With A2A:
  Specialist agents expose their capabilities via "Agent Cards"
  → An Orchestrator discovers and delegates to the right specialist
  → Works across frameworks and organizations
```

---

### How A2A Works

```
┌──────────────────────────┐
│   Orchestrator Agent     │   "Fix the production outage"
│   (the coordinator)      │
└────────────┬─────────────┘
             │
      [A2A Discovery: find agents that can help]
             │
    ┌────────┴─────────────────────────┐
    │                                  │
    ▼                                  ▼
┌────────────────┐           ┌──────────────────┐
│  Diagnostic    │           │  Remediation     │
│  Agent         │           │  Agent           │
│ "I found OOM   │──────────►│ "I've scaled the │
│  in pod-xyz"   │  (result) │  deployment up"  │
└────────────────┘           └──────────────────┘
         │                            │
         └─────────────┬──────────────┘
                       ▼
              ┌────────────────┐
              │  Notification  │
              │  Agent         │
              │ "Incident      │
              │  resolved,     │
              │  updating      │
              │  Slack + Jira" │
              └────────────────┘
```

---

### A2A Agent Card

Each A2A-compatible agent publishes an **Agent Card** — a JSON descriptor that says what the agent can do:

```json
{
  "name": "Kubernetes Diagnostic Agent",
  "description": "Diagnoses issues in Kubernetes clusters by analysing pod status, logs, and events",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "diagnose_pod_issue",
      "name": "Diagnose Pod Issue",
      "description": "Investigates why pods are failing in a given namespace",
      "inputModes": ["text"],
      "outputModes": ["text"],
      "examples": [
        "Why are pods in production crashing?",
        "Investigate OOMKilled pods in the payments namespace"
      ]
    }
  ],
  "url": "http://k8s-diagnostic-agent:8080"
}
```

---

### MCP vs A2A — Quick Comparison

| | MCP | A2A |
|--|-----|-----|
| **Purpose** | Agent ↔ Tools | Agent ↔ Agent |
| **Analogy** | USB-C (connects device to accessories) | Telephone (one device calls another) |
| **Who made it** | Anthropic | Google |
| **What it connects** | LLMs to external APIs/tools | Autonomous agents to each other |
| **Example** | Agent uses GitHub MCP to create a PR | Orchestrator delegates to Diagnostic Agent via A2A |

---

## ✅ Ready for the Finish When You Can...

- [ ] Explain what MCP is and why it matters (in simple language)
- [ ] Build a simple MCP server that exposes 2 DevOps tools
- [ ] Connect a LangGraph agent to an MCP server and use its tools
- [ ] Explain what A2A is and how it differs from MCP
- [ ] Design a multi-agent architecture using A2A for a real DevOps scenario (on paper)
