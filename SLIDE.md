# One-Slide Pitch — Copy into Google Slides / PowerPoint

---

## Apex Manufacturing — Supervisor Knowledge Assistant

**Problem:** Floor supervisors lose 15–30 min/shift searching safety, maintenance, and QC documentation — causing downtime, inconsistent decisions, and safety risk.

**Solution:** AI assistant that **routes** each question to the correct document class, **retrieves** relevant procedures, and returns **cited, actionable answers**.

```
Supervisor Question → Route (Safety | Maintenance | QC) → Retrieve → Cited Answer
```

**Demo highlights:**
- Lockout/tagout procedure → routes to Safety, cites LOTO-PROC-001
- Hydraulic troubleshooting → routes to Maintenance
- Jam during QC sampling → routes to Quality (edge-case judgment)

**Business value:**
- ↓ Supervisor downtime searching binders/SharePoint
- ↓ Safety incidents from outdated tribal knowledge
- ↑ Consistent, auditable floor decisions

**Pilot today · Production path:** PDF/SharePoint ingestion · SSO · audit logs · CMMS integration

**[QR code or URL to live demo]**

---

### Speaker notes (not on slide)

- Built in 2 hours with Python, embeddings, ChromaDB, Streamlit
- Deliberately skipped: auth, production PDF parsing, full UI polish
- Tradeoff: speed + core workflow proof over enterprise hardening
