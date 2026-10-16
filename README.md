# HornetFlow Lite

A financial aid appeal workspace built for the Sacramento State hackathon. Gather student details, check missing requirements, review a personal statement, and download a demo appeal packet.

**Working implementation:** Streamlit UI + AWS Bedrock Converse chat + a custom MCP server. All records and policies are synthetic. The app does not submit appeals or decide aid eligibility.

## Run

Dependencies are already installed in this checkout's `.venv` (Python 3.12).

```sh
./scripts/run.sh
```

Open http://127.0.0.1:8501. If that port is already in use, the demo may already be running; use `./scripts/run.sh --server.port 8502` for another instance.

For a new checkout, use Python 3.11 or newer:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./scripts/run.sh
```

## Try the demo

1. Click **Load fictional demo student**: Alex Rivera, ID `1001001`, Fall 2026.
2. Click **Check my appeal packet**. The illness appeal is missing a supporting document.
3. Check **I have a supporting document available** and check the packet again.
4. Click **Create my statement draft**, edit it, confirm review, and download.
5. Ask the guide: “Use my current form data to check what is missing.” Expand the tools panel to see MCP calls.

Inputs changing will clear the previous validation, statement and confirmation. Changing student identity also clears the chat. The draft is assembled from the form's exact facts; AI chat provides guidance and can suggest wording but does not modify form fields.

**Documents are self-reported checklist items.** No files are uploaded or authenticated. Incomplete downloads are explicitly marked drafts. The UI can perform MCP checks and export without AWS chat enabled.

## Custom MCP server

`mcp_server.py` exposes:

- `lookup_student` — match fictional student records.
- `check_appeal` — deterministic completeness checks.
- `get_appeal_policy` — retrieve the synthetic policy.
- `hornetflow://policy` — policy resource.

The app calls these tools using a real stdio MCP client. Bedrock discovers their schemas and routes tool requests through MCP. No public MCP network endpoint is opened.

Kiro workspace configuration: [.kiro/settings/mcp.json](.kiro/settings/mcp.json). Paths point to this checkout; teammates must adjust them for theirs. Enable/reconnect the server in Kiro to use it there. See [MCP setup and architecture](docs/mcp.md).

## AWS credentials

Use **Get AWS CLI credentials** in Workshop Studio. Enter each value without quotes or `export` prefixes:

```sh
python3 scripts/configure-aws.py
source ./aws-env.sh
aws sts get-caller-identity --profile hackathon --region us-east-1
```

Credentials stay in `~/.aws/credentials`, outside this repository. Refresh the three values together when the workshop session expires. The custom MCP server itself does not require AWS credentials.

Chat defaults to `us.amazon.nova-lite-v1:0` in `us-east-1` with profile `hackathon`. Change the model in the sidebar or set `BEDROCK_MODEL_ID`. A successful model listing does not guarantee invocation permission; chat shows failures while preserving the form.

## Verification

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q app.py backend mcp_server.py
.venv/bin/python -m pip check
```

The tests cover business rules, export checks, a real MCP subprocess, the Bedrock-to-MCP orchestration with a stubbed model, and the actual Streamlit flow. Live AWS smoke tests are separate; see [test results](docs/test-results.md).

## Implementation boundaries

This iteration uses a Bedrock Converse tool-calling agent loop. A managed Bedrock Agent, S3 Knowledge Base, deployed Lambda, authentication, actual uploads, PDF output, submission and persistent request tracking are not configured. `backend/lambda_handler.py` is an optional adapter for a future managed Agent action group; it is not the running MCP path.

## Team handoff

| Person | Next ownership |
|---|---|
| 1 | AWS model access and agent integration |
| 2 | Validation rules and Lambda deployment if needed |
| 3 | UI polish and packet format |
| 4 | Official-policy replacement, Knowledge Base integration and demo rehearsal |

[Specification](tasks/spec.md) · [One-hour plan](tasks/plan.md) · [Build status](tasks/todo.md) · [Demo script](docs/demo.md)




**Must-have (MVP, about 80% of the score)**

1. Two complete workflows (Workflow completeness, 30%)

Enrollment verification: asks for the ID → looks up the student → asks the purpose (e.g. landlord) → checks eligibility → generates the letter with a reference number.
SAP appeal: asks for the ID → explains why aid was suspended (GPA, completion rate) → asks what happened → drafts the personal statement → student approves it → packages the appeal with a checklist of required items.

2. Rule validation (Accuracy & validation, 25%)

Not enrolled → no letter
Account hold → blocked, with “contact the Registrar”
Aid not suspended → no appeal needed
GPA below 2.0 or completion below 67% → flagged
Invalid student ID → handled politely

The rules live in the Lambda, so the AI can’t make them up.

3. Guided conversation (Student experience, 20%)

One question at a time, greets the student by name, friendly tone.
Explains why a request was denied and what to do next.

4. Knowledge Base use (Architecture, 15%)

Mid-workflow, the agent pulls policy from the KB and cites it. Example: “Per SAP policy, you need a 2.0 GPA…”

5. Guardrails

Never shows another student’s data.
Stays on topic: politely redirects “write my essay” or “what’s the weather.”
Nice-to-have (only after both workflows work end to end)
Session status tracking: “What’s the status of HF-1234?” (a bonus on the sheet)
Spanish support: the instructions say “respond in the student’s language.” It costs almost nothing and is a bonus on the sheet.
Third workflow (e.g. change of major)
PDF output saved to S3
Demo features (Creativity & impact, 10%)
A story at the start: “Students wait 5–7 days for this letter. HornetFlow does it in 60 seconds.”
Show one success and one rejection (ID 1001 vs 1005). The rejection is what proves the validation works.
An architecture diagram slide (it’s already in the README).
