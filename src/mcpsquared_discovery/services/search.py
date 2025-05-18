"""
Service for searching MCP servers from various sources.
"""

import logging
import json
from typing import Dict, List
from pathlib import Path

import httpx

from mcpsquared_discovery.core.config import settings
from mcpsquared_discovery.core.logging import log_api_call
from mcpsquared_discovery.services.content_retrieval import retrieve_content

logger = logging.getLogger(__name__)

def load_mcp_servers() -> List[Dict]:
    """
    Load MCP servers from the local JSON file.

    Returns:
        List of server records
    """
    json_path = Path(__file__).parent.parent / "data" / "mcp_servers.json"
    with open(json_path) as f:
        data = json.load(f)
    return data.get("mcp_servers", [])

def score_server_match(server: Dict, query: str) -> float:
    """
    Score how well a server matches a query.

    Args:
        server: Server record
        query: Search query string

    Returns:
        Match score between 0 and 1
    """
    query = query.lower()
    score = 0.0
    
    # Check title match (highest weight)
    if query in server.get("title", "").lower():
        score += 0.5
        
    # Check description match
    if query in server.get("description", "").lower():
        score += 0.3
        
    # Check content match
    if query in server.get("content", "").lower():
        score += 0.2
        
    # Check CLI command match
    if query in server.get("cli_command", "").lower():
        score += 0.1
        
    # Check GitHub URL match
    if query in server.get("github_url", "").lower():
        score += 0.1
        
    return min(score, 1.0)

async def search_local_servers(query: str) -> List[Dict]:
    """
    Search for MCP servers in the local JSON data.

    Args:
        query: Search query string

    Returns:
        List of matching server records
    """
    servers = load_mcp_servers()
    
    # Score each server's match against the query
    scored_servers = []
    for server in servers:
        score = score_server_match(server, query)
        if score > 0:
            scored_servers.append((score, server))
    
    # Sort by score descending and return servers
    scored_servers.sort(reverse=True, key=lambda x: x[0])
    matches = [server for score, server in scored_servers]
    
    logger.debug("Local search with query '%s' found %d matches", query, len(matches))
    return matches

async def enrich_search_results(results: List[Dict]) -> List[Dict]:
    """
    Enrich search results with additional content from source pages.

    Args:
        results: Raw search results

    Returns:
        Enriched search results with full content
    """
    # No need to enrich as content is already in the JSON
    return results

async def search_mcp_servers(context: Dict) -> List[Dict]:
    """
    Search for MCP servers based on project context.

    Args:
        context: Project context including search queries

    Returns:
        List of search results
    """
    all_results = []
    seen_titles = set()

    # Search using each generated query
    for query in context["search_queries"]:
        # Search local JSON data
        local_results = await search_local_servers(query)
        
        # Add unique results
        for result in local_results:
            title = result.get("title")
            if title and title not in seen_titles:
                seen_titles.add(title)
                # Ensure all required fields are present with defaults if needed
                enriched_result = {
                    "title": title,
                    "github_url": result.get("github_url", ""),
                    "project_url": result.get("project_url", ""),
                    "sources": result.get("sources", []),
                    "cli_command": result.get("cli_command", "npm install -g unknown-mcp-server"),
                    "description": result.get("description", "No description available"),
                    "content": result.get("content", "No detailed content available")
                }
                all_results.append(enriched_result)

    logger.debug("Found %d unique servers across all queries", len(all_results))
    return all_results
