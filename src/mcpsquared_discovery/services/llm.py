"""
Service for LLM interactions using LangChain.
"""

import logging
from typing import Dict, List
from pathlib import Path
import json

from langchain_community.chat_models import ChatLiteLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from mcpsquared_discovery.core.config import settings
from mcpsquared_discovery.models.schemas import MCPServer, Source
from mcpsquared_discovery.prompts.content_generation import CONTENT_GENERATION_PROMPT
from mcpsquared_discovery.prompts.query_generation import QUERY_GENERATION_PROMPT
from mcpsquared_discovery.prompts.result_selection import RESULT_SELECTION_PROMPT
from mcpsquared_discovery.core.logging import log_llm_call

logger = logging.getLogger(__name__)

def load_mcp_resources() -> str:
    """
    Load MCP resources markdown file.

    Returns:
        Content of the MCP resources markdown file
    """
    resources_path = Path(__file__).parent.parent / "data" / "mcp_resources.md"
    with open(resources_path) as f:
        return f.read()


def get_llm():
    """
    Initialize and return the LLM client.

    Returns:
        Configured LangChain ChatLiteLLM instance
    """
    # Configure default headers for OpenRouter
    default_headers = {
        "HTTP-Referer": "https://mcpsquared-discovery.ai",
        "X-Title": "MCP Squared Discovery Service"
    }

    # Log the call to be made
    logger.debug("Making call to OpenRouter with model: %s", settings.LLM_MODEL)
    logger.debug("OpenRouter API Key: %s", settings.OPENROUTER_API_KEY)
    logger.debug("OpenRouter API Base: %s", settings.OPENROUTER_BASE_URL)

    model_kwargs = {
        "headers": default_headers,
    }

    return ChatLiteLLM(
        model="openrouter/anthropic/claude-3.5-sonnet",
        temperature=0.7,  # Add to settings if you want to make configurable
        api_base=settings.OPENROUTER_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
        model_kwargs=model_kwargs,
        max_retries=2,
    )


async def generate_search_queries(prompt: str, context: Dict) -> List[str]:
    """
    Generate search queries based on project context using LLM.

    Args:
        prompt: User prompt
        context: Project context dictionary

    Returns:
        List of generated search queries
    """
    logger.debug("Generating search queries from context")
    llm = get_llm()

    # Add MCP resources to context if not already present
    if "mcp_resources" not in context:
        context["mcp_resources"] = load_mcp_resources()

    # Prepare context for the prompt
    prompt_context = {
        "prompt": prompt,
        "files": "\n\n".join(
            [f"File: {name}\n{content}" for name, content in context["files"].items()]
        ),
        "mcp_resources": context["mcp_resources"]
    }

    # Create prompt
    prompt = ChatPromptTemplate.from_template(QUERY_GENERATION_PROMPT)

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Generate queries
    result = await chain.ainvoke(prompt_context)

    # Parse the result into a list of queries
    queries = [q.strip() for q in result.split("\n") if q.strip()]
    
    log_llm_call(
        logger,
        f"Generate search queries for prompt: {prompt}",
        f"Generated queries: {queries}\nRaw LLM response: {result}"
    )
    
    return queries


async def select_best_results(context: Dict, search_results: List[Dict]) -> List[Dict]:
    """
    Select the best MCP servers from search results and MCP resources using LLM.

    Args:
        context: Project context
        search_results: List of search results (may be empty)

    Returns:
        List of recommended servers, including suggestions from MCP resources
    """
    llm = get_llm()

    # Always load MCP resources
    context["mcp_resources"] = load_mcp_resources()

    # Prepare search results section
    search_results_text = ""
    if search_results:
        search_results_text = "# Direct Matches\n" + "\n\n".join(
            [
                f"Result {i+1}:\nTitle: {result.get('title', 'Unknown')}\n"
                f"Description: {result.get('description', 'No description')}\n"
                f"CLI Command: {result.get('cli_command', 'Not specified')}\n"
                f"GitHub URL: {result.get('github_url', 'Not specified')}\n"
                f"Content: {result.get('content', '')[:1000]}..."
                for i, result in enumerate(search_results)
            ]
        )
    else:
        search_results_text = "# No Direct Matches Found\nPlease suggest relevant servers from the MCP Resources."

    # Prepare context for the prompt
    prompt_context = {
        "prompt": context["prompt"],
        "files": "\n\n".join(
            [f"File: {name}\n{content}" for name, content in context["files"].items()]
        ),
        "mcp_resources": context["mcp_resources"],
        "search_results": search_results_text,
    }

    # Create prompt
    prompt = ChatPromptTemplate.from_template(RESULT_SELECTION_PROMPT)

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Generate selection
    result = await chain.ainvoke(prompt_context)

    log_llm_call(
        logger,
        "Select best results from search",
        f"Raw LLM response: {result}"
    )

    try:
        # Parse JSON response
        selected_servers = json.loads(result)
        
        # Validate and normalize server objects
        selected = []
        for server in selected_servers:
            if not isinstance(server, dict) or "title" not in server:
                continue
                
            # Ensure all required fields are present with defaults
            normalized_server = {
                "title": server.get("title", "Unknown"),
                "description": server.get("description", "No description available"),
                "github_url": server.get("github_url", ""),
                "project_url": server.get("project_url", ""),
                "sources": [],  # Can be populated if needed
                "cli_command": server.get("cli_command", "# Visit https://mcpindex.net for installation instructions"),
                "content": server.get("content", "Please check the MCP documentation for more details.")
            }
            selected.append(normalized_server)
            
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        logger.debug(f"Raw response: {result}")
        selected = []

    # If no valid results, provide a default suggestion
    if not selected:
        default_server = {
            "title": "MCP Server Recommendation",
            "description": "Based on your requirements, please visit the MCP Index for available servers.",
            "github_url": "https://github.com/modelcontextprotocol/servers",
            "project_url": "https://mcpindex.net",
            "sources": [],
            "cli_command": "# Visit https://mcpindex.net to find the right MCP server for your needs",
            "content": "The Model Context Protocol (MCP) offers various servers that might meet your needs. "
                      "Please visit https://mcpindex.net to explore available servers and find detailed installation instructions."
        }
        selected.append(default_server)

    logger.debug(f"Selected {len(selected)} recommendations")
    return selected


