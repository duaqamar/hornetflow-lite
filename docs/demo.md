# Three-minute demo

## Before presenting

Run `./scripts/run.sh`, visit http://127.0.0.1:8501 and load the fictional demo student. Test one chat response using current Workshop Studio credentials. If AWS is unavailable, turn off AI in the sidebar and demonstrate the actual MCP-backed checklist/export; disclose the unavailable cloud chat.

## Script

**0:00–0:25 — Problem.** Students often need help understanding appeal requirements and assembling their own narrative. HornetFlow turns this into a guided workspace with visible missing items.

**0:25–1:10 — Missing document.** Load Alex Rivera. Click Check my appeal packet. Show that the illness category requires a self-reported supporting document. Ask chat to check the current form and show the MCP tool activity if AWS is available.

**1:10–1:50 — Complete and review.** Mark supporting document available, check again, create a statement, edit a sentence, confirm review and download. Open the packet and point out the demo labeling and checklist.

**1:50–2:15 — Validation.** Change student ID to an unknown ID. The previous statement/download disappears. Run the check: no matched student record is exposed. Do not describe this lookup as authentication.

**2:15–3:00 — Architecture and limits.** Streamlit calls the custom MCP server. Bedrock Converse uses discovered MCP tools. The same Python rules support an optional Lambda adapter. Policy and records are currently local and synthetic; managed Bedrock Agent, Knowledge Base, real uploads and official submission are future work.

Do not claim the app approves aid, authenticates evidence, retrieves official policy, or has measured processing-time savings.
