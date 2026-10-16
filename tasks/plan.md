# HornetFlow Lite: one-hour build plan

Source of truth: [spec.md](spec.md). Primary workflow: financial aid appeal intake → completeness check → reviewed statement → downloadable demo packet.

## Current implementation

Core local workflow and custom MCP integration are implemented. The running cloud chat uses Bedrock Converse rather than a managed Bedrock Agent. Policy comes from the local MCP server rather than an S3 Knowledge Base. See `tasks/todo.md` for verified work and remaining integrations. The original timing/ownership guidance below remains a team handoff plan.

## Team ownership

| Person | Deliverable | Files |
|---|---|---|
| 1 — AWS / integration lead | Agent, action configuration, session adapter; cloud integration | `backend/agent_client.py`, `infra/agent-instructions.md`, `infra/resources.example.json` |
| 2 — backend | Mock records, student lookup, deterministic appeal checks | `backend/lambda_handler.py`, `backend/__init__.py`, `data/students.json`, `tests/test_validation.py` |
| 3 — frontend | Chat, progress checklist, statement editor, export | `app.py`, `backend/packet.py`, `requirements.txt`, `tests/test_packet.py` |
| 4 — policy / QA / pitch | Demo policy, S3/KB, test evidence, demo script | `data/demo-policy.md`, `docs/test-results.md`, `docs/demo.md` |

Each person owns their files. Person 1 owns integration; Person 3 coordinates dependency changes. Teammates share resource IDs, not credentials. Every person uses their own temporary credentials locally.

## Timeline

| Minutes | Parallel work | Required outcome |
|---|---|---|
| 0–5 | Everyone reads spec; agree interfaces and demo fixtures. Person 1 checks model access; Person 4 starts KB | Shared contract, reachable model, owners assigned |
| 5–20 | P1 agent + adapter; P2 validator + tests; P3 UI using stub result; P4 policy + KB | Components run independently |
| 20–30 | P1/P2 connect agent actions; P1/P3 pass structured state to UI; P4 attaches KB | One real action result reaches UI |
| 30–40 | Complete conversation, editable statement, packet download | One successful end-to-end appeal |
| 40–50 | Everyone tests missing data, mismatch, bypass requests and state resets | Rejections and missing-item guidance work |
| 50–60 | Freeze features; fix blockers; capture screenshots and rehearse | Repeatable three-minute demonstration |

## Dependency order and checkpoints

Agree contracts → implement lookup/checker → integrate agent action → deliver checked UI state → review statement → export packet. Policy creation and UI stub development run in parallel. Letter/enrollment features wait until the appeal path works.

Minute 20: validator passes local tests; UI renders; model responds. Minute 30: real action reaches UI. Minute 40: packet downloads. Minute 50: negative cases and state isolation pass.

## Risks and cutoffs

- No model access by minute 10: select another permitted model; avoid naming an unverified model in code or docs.
- KB blocked by minute 20: use demo policy in agent instructions temporarily and disclose missing retrieval.
- Structured result integration blocked by minute 30: use explicit UI intake fields and direct validation for the working slice; clearly disclose the incomplete agent action integration.
- UI blocked: demonstrate the agent in Bedrock test console and export separately; describe this as a partial demo.
- Do not spend core time on vector-store troubleshooting, PDF layout, deployment or real uploads. These are stretch work.

Fallback paths do not satisfy the full intended architecture; show their actual status honestly.

## Three-minute pitch

- 0:00–0:25: Students struggle to understand appeal requirements and assemble complete submissions.
- 0:25–1:45: Chat through a mock appeal, show a missing item, complete the checklist, review/edit the statement, download the packet.
- 1:45–2:15: Show an unknown student or bypass request failing safely.
- 2:15–3:00: Explain Bedrock + actions + KB, what is real in the demo, and production next steps.

Prioritize the rubric: completeness (30%), validation (25%), student experience (20%), architecture (15%), impact (10%). Do not claim measured time savings without measurements.
