"""
Prompt for generating detailed content about MCP servers.
"""

CONTENT_GENERATION_PROMPT = """
You are an expert AI assistant helping to generate detailed information about an MCP (Model Context Protocol) server for a user's project.

# Project Context
User Prompt: {prompt}

# Project Files
{files}

# Server Information
Name: {server_name}
Description: {server_description}
Content: {server_content}

# Task
Generate detailed, helpful information about this MCP server that would be valuable for the user's project.
Include:
1. A clear title for the server
2. GitHub URL (if available or can be inferred)
3. Project URL (if available or can be inferred)
4. CLI command to install or configure the server
5. A concise description (1-2 sentences)
6. Detailed markdown content explaining:
   - What the server does
   - Key features and capabilities
   - How it would be useful for this specific project
   - Basic configuration and usage instructions

Format your response exactly as follows:
TITLE: [server title]
GITHUB_URL: [github url or leave blank if unknown]
PROJECT_URL: [project url or leave blank if unknown]
CLI_COMMAND: [installation or setup command]
DESCRIPTION: [brief description]
CONTENT:
[detailed markdown content]
"""
