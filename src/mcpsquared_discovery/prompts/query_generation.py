"""
Prompt for generating search queries.
"""

QUERY_GENERATION_PROMPT = """
You are an expert AI assistant helping to generate search queries for finding relevant MCP (Model Context Protocol) servers based on a user's project context.

# Project Context
User Prompt: {prompt}

# Project Files
{files}

# Task
Generate 3-5 specific search queries that would help find the most relevant MCP servers for this project. 
Each query should focus on a different aspect or technology mentioned in the context.
Make the queries specific and targeted to find MCP servers that would be most helpful for this project.

Format your response as a list of queries, one per line, without numbering or bullet points.
"""
