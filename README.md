# MCP Squared Discovery Service

FastAPI based service to recommend MCP Servers and tools for use by the MCP Squared discovery tool.

Accepts a prompt and file attachments.

Returns a JSON response with the following fields:
- `mcp_servers` - a list of MCP Servers that are recommended for the prompt
- `tools` - a list of tools that are recommended for the prompt
- `reasoning` - a list of reasoning steps that were used to determine the recommendations

## Running the service

Deployment via Docker on K8s using Porter.


