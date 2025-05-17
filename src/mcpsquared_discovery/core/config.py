"""
Configuration settings for the application.
"""

from typing import List
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class Settings(BaseSettings):
    """Application settings."""

    # API Keys and URLs
    OPENROUTER_API_KEY: str = Field(..., description="OpenRouter API key")
    OPENROUTER_BASE_URL: str = Field("https://openrouter.ai/api/v1", description="OpenRouter base URL")
    SMITHERY_API_KEY: str = Field(..., description="Smithery API key")
    ANDISEARCH_API_KEY: str = Field(..., description="Andi Search API key")

    # AWS Settings
    AWS_ACCESS_KEY_ID: str = Field(..., description="AWS access key ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., description="AWS secret access key")
    AWS_DEFAULT_REGION: str = Field("us-west-2", description="AWS default region")
    AWS_PROFILE: str = Field("andi-ai", description="AWS profile name")

    # LLM Settings
    LLM_MODEL: str = Field(
        "anthropic/claude-3.5-sonnet", description="LLM model to use"
    )

    # API Settings
    CORS_ORIGINS: List[str] = Field(["*"], description="List of allowed CORS origins")

    # Environment
    ENVIRONMENT: str = Field("development", description="Application environment")

    # Content retrieval
    CONTENT_RETRIEVAL_URL: str = Field(
        "https://api.andisearch.com/parser/parser",
        description="URL for content retrieval API",
    )

    # Smithery API
    SMITHERY_API_URL: str = Field(
        "https://api.smithery.ai/v1/servers",
        description="Smithery API URL for server search",
    )

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        case_sensitive=True
    )


settings = Settings()
