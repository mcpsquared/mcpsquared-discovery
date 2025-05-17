"""
Prompt for selecting the best search results.
"""

RESULT_SELECTION_PROMPT = """
You are an expert AI assistant helping to select the most relevant MCP (Model Context Protocol) servers for a user's project.

# Project Context
User Prompt: {prompt}

# Project Files
{files}

# Search Results
{search_results}

# Task
Analyze the search results and select the 2-4 most relevant MCP servers that would be most helpful for this project.
Consider:
1. How well the server matches the project's technologies and requirements
2. The quality and completeness of the server's documentation
3. Whether the server provides unique functionality not covered by other selected servers

Format your response as a list of selected results, using the format:
Result X: Brief explanation of why this is relevant

Only include the result numbers for servers you're selecting, not all of them.
"""
