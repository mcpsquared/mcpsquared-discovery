# MCP Squared Discovery Service

A FastAPI-based backend service that recommends MCP Servers and tools for use by a locally running MCP Squared discovery tool.

## Overview

The MCP Squared Discovery Service accepts a prompt and file attachments, then returns a JSON response with recommended MCP servers based on the project context. It uses LangChain with Claude 3.5 Sonnet via OpenRouter to evaluate search results and generate detailed recommendations. The service uses a local JSON database of MCP servers for fast and reliable search results.

## Features

- Accept a prompt and file attachments (project specs, package configs)
- Search for relevant MCP servers using local JSON data
- Use LangChain with Claude 3.5 Sonnet to evaluate search results
- Generate detailed descriptions and installation instructions for each recommended server
- Return a structured JSON response with server recommendations
- Score-based ranking system for search results
- Case-insensitive search across multiple fields
- Duplicate removal based on title

## Getting Started

### Prerequisites

- Python 3.12.7
- Poetry
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mcpsquared/mcpsquared-discovery.git
cd mcpsquared-discovery
```

2. Install dependencies:
```bash
# Install latest stable Python
pyenv install 3.12.7

# Set local Python version
cd {project path}
pyenv local 3.12.7
pyenv shell 3.12.7

# Configure Poetry to create virtualenv in project directory
poetry config virtualenvs.in-project true

# Create new virtualenv with project Python version
poetry env use python

# Activate virtualenv
poetry env activate - not working currently

# Install dependencies
poetry install
```

Increment version:

```bash
poetry version patch
```

3. Create a `.env` file with required environment variables:
```
# OpenRouter Settings
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet

# Langsmith Settings
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=mcp-squared-discovery
LANGCHAIN_TRACING_V2=true

# AWS Settings
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-west-2
AWS_PROFILE=andi-ai

# API Settings
ANDISEARCH_API_KEY=your_andisearch_api_key
ENVIRONMENT=development

# Content Retrieval Settings
CONTENT_RETRIEVAL_URL=https://api.andisearch.com/parser/parser
```

### Running the Service

Using Poetry:
```bash
poetry run uvicorn mcpsquared_discovery.main:app --reload
```

Using Docker Compose:
```bash
docker-compose up
```

## API Documentation

Once the service is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

#### POST /discover

Discover MCP servers based on project context.

**Request:**
- `prompt` (form field): User prompt describing the project needs
- `files` (form files): Optional project files for context (specs, package configs, etc.)

**Response:**
```json
{
  "mcp_servers": [
    {
      "title": "Server Name",
      "github_url": "https://github.com/repo",
      "project_url": "https://project-site.com",
      "sources": [
        {
          "source_name": "directory-name",
          "source_url": "https://source-url.com",
          "source_title": "Page Title",
          "source_description": "Brief description"
        }
      ],
      "cli_command": "npm install package",
      "description": "Short description",
      "content": "Detailed markdown content"
    }
  ]
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Implementation Details

The service follows a modular architecture with separate components for:
- API routes and endpoint handling
- Project file analysis and context extraction
- Local JSON-based MCP server search with scoring system
- Content retrieval and enrichment
- LLM interaction using LangChain

Key features of the implementation:
1. Local JSON database for fast and reliable server lookup
2. Scoring system for ranking search results based on multiple fields
3. LangChain with Claude 3.5 Sonnet for intelligent result selection
4. Comprehensive error handling and validation
5. Docker and Docker Compose configuration for easy deployment
6. Poetry for dependency management
```
