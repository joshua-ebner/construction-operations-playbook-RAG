# Live Demo Script (5 minutes)

## Setup (before panel arrives)

1. Open deployed URL (or `streamlit run app.py`)
2. Confirm example questions load
3. Have Portkey env ready if using interview keys

## Pitch flow

**Opening (30 sec):**
> "Floor supervisors waste time hunting through safety binders, maintenance manuals, and QC standards. We built an assistant that routes each question to the right documentation and returns a cited, actionable answer — not a generic chatbot response."

**Demo 1 — Safety (90 sec):**
- Click: *"What is the lockout/tagout procedure for CNC Line 3?"*
- Point out: **Routing badge** → Safety Procedures
- Point out: **Steps** + **citations** from LOTO-PROC-001

**Demo 2 — Maintenance (60 sec):**
- Click: *"How do I troubleshoot a hydraulic pressure drop on CNC Line 3?"*
- Point out: routes to Maintenance, not Safety

**Demo 3 — Edge case (90 sec):**
- Click: *"Can I clear a jam on Line 3 during active QC sampling?"*
- Point out: routes to Quality, explains production hold rules
- Say: "This is where routing matters — wrong corpus = wrong answer."

**Close (30 sec):**
> "In production: ingest client PDFs/SharePoint, add SSO, audit logs, and feedback loop. This pilot proves the core workflow in under 2 hours."

## Likely stakeholder questions + answers

| Question | Answer |
|----------|--------|
| Why route before retrieve? | Different corpora are governed separately (EHS vs Maintenance vs QE). Routing prevents cross-contamination and wrong-policy answers. |
| Why synthetic data? | Not provided by client. Structured Markdown mirrors SOP format; production swaps in their docs. |
| Hallucination risk? | Answers constrained to retrieved chunks; citations shown. Out-of-scope → system says what's missing. |
| Why Streamlit? | Speed under constraints. Production = branded portal + SSO. |
| What's next? | PDF ingestion, human feedback, analytics on top questions, CMMS integration. |
