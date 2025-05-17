"""
API routes for the MCP Squared Discovery Service.
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from mcpsquared_discovery.models.schemas import (
    DiscoveryRequest,
    DiscoveryResponse,
    ProjectContext,
)
from mcpsquared_discovery.services.analyzer import (
    analyze_project_files,
    extract_project_context,
)
from mcpsquared_discovery.services.llm import generate_server_recommendations
from mcpsquared_discovery.services.search import search_mcp_servers

router = APIRouter()


@router.post("/discover", response_model=DiscoveryResponse)
async def discover_mcp_servers(
    prompt: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
):
    """
    Discover MCP servers based on project context.

    Args:
        prompt: User prompt describing the project needs
        files: Optional project files for context (specs, package configs, etc.)

    Returns:
        JSON response with recommended MCP servers
    """
    try:
        # Analyze project files to understand context
        project_context = await analyze_project_files(prompt, files)

        # Search for relevant MCP servers
        search_results = await search_mcp_servers(project_context)

        # Generate recommendations using LLM
        recommendations = await generate_server_recommendations(
            project_context, search_results
        )

        return DiscoveryResponse(mcp_servers=recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@router.post("/project-context")
async def read_project_context(project_context: ProjectContext) -> Dict:
    """
    Process project context information.

    Args:
        project_context: Project context information

    Returns:
        Confirmation message
    """
    return {
        "status": "success",
        "message": "Received project context",
        "prompt": project_context.user_prompt,
    }


@router.post("/discover-json", response_model=DiscoveryResponse)
async def discover_mcp_servers_json(request: DiscoveryRequest):
    """
    Discover MCP servers based on project context provided as JSON.

    Args:
        request: Discovery request with prompt and optional context

    Returns:
        JSON response with recommended MCP servers
    """
    try:
        # Extract project context
        project_context = extract_project_context(request.prompt, request.context)

        # Search for relevant MCP servers
        search_results = await search_mcp_servers(project_context)

        # Generate recommendations using LLM
        recommendations = await generate_server_recommendations(
            project_context, search_results
        )

        return DiscoveryResponse(mcp_servers=recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )
