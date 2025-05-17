"""
Service for analyzing project files to understand context.
"""

from typing import Dict, List, Optional

from fastapi import UploadFile

from mcpsquared_discovery.models.schemas import ProjectContext
from mcpsquared_discovery.services.llm import generate_search_queries


async def read_file_content(file: UploadFile) -> str:
    """
    Read the content of an uploaded file.

    Args:
        file: The uploaded file

    Returns:
        The file content as a string
    """
    content = await file.read()
    await file.seek(0)  # Reset file pointer
    return content.decode("utf-8")


def extract_project_context(
    prompt: str, context: Optional[ProjectContext] = None
) -> Dict:
    """
    Extract project context from the provided ProjectContext model.

    Args:
        prompt: User prompt describing the project needs
        context: Optional ProjectContext model

    Returns:
        Dictionary containing project context
    """
    # Initialize context with prompt
    project_context = {
        "prompt": prompt,
        "files": {},
        "technologies": [],
        "search_queries": [],
    }

    # Add context from ProjectContext model if provided
    if context:
        if context.project_mdc_file_contents:
            project_context["files"]["project.mdc"] = context.project_mdc_file_contents

        if context.project_package_manager_contents:
            project_context["files"][
                "package_manager.json"
            ] = context.project_package_manager_contents

        if context.additional_files:
            for filename, content in context.additional_files.items():
                project_context["files"][filename] = content

    return project_context


async def analyze_project_files(
    prompt: str, files: Optional[List[UploadFile]] = None
) -> Dict:
    """
    Analyze project files to understand context and generate search queries.

    Args:
        prompt: User prompt describing the project needs
        files: Optional project files for context

    Returns:
        Dictionary containing project context and search queries
    """
    # Initialize context with prompt
    context = {"prompt": prompt, "files": {}, "technologies": [], "search_queries": []}

    # Process files if provided
    if files:
        for file in files:
            file_content = await read_file_content(file)
            context["files"][file.filename] = file_content

            # Extract technologies from package files
            if file.filename.endswith(
                ("package.json", "pyproject.toml", "requirements.txt")
            ):
                # In a real implementation, we would parse these files to extract dependencies
                pass

    # Generate search queries using LLM
    search_queries = await generate_search_queries(context)
    context["search_queries"] = search_queries

    return context
