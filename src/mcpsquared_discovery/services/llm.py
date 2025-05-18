"""
Service for LLM interactions using LangChain.
"""

import logging
from typing import Dict, List

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

    # Prepare context for the prompt
    prompt_context = {
        "prompt": prompt,
        "files": "\n\n".join(
            [f"File: {name}\n{content}" for name, content in context["files"].items()]
        ),
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
    Select the best MCP servers from search results using LLM.

    Args:
        context: Project context
        search_results: List of search results

    Returns:
        Filtered list of the best matching servers
    """
    llm = get_llm()

    # Prepare context for the prompt
    prompt_context = {
        "prompt": context["prompt"],
        "files": "\n\n".join(
            [f"File: {name}\n{content}" for name, content in context["files"].items()]
        ),
        "search_results": "\n\n".join(
            [
                f"Result {i+1}:\nTitle: {result.get('name', 'Unknown')}\n"
                f"Description: {result.get('description', 'No description')}\n"
                f"Content: {result.get('full_content', '')[:1000]}..."
                for i, result in enumerate(search_results)
            ]
        ),
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

    # Parse the result to get indices of selected servers
    selected_indices = []
    for line in result.split("\n"):
        if line.strip().startswith("Result"):
            try:
                index = int(line.split("Result")[1].split(":")[0].strip()) - 1
                if 0 <= index < len(search_results):
                    selected_indices.append(index)
            except (ValueError, IndexError):
                continue

    # Return selected results
    selected = [search_results[i] for i in selected_indices]
    logger.debug(f"Selected {len(selected)} results from {len(search_results)} total results")
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

    # Prepare context for the prompt
    prompt_context = {
        "prompt": context["prompt"],
        "files": "\n\n".join(
            [f"File: {name}\n{content}" for name, content in context["files"].items()]
        ),
        "server_name": server.get("name", "Unknown"),
        "server_description": server.get("description", "No description"),
        "server_content": server.get("full_content", ""),
    }

    # Create prompt
    prompt = ChatPromptTemplate.from_template(CONTENT_GENERATION_PROMPT)

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Generate content
    result = await chain.ainvoke(prompt_context)

    log_llm_call(
        logger,
        f"Generate content for server: {server.get('name', 'Unknown')}",
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
    # Select best results
    best_results = await select_best_results(context, search_results)

    recommendations = []

    for result in best_results:
        # Generate detailed content
        content = await generate_server_content(context, result)

        # Create source object
        source = Source(
            source_name=result.get("source", "smithery.ai"),
            source_url=result.get("url", "https://smithery.ai"),
            source_title=result.get("name", "Unknown"),
            source_description=result.get("description", "No description"),
        )

        # Create server object
        server = MCPServer(
            title=content.get("title", result.get("name", "Unknown")),
            github_url=content.get("github_url"),
            project_url=content.get("project_url"),
            sources=[source],
            cli_command=content.get("cli_command", "npm install -g unknown-mcp-server"),
            description=content.get(
                "description", result.get("description", "No description")
            ),
            content=content.get("content", "No detailed information available."),
        )

        recommendations.append(server)

    log_llm_call(
        logger,
        "Generate final recommendations",
        f"Generated {len(recommendations)} recommendations with details"
    )
    
    return recommendations
