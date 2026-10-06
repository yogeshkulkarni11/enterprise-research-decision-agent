# Enterprise Research & Decision Agent

An intermediate-to-advanced **Agentic AI + RAG** portfolio project that combines enterprise policy retrieval, structured business data, transparent risk scoring and evidence-backed decision making.

## Business scenario

A procurement or architecture team asks:

> "Which Cloud vendor should we select, considering cost, security, resilience, regulatory posture and concentration risk?"

The system does not simply ask an LLM to answer. It coordinates specialized capabilities:

```text
Business Request
      |
      v
Orchestrator
   /       \
  v         v
Research   Data
  |         |
  v         v
RAG      SQL/Data
   \       /
    v     v
    Risk Agent
        |
        v
   Decision Agent
        |
        v
Evidence-backed Recommendation
```

## Agents

| Agent | Role |
|---|---|
| Orchestrator | Coordinates the decision workflow |
| Research/RAG Agent | Retrieves enterprise policy evidence |
| Data Agent | Reads structured vendor data through SQL |
| Risk Agent | Calculates a transparent risk score and band |
| Decision Agent | Ranks vendors and produces recommendation |
| Response Layer | Presents rationale, alternatives and evidence |

## Why this is Agentic AI

The workflow uses multiple specialized reasoning responsibilities, tools/data access, shared intermediate results and a decision stage. This is materially different from a single prompt-to-LLM chatbot.

## RAG

Synthetic enterprise policies are chunked and indexed in ChromaDB using Sentence Transformers. The Research component retrieves relevant evidence for the decision context and returns source names with the recommendation.

## Structured data

The sample vendor dataset contains:

- annual cost
- security score
- financial score
- resilience score
- regulatory score
- concentration percentage
- implementation duration

SQLite is initialized automatically from `data/vendors.csv`.

## Risk model

The demo intentionally uses an explainable scoring formula rather than opaque model output:

```text
average_control_score = average(security, financial, resilience, regulatory)
control_risk = (100 - average_control_score) * 0.65
concentration_risk = concentration_pct * 0.35
risk_score = control_risk + concentration_risk
```

Bands:

- `< 15` → Low
- `15–24.99` → Medium
- `>= 25` → High

These thresholds are demonstration values, not production risk policy.

## Repository structure

```text
enterprise-research-decision-agent/
├── data/
│   ├── documents/
│   │   ├── vendor-policy.md
│   │   ├── security-policy.md
│   │   └── procurement-policy.md
│   └── vendors.csv
├── docs/
│   ├── architecture.md
│   └── interview_questions.md
├── src/
│   ├── __init__.py
│   ├── agent.py
│   └── main.py
├── tests/
│   └── test_agent.py
├── .env.example
├── .gitignore
├── .github/workflows/tests.yml
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python -m src.main
```

The demo can run without an LLM API key because the decision logic is deterministic. The RAG retrieval uses local embeddings.

## Example output

```text
Recommended vendor: AlphaCloud
- Selected AlphaCloud with risk score ...
- Security score: ...; resilience score: ...; regulatory score: ...
- Annual cost: $1.20M and concentration: 18%

Evidence:
- security-policy.md: ...
- vendor-policy.md: ...
```

## Production architecture on Azure

| Demo component | Azure production equivalent |
|---|---|
| Local embeddings | Azure OpenAI / managed embedding model |
| ChromaDB | Azure AI Search |
| SQLite | Azure SQL / Microsoft Fabric |
| Markdown documents | ADLS Gen2 / Blob Storage |
| Agent runtime | Azure AI Foundry |
| Secrets | Azure Key Vault |
| Governance | Microsoft Purview |
| Monitoring | Application Insights / Azure Monitor |

## Production improvements

1. Add Azure AI Foundry Agent Service or an equivalent managed agent runtime.
2. Add human approval for high-risk decisions.
3. Add identity-based access control and document-level authorization.
4. Add RAG evaluation for retrieval relevance and groundedness.
5. Add prompt/version management and tracing.
6. Add model fallback and retry policies.
7. Store decisions and evidence for auditability.
8. Add policy versioning and effective dates.
9. Replace the demonstration risk formula with approved enterprise risk models.
10. Add data-quality checks and lineage for structured inputs.

## Interview explanation

**One-line explanation:**

> "I built a multi-agent enterprise decision system where a Research Agent retrieves policy evidence, a Data Agent queries structured business data, a Risk Agent calculates transparent risk, and a Decision Agent combines both to produce an evidence-backed recommendation."

See [`docs/architecture.md`](docs/architecture.md) and [`docs/interview_questions.md`](docs/interview_questions.md) for the architecture and interview preparation.

## Disclaimer

All documents and business data are synthetic and created only for learning, portfolio and demonstration purposes.
