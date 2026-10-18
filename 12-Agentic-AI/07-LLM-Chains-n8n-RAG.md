---
tags: [llm, chains, n8n, rag, vector-db, agentic-ai]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🔗 Step 2 — LLM Chains, n8n, Vector DB & RAG

Before building full autonomous agents, you need to master the "AI plumbing" — how to chain LLM calls, automate workflows visually, store knowledge for AI to search, and give AI access to your own documents.

---

## 🔗 Part 1: LLM Chains

A **chain** is a sequence of steps where the output of one step feeds into the next. It's the simplest form of AI automation — no loops, no decision-making, just a pipeline.

### Simple Chain Example

```
User Problem → Prompt → LLM → Parser → Action
```

**Real DevOps example: Auto-generate a post-mortem outline from raw logs**

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Step 1: Summarize the raw logs
summarize_prompt = ChatPromptTemplate.from_template("""
You are a DevOps expert. Summarize the following error logs in 3 bullet points:
{raw_logs}
""")

# Step 2: Generate post-mortem from the summary
postmortem_prompt = ChatPromptTemplate.from_template("""
Based on this incident summary:
{summary}

Write a post-mortem with: Root Cause, Impact, Timeline, and 3 Action Items.
""")

parser = StrOutputParser()

# Chain: logs → summary → post-mortem
chain = (
    summarize_prompt
    | llm
    | parser
    | (lambda summary: {"summary": summary})  # Pass to next prompt
    | postmortem_prompt
    | llm
    | parser
)

# Run the chain
result = chain.invoke({"raw_logs": open("incident-logs.txt").read()})
print(result)
```

### When to Use Chains vs Agents

| Situation | Use |
|-----------|-----|
| Fixed, predictable steps | **Chain** (faster, cheaper, more predictable) |
| Agent needs to decide what to do next | **Agent** (more flexible, but slower/costlier) |
| Read logs → summarize → email | **Chain** |
| Debug a failing pipeline (unknown root cause) | **Agent** |

---

## 🔄 Part 2: n8n — Visual Workflow Automation

**n8n** is a self-hostable, open-source workflow automation tool. Think Zapier but you own it — and it can run Python code, call any API, and connect to your internal tools.

### Why n8n for DevOps?

- **No code required** for simple integrations
- **Self-hosted** — your data never leaves your infrastructure
- **Works with everything:** GitHub, Slack, PagerDuty, Azure, Jira, Prometheus
- **Can call LLMs** — has built-in OpenAI and LangChain nodes

### Example n8n Workflows

**Workflow 1: AI-powered PR Review**
```
Trigger: GitHub PR Opened
    ↓
Get PR diff (GitHub node)
    ↓
Send diff to OpenAI (AI node): "Review this Terraform code for security issues"
    ↓
Post LLM response as PR comment (GitHub node)
    ↓
If LLM found CRITICAL issues → Notify Slack channel
```

**Workflow 2: Alert → AI Diagnosis → Ticket**
```
Trigger: Prometheus Webhook (alert fired)
    ↓
Fetch last 100 log lines (HTTP Request node → Log Analytics API)
    ↓
Send logs to OpenAI: "What is causing this alert? Suggest fix."
    ↓
Create Jira ticket with AI diagnosis (Jira node)
    ↓
Send Slack notification with ticket link
```

### Running n8n Locally
```bash
# Docker (easiest)
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Then open: http://localhost:5678
```

---

## 📦 Part 3: Vector Databases

A **vector database** stores information as mathematical vectors (arrays of numbers) so AI can search for *meaning* rather than just keywords.

### How It Works

```
Your document: "The prod-db-01 disk full issue is fixed by compressing logs older than 3 days"
         ↓
Embedding model converts text → [0.23, -0.87, 0.45, 0.12, ...]  (1536 numbers)
         ↓
Stored in Vector DB

User asks: "How do I fix a disk full alert on a database server?"
         ↓
Question converted to vector: [0.21, -0.85, 0.44, 0.09, ...]
         ↓
Vector DB finds stored vectors that are mathematically similar (cosine similarity)
         ↓
Returns: "The prod-db-01 disk full issue is fixed by compressing logs..."
```

### Popular Vector DBs

| Database | Best For | Hosting |
|----------|---------|---------|
| **Chroma** | Local dev, small projects | Local / self-hosted |
| **Pinecone** | Production, managed service | Cloud (SaaS) |
| **Qdrant** | High performance, self-hosted | Docker / cloud |
| **Azure AI Search** | Azure-native, hybrid search | Azure managed |
| **pgvector** | Already using PostgreSQL | Self-hosted |

### Chroma Example (Local Dev)

```python
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OpenAIEmbeddings()

# Create vector store from your DevOps runbooks
vectorstore = Chroma.from_texts(
    texts=[
        "prod-db-01 disk full: compress logs older than 3 days with gzip",
        "AKS OOM: increase memory limits in deployment.yaml, check with kubectl top pod",
        "Pipeline failure: check for dependency version conflicts in package.json",
        "VM CPU spike: check for zombie processes with 'ps aux | sort -k3 -rn | head -20'",
    ],
    embedding=embeddings,
    persist_directory="./runbook-db"
)

# Search by meaning (not exact keyword)
results = vectorstore.similarity_search("database server is running out of space", k=2)
for doc in results:
    print(doc.page_content)
# Output: "prod-db-01 disk full: compress logs older than 3 days with gzip"
```

---

## 🔍 Part 4: RAG (Retrieval-Augmented Generation)

**RAG = Vector DB + LLM**. You store your own DevOps knowledge (runbooks, architecture docs, past incidents) and let the LLM answer questions based on YOUR data — not just its training data.

### Why RAG?

| Without RAG | With RAG |
|------------|---------|
| LLM only knows what it was trained on | LLM knows your runbooks, architecture, past incidents |
| LLM may give outdated answers | LLM always has your latest documentation |
| LLM can't know your internal systems | LLM knows your specific prod-db-01 configuration |
| LLM might hallucinate | LLM cites the exact document it used |

### Complete RAG Pipeline

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- 1. Setup ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)
embeddings = OpenAIEmbeddings()

# Load your pre-built runbook vector store
vectorstore = Chroma(
    persist_directory="./runbook-db",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 2. Prompt with context ---
prompt = ChatPromptTemplate.from_template("""
You are a DevOps expert. Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have a runbook for this."

Context from runbooks:
{context}

Question: {question}
""")

# --- 3. RAG Chain ---
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 4. Ask questions about YOUR infrastructure ---
answer = rag_chain.invoke("The prod-db-01 disk is at 95%, what do I do?")
print(answer)
# "According to the runbook: compress logs older than 3 days using gzip..."
```

---

## ✅ Ready for Step 3 When You Can...

- [ ] Build a 2-step LangChain chain (one LLM call feeds into another)
- [ ] Create an n8n workflow that triggers on a GitHub event and posts to Slack
- [ ] Store 10+ documents in Chroma and search them by meaning
- [ ] Build a basic RAG chain that answers questions from your own documents
- [ ] Explain the difference between a chain (fixed steps) and an agent (dynamic loop)
