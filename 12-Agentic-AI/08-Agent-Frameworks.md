---
tags: [langchain, langgraph, crewai, agents, frameworks, agentic-ai]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🤖 Step 3 — Agent Frameworks (LangChain / LangGraph)

You now understand chains and RAG. Step 3 adds the **loop** — the agent can take actions, observe results, decide what to do next, and keep going until the goal is achieved.

---

## 🧠 What Makes a Framework an "Agent Framework"?

A regular program follows fixed steps: A → B → C → Done.

An agent framework provides:
1. **Tool registry** — A way to define and manage what tools the agent can use
2. **ReAct loop** — The Observe → Think → Act → Observe cycle
3. **State management** — Remembering what happened across many steps
4. **Human-in-the-loop** — Pausing to ask for approval before dangerous actions
5. **Multi-agent coordination** — Multiple AI agents working together

---

## 🔗 LangChain — Start Here

LangChain is the most popular AI framework. Use it to understand the core concepts before moving to LangGraph.

### Simple LangChain Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate
import subprocess

# --- 1. Define tools (functions the agent can call) ---
@tool
def run_kubectl(command: str) -> str:
    """Run a kubectl command and return output. Use for Kubernetes operations."""
    result = subprocess.run(
        command.split(), capture_output=True, text=True, timeout=30
    )
    return result.stdout or result.stderr

@tool
def run_azure_cli(command: str) -> str:
    """Run an Azure CLI (az) command. Use for Azure resource management."""
    result = subprocess.run(
        ["az"] + command.split(), capture_output=True, text=True
    )
    return result.stdout or result.stderr

@tool
def search_runbook(query: str) -> str:
    """Search internal runbooks and past incidents for relevant procedures."""
    # In real implementation, this would query your vector DB
    return f"Runbook found for '{query}': [example procedure]"

tools = [run_kubectl, run_azure_cli, search_runbook]

# --- 2. Setup the LLM and prompt ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a DevOps expert agent. Diagnose and fix infrastructure issues step by step."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # Agent's reasoning goes here
])

# --- 3. Create agent and executor ---
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 4. Run ---
result = agent_executor.invoke({"input": "Why are pods in the production namespace crashing?"})
print(result["output"])
```

---

## 🔀 LangGraph — Production Standard

LangGraph extends LangChain with **graph-based state machines**. This is the right choice for production DevOps agents because:

- **Stateful:** The agent remembers everything across many steps
- **Branching:** Take different paths based on what you find
- **Human-in-the-loop:** Pause and wait for human approval before dangerous actions
- **Streaming:** Stream intermediate results to the user in real-time

### LangGraph Agent for Incident Response

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from typing import TypedDict, Annotated
import operator

# --- State: What the agent remembers ---
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    incident_severity: str   # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    approved_for_changes: bool

# --- Tools ---
@tool
def check_pod_status(namespace: str) -> str:
    """Check status of all pods in a namespace."""
    import subprocess
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "--output=json"],
        capture_output=True, text=True
    )
    return result.stdout

@tool
def get_pod_logs(pod_name: str, namespace: str) -> str:
    """Get logs from a specific pod."""
    import subprocess
    result = subprocess.run(
        ["kubectl", "logs", pod_name, "-n", namespace, "--tail=100"],
        capture_output=True, text=True
    )
    return result.stdout

@tool
def scale_deployment(deployment: str, namespace: str, replicas: int) -> str:
    """Scale a deployment to a specific number of replicas. REQUIRES APPROVAL."""
    import subprocess
    result = subprocess.run(
        ["kubectl", "scale", "deployment", deployment,
         "-n", namespace, f"--replicas={replicas}"],
        capture_output=True, text=True
    )
    return result.stdout

llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [check_pod_status, get_pod_logs, scale_deployment]
llm_with_tools = llm.bind_tools(tools)

# --- Nodes (steps in the graph) ---
def diagnose(state: AgentState):
    """LLM decides what to do next."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def classify_severity(state: AgentState):
    """Classify how severe the incident is."""
    last_message = state["messages"][-1].content
    if "CrashLoopBackOff" in last_message or "OOMKilled" in last_message:
        return {"incident_severity": "HIGH"}
    elif "Pending" in last_message:
        return {"incident_severity": "MEDIUM"}
    return {"incident_severity": "LOW"}

def request_human_approval(state: AgentState):
    """Human-in-the-loop: pause before making changes."""
    print("\n⚠️  APPROVAL REQUIRED")
    print("The agent wants to scale a deployment. Approve? (yes/no)")
    approval = input().strip().lower()
    return {"approved_for_changes": approval == "yes"}

# --- Routing logic ---
def should_use_tools(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        # Check if the tool needs approval
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "scale_deployment":
                return "request_approval"
        return "tools"
    return END

# --- Build the graph ---
graph = StateGraph(AgentState)
graph.add_node("diagnose", diagnose)
graph.add_node("classify", classify_severity)
graph.add_node("tools", ToolNode(tools))
graph.add_node("request_approval", request_human_approval)

graph.set_entry_point("diagnose")
graph.add_conditional_edges("diagnose", should_use_tools)
graph.add_edge("tools", "classify")
graph.add_edge("classify", "diagnose")
graph.add_edge("request_approval", "diagnose")

app = graph.compile()

# --- Run ---
result = app.invoke({
    "messages": [{"role": "user", "content": "Pods in production are crashing. Investigate and fix."}],
    "incident_severity": "UNKNOWN",
    "approved_for_changes": False
})
```

