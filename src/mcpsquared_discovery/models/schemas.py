"""
Pydantic models for request and response schemas.
"""

from typing import Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, AnyHttpUrl, field_validator


class ProjectContext(BaseModel):
    """Project context information for MCP server discovery."""

    user_prompt: str = Field(..., description="The user prompt for the project")
    project_mdc_file_contents: Optional[str] = Field(
        None, description="The contents of the project's mdc and .md files (if any)"
    )
    project_package_manager_contents: Optional[str] = Field(
        None,
        description="The contents of the project's package manager file eg package.json, pyproject.toml, cargo.toml, etc",
    )
    additional_files: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Additional project files with filename as key and content as value",
    )


class Source(BaseModel):
    """Information about a source where an MCP server was found."""

    source_name: str = Field(..., description="Name of the directory source")
    source_url: str = Field("", description="URL of the source page")
    source_title: str = Field(..., description="Title of the source page")
    source_description: str = Field(
        ..., description="Brief description from the source"
    )

    @field_validator("source_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL if present, allow empty string."""
        if not v:
            return ""
        try:
            result = urlparse(v)
            if all([result.scheme, result.netloc]):
                return v
        except Exception:
            pass
        return ""


class MCPServer(BaseModel):
    """Information about a recommended MCP server."""

    title: str = Field(..., description="Name of the MCP server")
    github_url: str = Field("", description="GitHub repository URL")
    project_url: str = Field("", description="Official project URL")
    sources: List[Source] = Field(
        default_factory=list, description="Sources where this server was found"
    )
    cli_command: str = Field(
        ..., description="Command to install or configure the server"
    )
    description: str = Field(..., description="Brief description of the server")
    content: str = Field(..., description="Detailed markdown content about the server")

    @field_validator("github_url", "project_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL if present, allow empty string."""
        if not v:
            return ""
        try:
            result = urlparse(v)
            if all([result.scheme, result.netloc]):
                return v
        except Exception:
            pass
        return ""


class DiscoveryResponse(BaseModel):
    """Response model for the discovery endpoint."""

    mcp_servers: List[MCPServer] = Field(
        ..., description="List of recommended MCP servers"
    )


class DiscoveryRequest(BaseModel):
    """Request model for the discovery endpoint."""

    prompt: str = Field(..., description="User prompt describing the project needs")
    context: Optional[ProjectContext] = Field(
        None, description="Additional project context"
    )
