"""
Service for searching MCP servers from various sources.
"""

import logging
from typing import Dict, List

import httpx

from mcpsquared_discovery.core.config import settings
from mcpsquared_discovery.core.logging import log_api_call
from mcpsquared_discovery.services.content_retrieval import retrieve_content

logger = logging.getLogger(__name__)

async def search_smithery_api(query: str) -> List[Dict]:
    """
    Search for MCP servers in the Smithery registry.

    Args:
        query: Search query string

    Returns:
        List of matching server records
    """
    headers = {
        "Authorization": f"Bearer {settings.SMITHERY_API_KEY}",
        "Accept": "application/json",
    }

    params = {"q": query, "page": 1, "pageSize": 10}

    async with httpx.AsyncClient() as client:
        logger.debug("Searching Smithery API with query: %s", query)
        response = await client.get(
            settings.SMITHERY_API_URL, headers=headers, params=params
        )
        response.raise_for_status()
        response_data = response.json()
        
        log_api_call(
            logger,
            "smithery_search",
            {"query": query, "params": params},
            {"status_code": response.status_code, "data": response_data}
        )
        
        return response_data.get("servers", [])


async def enrich_search_results(results: List[Dict]) -> List[Dict]:
    """
    Enrich search results with additional content from source pages.

    Args:
        results: Raw search results

    Returns:
        Enriched search results with full content
    """
    enriched_results = []

    for result in results:
        # Get source URL
        source_url = result.get("url") or result.get("homepage")

        if source_url:
            # Retrieve full content from the source page
            content = await retrieve_content(source_url)
            result["full_content"] = content

        enriched_results.append(result)

    return enriched_results


async def search_mcp_servers(context: Dict) -> List[Dict]:
    """
    Search for MCP servers based on project context.

    Args:
        context: Project context including search queries

    Returns:
        List of search results
    """
    all_results = []

    # Search using each generated query
    for query in context["search_queries"]:
        # Search Smithery API
        smithery_results = await search_smithery_api(query)
        all_results.extend(smithery_results)

    # Enrich results with full content
    enriched_results = await enrich_search_results(all_results)

    return enriched_results