---

## 👥 CrewAI — Multi-Agent Teams

CrewAI lets you define a **team** of AI agents where each has a specific role, just like a real DevOps team:

```python
from crewai import Agent, Task, Crew

# --- Define specialist agents ---
diagnostician = Agent(
    role="Infrastructure Diagnostician",
    goal="Identify the root cause of infrastructure issues by analyzing logs, metrics, and events",
    backstory="You are a senior SRE with 10 years of experience diagnosing cloud infrastructure issues.",
    tools=[check_pod_status, get_pod_logs],
    llm=llm
)

remediator = Agent(
    role="Incident Remediator",
    goal="Apply fixes to resolve infrastructure issues following approved runbooks",
    backstory="You are a platform engineer who executes precise, safe remediation steps.",
    tools=[scale_deployment],
    llm=llm
)

communicator = Agent(
    role="Incident Communicator",
    goal="Keep stakeholders informed about incident status and resolution",
    backstory="You write clear, concise incident updates for both technical and non-technical audiences.",
    tools=[],  # Only writes, no tool calls needed
    llm=llm
)

# --- Define tasks ---
diagnose_task = Task(
    description="Investigate the production pods issue and identify the root cause",
    agent=diagnostician,
    expected_output="A clear root cause analysis with supporting evidence from logs"
)

remediate_task = Task(
    description="Based on the diagnosis, apply the appropriate fix",
    agent=remediator,
    expected_output="Confirmation that the fix was applied and the issue is resolved",
    context=[diagnose_task]  # Uses output from diagnosis
)

communicate_task = Task(
    description="Write a status update for the engineering Slack channel",
    agent=communicator,
    expected_output="A clear, professional incident update message",
    context=[diagnose_task, remediate_task]
)

# --- Run the crew ---
crew = Crew(
    agents=[diagnostician, remediator, communicator],
    tasks=[diagnose_task, remediate_task, communicate_task],
    verbose=True
)
result = crew.kickoff()
```

---

## 📊 Framework Comparison

| Feature | LangChain | LangGraph | CrewAI |
|---------|----------|----------|--------|
| **Complexity** | Low | Medium-High | Medium |
| **Stateful** | No (basic) | Yes (full graph state) | Yes |
| **Multi-agent** | No | Yes (nodes can be agents) | Yes (designed for this) |
| **Human-in-loop** | Manual | Built-in checkpoint | Manual |
| **Best for** | Simple agents, learning | Production, complex workflows | Role-based agent teams |
| **Observability** | LangSmith | LangSmith (native) | LangSmith |

---

## ✅ Ready for Step 4 When You Can...

- [ ] Build a LangChain agent with 3+ tools that solves a real DevOps problem
- [ ] Build a LangGraph workflow with at least one conditional branch
- [ ] Implement a human-in-the-loop checkpoint before a destructive tool call
- [ ] Explain the difference between LangChain and LangGraph
- [ ] Explain when you'd use CrewAI vs LangGraph
