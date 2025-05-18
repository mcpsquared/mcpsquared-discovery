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
    prompt: str, 
    files: Optional[List[UploadFile]] = None,
    existing_context: Optional[ProjectContext] = None,
) -> ProjectContext:
    """
    Analyze project files to understand context and generate search queries.

    Args:
        prompt: User prompt describing the project needs
        files: Optional project files for context
        existing_context: Optional existing ProjectContext to enhance

    Returns:
        ProjectContext object with analyzed information
    """
    # Start with existing context or create new one
    if existing_context:
        context = existing_context
    else:
        context = ProjectContext(
            user_prompt=prompt,
            project_mdc_file_contents=None,
            project_package_manager_contents=None,
            additional_files={}
        )

    # Process files if provided
    if files:
        for file in files:
            file_content = await read_file_content(file)
            
            # Update appropriate fields based on file type
            if file.filename.endswith(".mdc"):
                context.project_mdc_file_contents = file_content
            elif file.filename == "package.json":
                context.project_package_manager_contents = file_content
            else:
                if not context.additional_files:
                    context.additional_files = {}
                context.additional_files[file.filename] = file_content

    return context
