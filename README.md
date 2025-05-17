# MCP Squared Discovery Service

A FastAPI-based backend service that recommends publicly available MCP Servers and tools for use by a locally running MCP Squared discovery tool.

## Overview

The MCP Squared Discovery Service accepts a prompt and file attachments, then returns a JSON response with recommended MCP servers based on the project context. It uses LangChain with Claude 3.5 Sonnet via OpenRouter to evaluate search results and generate detailed recommendations.

## Features

- Accept a prompt and file attachments (project specs, package configs)
- Search for relevant MCP servers using the Smithery API
- Use LangChain with Claude 3.5 Sonnet to evaluate search results
- Generate detailed descriptions and installation instructions for each recommended server
- Return a structured JSON response with server recommendations

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

3. Create a `.env` file with required API keys:
```
OPENROUTER_API_KEY=your_openrouter_api_key
SMITHERY_API_KEY=your_smithery_api_key
ANDISEARCH_API_KEY=your_andisearch_api_key
ENVIRONMENT=development
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
```

This implementation provides a solid foundation for the MCP Squared Discovery Service. It includes:

1. A FastAPI backend with a `/discover` endpoint that accepts a prompt and file attachments
2. Integration with the Smithery API for searching MCP servers
3. LangChain with Claude 3.5 Sonnet via OpenRouter for evaluating search results
4. Detailed prompts for query generation, result selection, and content generation
5. Docker and Docker Compose configuration for containerization
6. Poetry for dependency management

The service follows a modular architecture with separate components for:
- API routes
- Project file analysis
- MCP server search
- Content retrieval
- LLM interaction

This implementation focuses on the Smithery API as the initial source for MCP servers, with the ability to add more sources in the future.
```
