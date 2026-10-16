# Verification results — October 16, 2026

## Automated checks

- **16 tests passed** with `.venv/bin/python -m unittest discover -s tests -v`.
- Python compilation passed for `app.py`, `backend/` and `mcp_server.py`.
- `pip check` reported no broken requirements.
- HTTP health endpoint `http://127.0.0.1:8501/_stcore/health` returned `ok`.

Coverage includes valid/unknown students, name/term mismatch, missing narrative fields, illness supporting-document requirement, category validation, whitespace normalization, export review gating, real stdio MCP handshake/discovery/calls/resources, invalid MCP arguments, Bedrock-to-MCP routing with a stubbed model, and Streamlit's actual demo/review/input-reset flow.

Streamlit AppTest executed the app, loaded fictional records, observed the missing-document warning, completed the checklist, generated/edited/reviewed a statement, and changed identity to verify stale statement/check/chat state cleared. This is runtime UI testing, not a visual accessibility audit or real-browser download test.

## Live AWS smoke checks

Using the `hackathon` profile in `us-east-1` with model `us.amazon.nova-lite-v1:0`:

1. Policy request produced a real MCP `get_appeal_policy` call and a Bedrock reply. That first reply unnecessarily requested student details; the prompt was refined so general policy questions do not require lookup.
2. A real Bedrock request using Alex Rivera's illness appeal form invoked MCP `check_appeal`, returned success, and correctly identified the missing supporting document.

No managed Agent, Knowledge Base, Lambda deployment or Kiro-host connection was tested. No appeal was submitted. Temporary credentials and future model access may expire/change.

## Visual verification limitation

Computer-use tooling reported no available browser. Visual layout, mobile breakpoints, keyboard navigation and actual browser download behavior remain for team review. No screenshot or visual accessibility pass is claimed.
