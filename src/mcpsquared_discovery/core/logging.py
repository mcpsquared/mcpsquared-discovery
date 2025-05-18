"""
Logging configuration for the MCP Squared Discovery Service.
"""

import logging
import sys
from typing import Any, Dict

from mcpsquared_discovery.core.config import settings

def setup_logging() -> None:
    """
    Configure logging for the application.
    
    Sets up logging with appropriate level and format based on environment.
    """
    log_level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # Set level for external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)

def log_api_call(logger: logging.Logger, endpoint: str, payload: Dict[str, Any], response: Dict[str, Any]) -> None:
    """
    Log API call details.
    
    Args:
        logger: Logger instance
        endpoint: API endpoint called
        payload: Request payload
        response: API response
    """
    logger.debug(
        "API Call",
        extra={
            "endpoint": endpoint,
            "payload": payload,
            "response": response
        }
    )

def log_llm_call(logger: logging.Logger, prompt: str, response: str) -> None:
    """
    Log LLM call details.
    
    Args:
        logger: Logger instance
        prompt: Input prompt
        response: LLM response
    """
    logger.debug("LLM Call - Prompt: %s, Response: %s", str(prompt), str(response)) 