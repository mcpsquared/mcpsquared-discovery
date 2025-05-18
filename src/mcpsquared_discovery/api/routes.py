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
    project_spec_mdc: Optional[str] = Form(None, alias="project_spec.mdc"),
    package_json: Optional[str] = Form(None, alias="package.json"),
    files: Optional[List[UploadFile]] = File(None),
):
    """
    Discover MCP servers based on project context.

    Args:
        prompt: User prompt describing the project needs
        project_spec_mdc: Optional project MDC specification
        package_json: Optional package.json contents
        files: Optional additional project files for context

    Returns:
        JSON response with recommended MCP servers
    """
    try:
        # Create initial project context from form data
        project_context = ProjectContext(
            user_prompt=prompt,
            project_mdc_file_contents=project_spec_mdc,
            project_package_manager_contents=package_json,
        )

        # Analyze any additional project files to enhance context
        if files:
            project_context = await analyze_project_files(
                prompt=prompt,
                files=files,
                existing_context=project_context
            )

        # Convert ProjectContext to dict for search
        context_dict = {
            "prompt": project_context.user_prompt,
            "files": {},
            "search_queries": [],
        }
        
        if project_context.project_mdc_file_contents:
            context_dict["files"]["project.mdc"] = project_context.project_mdc_file_contents
        if project_context.project_package_manager_contents:
            context_dict["files"]["package.json"] = project_context.project_package_manager_contents
        if project_context.additional_files:
            context_dict["files"].update(project_context.additional_files)

        # Search for relevant MCP servers
        search_results = await search_mcp_servers(context_dict)

        # Generate recommendations using LLM
        recommendations = await generate_server_recommendations(
            context_dict, search_results
        )

        return DiscoveryResponse(mcp_servers=recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@router.post("/project-context")
async def read_project_context(
    prompt: str = Form(...),
    project_spec_mdc: Optional[str] = Form(None, alias="project_spec.mdc"),
    package_json: Optional[str] = Form(None, alias="package.json"),
) -> Dict:
    """
    Process project context information from form data.

    Args:
        prompt: The user's prompt
        project_spec_mdc: Optional project MDC specification
        package_json: Optional package.json contents

    Returns:
        Confirmation message with processed context
    """
    project_context = ProjectContext(
        user_prompt=prompt,
        project_mdc_file_contents=project_spec_mdc,
        project_package_manager_contents=package_json,
    )
    
    return {
        "status": "success",
        "message": "Received project context",
        "data": project_context.model_dump(),
    }


@router.post("/discover-json", response_model=DiscoveryResponse)
async def discover_mcp_servers_json(request: DiscoveryRequest):
    """
    Discover MCP servers based on project context provided as JSON.
    This endpoint accepts JSON data instead of form data.

    Args:
        request: Discovery request with prompt and optional context

    Returns:
        JSON response with recommended MCP servers
    """
    try:
        # Extract project context
        context_dict = extract_project_context(request.prompt, request.context)

        # Search for relevant MCP servers
        search_results = await search_mcp_servers(context_dict)

        # Generate recommendations using LLM
        recommendations = await generate_server_recommendations(
            context_dict, search_results
        )

        return DiscoveryResponse(mcp_servers=recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )
