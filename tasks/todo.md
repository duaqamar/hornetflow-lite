# HornetFlow implementation status

## Implemented and verified

- [x] Synthetic student fixtures, normalized record matching and explicit failure codes.
- [x] Deterministic appeal checks: missing narratives, category and conditional document checklist.
- [x] Custom MCP stdio server with three tools and a policy resource.
- [x] Real MCP client used by the UI and Bedrock orchestration loop.
- [x] Bedrock Converse discovers MCP tools and executes model requests through MCP.
- [x] Streamlit intake, checklist feedback, editable statement and reviewed text export.
- [x] Input edits invalidate statement/review/check results; identity edits clear chat.
- [x] Kiro workspace MCP configuration provided (host connection not verified).
- [x] Automated tests, Python compilation and dependency checks pass.
- [x] Launch instructions and three-minute demo script.

## Remaining cloud integrations

- [ ] Managed Bedrock Agent provisioning (the current app uses Converse).
- [ ] S3 + Bedrock Knowledge Base provisioning/sync/attachment (current policy is local MCP).
- [ ] Deploy optional Lambda adapter if choosing managed Agent architecture.
- [ ] Verify custom MCP connection inside Kiro; automated protocol connection is verified separately.

## Team's remaining demo work

- [ ] Review visually on the team's presentation browser; no browser automation surface was available in this session.
- [ ] Rehearse three-minute script and capture screenshots.
- [ ] Verify each teammate's own AWS credentials and local absolute MCP configuration paths.

## Future scope

- [ ] Official policy review and authenticated university integration.
- [ ] Real uploads, durable status tracking, PDF output or enrollment workflow.

These remaining items are not represented as completed features in the UI or README.
