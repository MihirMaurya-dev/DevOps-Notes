---
tags: [python, agentic-ai, programming, fundamentals]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🐍 Step 1 — Python for Agentic AI

Python is the **foundation** of this entire roadmap. Every framework — LangChain, LangGraph, n8n scripting, vector databases — is Python-first. Strong Python = everything else becomes easy.

---

## 🤔 Why Python Specifically?

- **LangChain, LangGraph, CrewAI, AutoGen** → All Python
- **OpenAI, Gemini, Anthropic SDKs** → Python-first
- **Vector DBs (Pinecone, Chroma, Qdrant)** → Python SDKs
- **DevOps tooling** → `subprocess`, `azure-mgmt`, `azure-identity`, `azure-mgmt-compute`, `kubernetes` Python clients
- **Data processing** → JSON, YAML, CSV — all trivial in Python

---

## 📚 What to Learn (Ordered)

### 1. Core Python Basics

```python
# Variables and types
name = "DevOps Agent"
port = 8080
is_running = True
servers = ["vm-01", "vm-02", "vm-03"]
config = {"region": "eastus", "sku": "Standard_D2s_v3"}

# f-strings (used everywhere in prompts)
print(f"Deploying {name} on port {port} in {config['region']}")

# List comprehension (used to filter resources)
large_vms = [vm for vm in servers if "prod" in vm]
```

### 2. Functions (Agent Tools are Functions)

Every tool you give to an AI agent is a Python function. This is the most important concept:

```python
def get_pod_status(namespace: str, pod_name: str) -> str:
    """
    Returns the status of a Kubernetes pod.
    The agent calls this when it needs to check pod health.
    """
    import subprocess
    result = subprocess.run(
        ["kubectl", "get", "pod", pod_name, "-n", namespace, "-o", "json"],
        capture_output=True, text=True
    )
    return result.stdout

def create_github_pr(title: str, body: str, branch: str) -> dict:
    """
    Creates a GitHub Pull Request.
    The agent calls this after generating a fix.
    """
    import requests
    response = requests.post(
        "https://api.github.com/repos/myorg/myrepo/pulls",
        headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
        json={"title": title, "body": body, "head": branch, "base": "main"}
    )
    return response.json()
```

> **Key insight:** When you write agent tools, you are essentially writing well-typed, well-documented Python functions. The LLM reads the function name, arguments, and docstring to decide when and how to call it.

### 3. Classes and OOP (Agents are Objects)

```python
class DevOpsAgent:
    def __init__(self, name: str, tools: list):
        self.name = name
        self.tools = tools
        self.memory = []  # Stores conversation history

    def run(self, goal: str) -> str:
        self.memory.append({"role": "user", "content": goal})
        # ... agent loop logic
        return "Task completed"

# Usage
agent = DevOpsAgent(
    name="IncidentResponder",
    tools=[get_pod_status, create_github_pr]
)
result = agent.run("Why are pods in production crashing?")
```

### 4. REST APIs with `requests`

Agents constantly call external APIs (Azure, GitHub, Kubernetes, PagerDuty):

```python
import requests
import os

# Call Azure REST API to list VMs
def list_azure_vms(subscription_id: str, token: str) -> list:
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Compute/virtualMachines?api-version=2023-07-01"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

# Call OpenAI API directly (what LangChain does under the hood)
def call_llm(prompt: str) -> str:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        json={
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 5. Async / Await (Critical for Agent Performance)

LLM API calls take 2–10 seconds each. If your agent makes 5 sequential calls, that's 10–50 seconds of waiting. `async` lets you make multiple calls simultaneously:

```python
import asyncio
import httpx  # async-friendly version of requests

async def check_all_services(service_urls: list[str]) -> dict:
    """Check health of multiple services simultaneously."""
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f"{url}/health") for url in service_urls]
        responses = await asyncio.gather(*tasks)

    return {
        url: resp.json()
        for url, resp in zip(service_urls, responses)
    }

# Run: checks all 5 services in ~2s instead of ~10s
results = asyncio.run(check_all_services([
    "http://payment-api",
    "http://auth-service",
    "http://order-service",
    "http://inventory-api",
    "http://notification-service"
]))
```

### 6. File I/O (Agents Read/Write IaC Files)

```python
import json
import yaml

# Read a Kubernetes manifest
def read_manifest(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

# Update a Terraform tfvars file
def update_tfvars(path: str, key: str, value: str):
    with open(path, "r") as f:
        content = f.read()

    # Simple replacement (real agents use regex or HCL parser)
    updated = content.replace(f'{key} = ', f'{key} = "{value}" #')

    with open(path, "w") as f:
        f.write(updated)

# Parse JSON API response
def parse_azure_costs(response_json: str) -> list:
    data = json.loads(response_json)
    return [
        {"name": item["name"], "cost": item["properties"]["cost"]}
        for item in data["value"]
    ]
```

### 7. Environment Variables (Never Hardcode Secrets)

```python
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # reads from .env file

# Always use env vars for secrets
openai_key = os.getenv("OPENAI_API_KEY")
azure_sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
github_token = os.getenv("GITHUB_TOKEN")

if not openai_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")
```

### 8. Error Handling (Agents Must Be Resilient)

```python
import time

def run_kubectl_with_retry(command: list, max_retries: int = 3) -> str:
    """Agents should retry transient failures, not give up immediately."""
    import subprocess

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                raise RuntimeError(f"kubectl error: {result.stderr}")
            return result.stdout

        except RuntimeError as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Attempt {attempt+1} failed. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise  # Re-raise on final attempt
```

---

## 🛠️ Python Setup for Agentic AI Projects

```bash
# Create a clean virtual environment
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\activate             # Windows

# Install core agentic AI packages
pip install langchain langchain-openai langchain-community
pip install langgraph
pip install openai google-generativeai anthropic
pip install chromadb pinecone-client
pip install python-dotenv httpx requests pyyaml

# Save dependencies
pip freeze > requirements.txt
```

---

## 🎯 Mini Projects to Build Confidence

| Project | Skills Practiced |
|---------|-----------------|
| **Azure VM Lister:** Script that calls Azure REST API and lists all VMs with their CPU usage | REST API, env vars, JSON parsing |
| **Log Analyser:** Script that reads a log file, calls an LLM to classify each error, and outputs a summary | File I/O, REST API, string formatting |
| **Health Checker:** Async script that checks 10 service endpoints simultaneously and reports which are down | async/await, error handling |
| **Terraform Helper:** Script that reads a `.tf` file, sends it to an LLM, and prints suggested improvements | File I/O, LLM API call, f-strings |

---

## ✅ Ready for Step 2 When You Can...

- [ ] Write a function that calls a REST API and parses the JSON response
- [ ] Use `async/await` to make 3 API calls simultaneously
- [ ] Read a YAML file and modify a value, then write it back
- [ ] Use environment variables for all secrets (no hardcoded keys)
- [ ] Handle errors gracefully with try/except and retries
- [ ] Explain what OOP is and why agents are implemented as classes
