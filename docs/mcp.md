# Custom HornetFlow MCP server

This is a real stdio MCP server built with the official Python SDK (v1 maintenance API, pinned in requirements). It does not open a network port. Hosts launch it as a subprocess; stdout carries MCP messages only.

## Tools

- `lookup_student(student_id, full_name, term)`: matches synthetic records; mismatches return no student data.
- `check_appeal(student_id, full_name, term, circumstances, academic_impact, recovery_plan, category, documents_available)`: checks deterministic packet rules, never aid eligibility.
- `get_appeal_policy()`: reads the labeled synthetic policy.

Resource: `hornetflow://policy`.

The server is stateless. Each tool receives all needed input. It exposes no arbitrary file paths, shell execution, uploads, credentials, or real student records.

## Start

```sh
.venv/bin/python mcp_server.py
```

It waits for a client's protocol handshake; no startup banner is expected on stdout.

## Kiro

A workspace configuration is included at `.kiro/settings/mcp.json`. Open this folder in Kiro and enable/reconnect the `hornetflow` MCP server through its MCP interface. Configuration is provided; host discovery/connection still needs to happen in Kiro.

If a teammate clones the project elsewhere, replace the absolute paths to `.venv/bin/python` and `mcp_server.py` with their checkout paths. No AWS credentials are needed by this MCP server.

For another MCP host, use the same command and args in its `mcpServers` configuration. Do not add credentials to the config.

## App integration

The Streamlit check button calls `check_appeal` through a real MCP stdio client. Bedrock Converse receives tool schemas discovered from this server, then routes model tool requests through MCP. The server returns structured results; the form's own completeness check governs downloads and status. Chat cannot silently edit form fields.

This is a custom Bedrock Converse orchestration loop, not a deployed managed Bedrock Agent. S3/Knowledge Base retrieval is not configured; policy is served locally by MCP. An optional Lambda action adapter is included but not deployed.

## Verify

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The suite opens real MCP subprocesses, performs initialize/list-tools/call-tool/resource discovery, and checks invalid arguments. AWS smoke testing is separate and requires current credentials.

SDK reference: https://github.com/modelcontextprotocol/python-sdk/tree/v1.x
