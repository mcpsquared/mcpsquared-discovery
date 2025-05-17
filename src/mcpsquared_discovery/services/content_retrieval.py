"""
Service for retrieving content from URLs.
"""

import httpx

from mcpsquared_discovery.core.config import settings


async def retrieve_content(url: str) -> str:
    """
    Retrieve and parse content from a URL using the Andi Search API.

    Args:
        url: The URL to retrieve content from

    Returns:
        Parsed content as markdown or text
    """
    params = {"url": url, "api_key": settings.ANDISEARCH_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.CONTENT_RETRIEVAL_URL, params=params, timeout=30.0
        )

        if response.status_code == 200:
            data = response.json()
            # Extract content from the response
            content = data.get("content", "")
            return content
        else:
            # Return empty string if retrieval fails
            return ""
