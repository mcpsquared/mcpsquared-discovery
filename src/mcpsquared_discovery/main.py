"""
Main application module for MCP Squared Discovery Service.
"""

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import os

from mcpsquared_discovery.api.routes import router
from mcpsquared_discovery.core.config import settings
from mcpsquared_discovery.core.logging import setup_logging
from mcpsquared_discovery.models.schemas import ProjectContext

# Initialize logging
setup_logging()

# Initialize Langsmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2).lower()
os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

app = FastAPI(
    title="MCP Squared Discovery Service",
    description="A service to recommend MCP Servers based on project context",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/project-context-test")
async def test_project_context(
    prompt: str = Form(...),
    project_spec_mdc: str = Form(..., alias="project_spec.mdc"),
    package_json: str = Form(..., alias="package.json"),
):
    """
    Test endpoint for project context that accepts form data.

    Args:
        prompt: The user's prompt
        project_spec_mdc: The project's MDC specification
        package_json: The project's package.json contents

    Returns:
        The received project context
    """
    # Create ProjectContext object from form data
    project_context = ProjectContext(
        user_prompt=prompt,
        project_mdc_file_contents=project_spec_mdc,
        project_package_manager_contents=package_json
    )
    
    return {"message": "Received project context", "data": project_context.model_dump()}
