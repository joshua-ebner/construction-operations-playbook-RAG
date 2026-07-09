# Prototype Brief — Apex Manufacturing Supervisor Assistant

## Problem

Floor supervisors need fast, accurate answers from safety, maintenance, and quality documentation — but currently must search binders, SharePoint folders, or call specialists, causing downtime and inconsistency.

## Target User

Plant floor **supervisor** at a discrete manufacturing facility (Building B, CNC Line 3).

## Assumptions

* Internal prototype, not production software.
* Synthetic Markdown SOPs stand in for client PDFs/SharePoint.
* Streamlit UI for speed; Railway for deploy.
* Portkey (Claude Sonnet 4.5) at interview; OpenAI locally for prep.

## Core Workflow

1. Supervisor enters an operational question.
2. System **routes** to safety, maintenance, or quality corpus.
3. System **retrieves** relevant chunks and **generates** a grounded answer.
4. Supervisor sees routing decision, structured answer, and citations.

## MVP Scope

* 9 synthetic Markdown docs (3 corpora × 3 docs)
* Chunk → embed → ChromaDB (per-corpus collections)
* LLM router (structured output)
* RAG answer with summary, steps, warnings, citations
* Streamlit decision-support UI
* Railway deploy config

## Out of Scope

* Authentication / SSO
* Production PDF ingestion
* React frontend
* Audit logs / permissions

## Success Criteria

* Demo shows visible routing + cited answers on 3+ scripted questions
* Edge-case question demonstrates routing judgment
* Deployable URL on Railway (optional polish phase)

## Build Status

- [x] Dummy Markdown data (`data/safety`, `data/maintenance`, `data/quality`)
- [ ] `src/config.py`, `src/models.py`, `src/ingest.py`, `src/router.py`, `src/rag.py`
- [ ] `app.py` (Streamlit UI)
- [ ] `railway.toml`, `.streamlit/config.toml`
- [ ] Smoke test

## Demo Questions

1. "What is the lockout/tagout procedure for CNC Line 3?" → safety
2. "How do I troubleshoot a hydraulic pressure drop on CNC Line 3?" → maintenance
3. "What are the acceptance criteria for SPC sampling on Line 3?" → quality
4. "Can I clear a jam on Line 3 during active QC sampling?" → edge case

## Env Vars

```bash
# Local prep
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Interview (Portkey)
USE_PORTKEY=true
PORTKEY_API_KEY=...
PORTKEY_BASE_URL=https://portkeygateway.perficient.com/v1
LLM_PROVIDER=openai
LLM_MODEL=@aws-bedrock-use2/us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

## Run Locally

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Railway

```bash
# railway.toml start command
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
