"""
Prompt for selecting the best search results.
"""

RESULT_SELECTION_PROMPT = """
You are an expert AI assistant helping to select the most relevant MCP (Model Context Protocol) servers for a user's project.

# Project Context
User Prompt: {prompt}

# Project Files
{files}

# MCP Resources
{mcp_resources}

# Search Results
{search_results}

# Task
Analyze the available information and provide 2-4 of the most relevant MCP servers that would be most helpful for this project.

Consider:
1. How well the server matches the project's technologies and requirements
2. The quality and completeness of the server's documentation
3. Whether the server provides unique functionality not covered by other selected servers
4. The server's availability and compatibility based on the MCP resources

Return your response as a JSON array of server objects. Each server object should have this structure:
{{
  "title": "Server name",
  "description": "1-2 sentence description",
  "github_url": "GitHub URL if available, otherwise empty string",
  "cli_command": "Installation command or comment with instructions",
  "content": "Explanation of relevance and key features"
}}

For direct matches, use the existing information. For suggestions from MCP resources, create appropriate server objects with the same structure.

IMPORTANT: Return JSON only, no other text. Ensure the JSON is valid and follows the schema above.
"""
