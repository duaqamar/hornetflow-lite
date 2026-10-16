# HornetFlow Lite specification

## Implemented architecture revision

The user requested a custom MCP server when authorizing implementation. The running slice uses Streamlit → Bedrock Converse → a local stdio MCP server for tools and policy. Managed Bedrock Agent/Knowledge Base deployment remains pending. Shared deterministic validation is implemented in `backend/validation.py`; an optional Lambda adapter is present but not deployed. The student-facing intake is a structured form with conversational guidance; chat cannot silently edit form data. `check_appeal` requires `full_name` as well as student ID/term to match records. The implemented interface is `chat(messages, fields, model_id)` with per-browser Streamlit message history, rather than an external session-ID API.

## Objective
Build a student-facing financial aid appeal assistant for a four-person, one-hour hackathon. Guide a student through an appeal, check a mock record and document checklist, draft a personal statement for review, and export a submission-ready demo packet.

Scope assumption: the README's financial aid focus takes priority over the earlier enrollment-first proposal. File management means document collection and completeness tracking for one appeal, not an administrative document management system.

## User journey
1. Student selects “Financial aid appeal” and supplies student ID, name and term.
2. Backend checks a synthetic student record; agent explains demo policy.
3. Agent asks for circumstances, academic impact and recovery plan without inventing details.
4. Student marks supporting documents available. For the core demo, document availability is self-reported; no document-content verification is claimed.
5. Backend computes missing requirements and packet readiness.
6. Agent drafts a personal statement using student-provided facts; student reviews and confirms it.
7. App exports a text packet containing the reviewed statement, mock student details, checklist and remaining steps.

A complete packet is ready for review, not an approved appeal. Draft downloads may be available with explicit missing-item labels; only the deterministic checker can label a packet complete.

## Technology and architecture
- Python 3.11+ for implementation; Streamlit web UI; boto3 AWS adapter.
- Bedrock Agent for guided conversation, Lambda action group for deterministic student lookup and checklist checks.
- S3 demo-policy document attached through a Bedrock Knowledge Base.
- Mock records in JSON packaged with Lambda; no database setup required.
- Text download for the first hour; PDF, real uploads and persistent tracking are stretch work.
- Resolve compatible dependency versions during setup and record them in requirements.txt; do not assume proposed dependencies are already installed.

Flow: Streamlit → Bedrock Agent → Lambda → mock records; agent retrieves guidance from KB backed by S3. App assembles export from structured checked fields and a student-reviewed statement.

## Shared interfaces
`lookup_student(student_id, full_name, term)` returns `matched`, `reason_code`, and `student` (null unless matched).

`check_appeal(student_id, term, circumstances, academic_impact, recovery_plan, documents_available)` returns `complete`, `missing_fields`, `missing_documents`, and `reason_codes`. Student name/record matching must also succeed before completeness is true.

Demo document rules: a personal statement and recovery plan are always required; illness-related appeals require a supporting-document checklist item. This is a synthetic workshop policy, not official university guidance. Check reported presence only; never claim authenticity checks.

UI adapter: `chat(message, session_id)` returns `reply`, `session_id`, and optional structured `appeal_state`. The backend owns completeness. Never parse model prose to decide readiness. Preserve structured tool results through action trace handling or the supported return-control flow; prove this integration early.

Statement changes or edited inputs clear prior review confirmation. A changed student ID clears prior student data and packet state.

## Proposed project structure
```text
app.py                         Streamlit chat, review, checklist and download
backend/agent_client.py         Bedrock invocation and structured state adapter
backend/lambda_handler.py       Student lookup and appeal validation actions
backend/packet.py               Deterministic packet assembly
backend/__init__.py             Package marker
data/students.json             Synthetic student fixtures
data/demo-policy.md            Synthetic appeal policy
infra/agent-instructions.md     Agent instructions and setup notes
infra/resources.example.json   Non-secret resource configuration template
requirements.txt               Tested dependencies
tests/test_validation.py       Validation tests
tests/test_packet.py           Export tests
docs/demo.md                   Three-minute presentation script
tasks/                        Spec, implementation plan and checklist
```
Paths above are planned deliverables, not existing application files.

## Commands after implementation
```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
source ./aws-env.sh
aws sts get-caller-identity --profile hackathon --region us-east-1
python3 -m streamlit run app.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q app.py backend
```
No frontend build step is required. These application commands become runnable after their corresponding files are implemented.

## Code style
Use snake_case functions, explicit dictionaries for small tool results, and short functions. Keep AWS transport separate from validation so rules can be tested without AWS.

```python
def missing_fields(values: dict[str, str]) -> list[str]:
    required = ("circumstances", "academic_impact", "recovery_plan")
    return [name for name in required if not values.get(name, "").strip()]
```

## Testing strategy
Use standard-library unittest. Cover valid/unknown students, name and term mismatches, missing narrative fields, missing conditional documents, complete intake, clearing stale state and packet contents. Manually exercise the real Bedrock → action → UI path and a request to bypass requirements. Record actual results; local unit tests alone do not demonstrate cloud integration.

## Boundaries
- Always: use synthetic records, validate in Python, label demo policies, preserve session isolation, keep credentials outside the repo, disclose incomplete integrations.
- Ask first: changing the primary workflow, introducing real student records, actually submitting an appeal, or adding persistent document storage beyond this plan.
- Never: invent student circumstances, promise approval, claim checklist checks authenticate files, commit credentials or export another session's data.

## Success criteria
- A fresh session completes one financial aid appeal conversation and downloads a reviewed demo packet.
- Missing requirements produce specific next steps and cannot be labeled complete.
- Unknown/mismatched students do not receive matched record details.
- Student can edit the statement before confirming it for export.
- At least one real Bedrock action call works; policy retrieval is demonstrated or clearly marked incomplete.
- Team can run a repeatable three-minute demo and explain limitations.

## Outside the core hour
Enrollment letters, PDF output, real document uploads/OCR, email delivery, authentication, real university integration, multilingual support, database-backed history and frontend cloud deployment.
