"""
Configuration settings for the MCP Squared Discovery Service.
"""

from typing import List
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

import logging

logger = logging.getLogger(__name__)

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

    # Langsmith Settings
    LANGCHAIN_API_KEY: str = Field(..., description="Langsmith API key")
    LANGCHAIN_ENDPOINT: str = Field(
        "https://api.smith.langchain.com", description="Langsmith API endpoint"
    )
    LANGCHAIN_PROJECT: str = Field("mcp-squared-discovery", description="Langsmith project name")
    LANGCHAIN_TRACING_V2: bool = Field(True, description="Enable Langsmith tracing v2")

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
        "https://api.smithery.dev/v1/servers",
        description="Smithery API URL for server search",
    )

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        case_sensitive=True
    )

    def setup_langchain_env(self):
        """Set up Langchain environment variables."""
        os.environ["LANGCHAIN_API_KEY"] = self.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_ENDPOINT"] = self.LANGCHAIN_ENDPOINT
        os.environ["LANGCHAIN_PROJECT"] = self.LANGCHAIN_PROJECT
        os.environ["LANGCHAIN_TRACING_V2"] = str(self.LANGCHAIN_TRACING_V2).lower()
        
        logger.info("\n\n===\n\nLangchain environment variables set up\n\n===\n\n")
        logger.info(f"LANGCHAIN_API_KEY: {self.LANGCHAIN_API_KEY}")
        logger.info(f"LANGCHAIN_ENDPOINT: {self.LANGCHAIN_ENDPOINT}")
        logger.info(f"LANGCHAIN_PROJECT: {self.LANGCHAIN_PROJECT}")
        logger.info(f"LANGCHAIN_TRACING_V2: {self.LANGCHAIN_TRACING_V2}")
        logger.info("\n\n===\n\n")


settings = Settings()
settings.setup_langchain_env()  # Set up Langchain environment variables

# Log the settings loaded
logger.info("Settings loaded and environment configured")