async def generate_server_content(context: Dict, server: Dict) -> Dict:
    """
    Generate detailed content for an MCP server.

    Args:
        context: Project context
        server: Server information

    Returns:
        Dictionary with generated content
    """
    llm = get_llm()

    # Add MCP resources to context if not already present
    if "mcp_resources" not in context:
        context["mcp_resources"] = load_mcp_resources()

    # Prepare context for the prompt
    prompt_context = {
        "prompt": context["prompt"],
        "files": "\n\n".join(
            [f"File: {name}\n{content}" for name, content in context["files"].items()]
        ),
        "mcp_resources": context["mcp_resources"],
        "server_name": server.get("title", "Unknown"),
        "server_description": server.get("description", "No description"),
        "server_content": server.get("content", ""),
    }

    # Create prompt
    prompt = ChatPromptTemplate.from_template(CONTENT_GENERATION_PROMPT)

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Generate content
    result = await chain.ainvoke(prompt_context)

    log_llm_call(
        logger,
        f"Generate content for server: {server.get('title', 'Unknown')}",
        f"Raw LLM response: {result}"
    )

    # Parse the result to extract different sections
    lines = result.split("\n")
    content = {}

    for i, line in enumerate(lines):
        if line.startswith("TITLE:"):
            content["title"] = line.replace("TITLE:", "").strip()
        elif line.startswith("GITHUB_URL:"):
            content["github_url"] = line.replace("GITHUB_URL:", "").strip()
        elif line.startswith("PROJECT_URL:"):
            content["project_url"] = line.replace("PROJECT_URL:", "").strip()
        elif line.startswith("CLI_COMMAND:"):
            content["cli_command"] = line.replace("CLI_COMMAND:", "").strip()
        elif line.startswith("DESCRIPTION:"):
            content["description"] = line.replace("DESCRIPTION:", "").strip()
        elif line.startswith("CONTENT:"):
            # Get all remaining lines as content
            content["content"] = "\n".join(lines[i + 1 :])
            break

    return content


async def generate_server_recommendations(
    context: Dict, search_results: List[Dict]
) -> List[MCPServer]:
    """
    Generate final MCP server recommendations.

    Args:
        context: Project context
        search_results: List of search results

    Returns:
        List of MCPServer objects with recommendations
    """
    logger.debug("Generating server recommendations")
    
    # Add MCP resources to context
    context["mcp_resources"] = load_mcp_resources()
    
    # Select best results
    best_results = await select_best_results(context, search_results)

    recommendations = []

    for result in best_results:
        # Create source objects from the sources list
        sources = []
        for source_data in result.get("sources", []):
            source = Source(
                source_name=source_data.get("source_name", "unknown"),
                source_url=source_data.get("source_url", ""),
                source_title=source_data.get("source_title", ""),
                source_description=source_data.get("source_description", "")
            )
            sources.append(source)

        # If no sources provided, create a default one
        if not sources:
            sources = [Source(
                source_name="github.com",
                source_url=result.get("github_url", ""),
                source_title=result.get("title", "Unknown"),
                source_description=result.get("description", "")
            )]

        # Create server object using the JSON structure directly
        server = MCPServer(
            title=result.get("title", "Unknown"),
            github_url=result.get("github_url"),
            project_url=result.get("project_url"),
            sources=sources,
            cli_command=result.get("cli_command", "npm install -g unknown-mcp-server"),
            description=result.get("description", "No description"),
            content=result.get("content", "No detailed information available.")
        )

        recommendations.append(server)

    log_llm_call(
        logger,
        "Generate final recommendations",
        f"Generated {len(recommendations)} recommendations with details"
    )
    
    return recommendations
