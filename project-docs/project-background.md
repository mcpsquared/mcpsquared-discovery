
# What we're building

## MCP Squared Discovery Service Background


### Background on the service

FastAPI based backend service to recommend publicly available MCP Servers and tools for use by a locally running MCP Squared discovery tool.

Accepts a prompt and file attachments.

Returns a JSON response with the following fields:
- `mcp_servers` - a list of MCP Servers that are recommended for the prompt with the url, project info url, description, install command, overview and directory sources used

### Running the service

Deployment via Docker on K8s using Porter.

# Backgrounder - Model Context Protocol (MCP) Servers: A Technical Overview

## Core Architecture

MCP servers act as standardized bridges between AI models and external tools/data sources. The architecture consists of three main components[^1]:

- MCP Hosts: AI-powered applications like Cursor IDE that need access to external tools
- MCP Clients: Protocol interfaces that maintain 1:1 connections with servers
- MCP Servers: Programs that expose specific capabilities through the standardized protocol

## Transport Types

MCP servers support two primary transport mechanisms[^2]:

1. STDIO (Standard Input/Output): Used for local integrations where the server runs on the same machine. Communication happens through stdin/stdout streams.

2. HTTP/SSE (Server-Sent Events): Enables remote connections over HTTP, with SSE handling server-to-client streaming. As of March 2025, a new Streamable HTTP specification has emerged to better support serverless deployments[^3].

## Server Capabilities 

MCP servers expose three types of functionality[^4]:

1. Tools: Functions that LLMs can call to perform specific actions
2. Resources: Data sources that provide context without side effects
3. Prompts: Pre-defined templates for optimal tool/resource usage

## Integration with Cursor IDE

To use an MCP server in Cursor:

1. Configure the server in Cursor's MCP settings (File → Preferences → Cursor Settings → MCP)[^5]

2. Add server configuration in JSON format:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "mcp-server"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

For remote HTTP servers:

```json
{
  "mcpServers": {
    "server-name": {
      "url": "http://example.com/sse"
    }
  }
}
```

## Popular MCP Servers

Several production-ready servers are available[^6]:

- GitHub: Repository management and code operations
- Slack: Channel and messaging capabilities  
- PostgreSQL: Read-only database access
- Google Drive: File access and search
- Brave Search: Web and local search functionality

## Security and Authorization

As of March 2025, MCP implements OAuth 2.1 for authentication with key features[^7]:

- Built-in PKCE security baseline
- Metadata discovery for endpoint advertisement
- Dynamic client registration
- Support for third-party identity providers

## Tool Discovery Process

When an MCP server connects to Cursor[^8]:

1. Server advertises available tools and capabilities
2. Cursor registers these tools for use by the AI
3. AI can discover and invoke tools based on natural language requests
4. User approval is required before tool execution
5. Results are returned to the AI for incorporation into responses

## Best Practices for Implementation

Key considerations when building MCP servers[^9]:

- Implement proper error handling and logging
- Use structured schemas for tool definitions
- Include clear documentation for each tool
- Follow the principle of least privilege
- Cache responses when appropriate
- Add request validation to prevent injection attacks

[^1]: [Cursor – Model Context Protocol](https://docs.cursor.com/context/model-context-protocol)
[^2]: [Snyk - A Beginner's Guide to Visually Understanding MCP Architecture](https://snyk.io/articles/a-beginners-guide-to-visually-understanding-mcp-architecture/)
[^3]: [Auth0 - An Introduction to MCP and Authorization](https://auth0.com/blog/an-introduction-to-mcp-and-authorization/)
[^4]: [Hugging Face - What are MCP Servers And Why It Changes Everything](https://huggingface.co/blog/lynn-mikami/mcp-servers)
[^5]: [Cursor Forum - How to use MCP Server?](https://forum.cursor.com/t/how-to-use-mcp-server/50064)
[^6]: [Bright Coding - Model Context Protocol (MCP) Servers: A Comprehensive Overview](https://www.blog.brightcoding.dev/2025/04/01/model-context-protocol-mcp-servers-a-comprehensive-overview/)
[^7]: [Descope - What Is the Model Context Protocol (MCP) and How It Works](https://www.descope.com/learn/post/mcp)
[^8]: [Medium - What Are MCP Servers? The New AI Trend Explained for Everyone](https://medium.com/@sebuzdugan/what-are-mcp-servers-the-new-ai-trend-explained-for-everyone-8936489c561f)
[^9]: [What Is MCP - Notes on Implementing an MCP Server](https://www.whatismcp.com/articles/notes-on-implementing-mcp-server)


# Bcakgrounder - Best Practices for Building MCP Servers with Cursor IDE

## Project Setup
- Create isolated virtual environment for development[^1]
- Install required dependencies:
  ```bash
  pip install mcp mcp[cli]
  ```
- Configure proper directory structure with src, tests, and config folders[^1]

## Server Architecture
- Use FastMCP for rapid development[^1]
- Implement clear separation between:
  - Tools (executable functions)
  - Resources (read-only data)
  - Transport layers (stdio or SSE)[^11]
- Follow JSON-RPC 2.0 protocol standards[^3]

## Tool Development
- Write clear docstrings describing each tool's purpose and parameters[^1]
- Implement proper input validation and error handling[^14]
- Keep tools focused on single responsibilities[^1]
- Example tool structure:
```python
@mcp.tool()
def example_tool(arg1: str) -> str:
    """Clear description of what the tool does"""
    return process_input(arg1)
```

## Resource Implementation 
- Use URI templates for dynamic resources[^23]
- Include descriptive metadata (name, description, MIME type)[^23]
- Implement proper content type handling[^23]
- Example resource:
```python
@mcp.resource("example://{param}")
def get_resource(param: str) -> str:
    """Resource description"""
    return fetch_resource(param)
```

## Testing
- Use MCP Inspector for development testing[^1]
- Implement unit tests for tools and resources[^14]
- Test error handling and edge cases[^14]
- Verify transport layer functionality[^11]

## Security
- Implement authentication for sensitive operations[^14]
- Validate all inputs[^14]
- Use environment variables for sensitive data[^11]
- Follow principle of least privilege[^14]

## Integration with Cursor
- Add server configuration to `.cursor/mcp.json`[^11]
- Configure proper transport type (stdio/SSE)[^11]
- Example configuration:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

## Maintenance
- Monitor server performance and errors[^14]
- Implement proper logging[^14]
- Keep dependencies updated[^1]
- Document changes and versioning[^14]

[^1]: [MCP server: A step-by-step guide to building from scratch](https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch/)
[^3]: [Master the Art of MCP Servers: Build, Test, and Deploy Like a Pro](https://www.geeky-gadgets.com/building-mcp-server-guide/)
[^11]: [Cursor – Model Context Protocol](https://docs.cursor.com/context/model-context-protocol)
[^14]: [Building an MCP Server: Step-by-Step Guide for Developers](https://www.rapidinnovation.io/post/building-an-mcp-server-a-step-by-step-guide-for-developers)
[^23]: [Building MCP Servers : Part 1 — Getting Started with Resources](https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809)

# MCP Server Directories

We will be scraping these services to find the best MCP Servers and Tools to recommend.

https://github.com/modelcontextprotocol/servers

https://mcpservers.org/

https://mcpindex.net/en/explore

https://mcp.composio.dev/

https://mcp-server-list.com/


We will also maintain a local list of key MCP Servers extracted from these. This will include paid recommended/sponsored servers, including the hackathon sponsors if available (Goose, Greptile, Anthropic, Mintlify)

## Official Resources

1. Model Context Protocol Documentation
- Official documentation and examples at modelcontextprotocol.io[^5]
- Reference implementations and SDK usage guides
- Comprehensive server categories including data systems, web automation, and productivity tools

2. MCP Servers Repository
- Central repository of reference implementations[^1]
- Installation guides and configuration examples
- Regular updates with new server additions

## Major Directories

1. MCP Index (mcpindex.net)
- Curated directory focused on Claude, Cursor, and Cline integrations[^3]
- Integration guides and compatibility details
- Official and community server listings

2. Composio Directory (mcp.composio.dev)
- Managed MCP server deployments[^19]
- OAuth authentication handling
- Step-by-step integration tutorials for popular platforms

3. MCP Server Finder
- Detailed profiles of available MCP servers[^6]
- Implementation guides and troubleshooting resources
- Community reviews and ratings

## Technical Guides

1. Server Development Guide
- Step-by-step setup for JavaScript/TypeScript and Python servers[^23]
- Testing procedures using MCP Inspector
- Deployment workflows for npm and PyPI

2. Integration Patterns
- Authentication and security best practices[^1]
- Error handling and rate limiting strategies
- Transport layer implementations (stdio and SSE)

## Popular Categories

1. Data & Storage
- PostgreSQL for database access[^5]
- Google Drive for file management
- Qdrant for vector search

2. Development Tools
- GitHub for repository management[^1]
- Docker for code execution
- Puppeteer for browser automation

3. Communication
- Slack for team collaboration[^1]
- Discord for community engagement
- Email integration services

## Community Resources

1. MCP Server List
- Over 650 servers and clients cataloged[^4]
- Cross-platform desktop applications
- IDE extensions and development tools

2. Implementation Examples
- Reference code samples[^5]
- Configuration templates
- Best practices documentation

[^1]: [10 Best MCP Servers You Need To Know About – Bind AI](https://blog.getbind.co/2025/04/24/10-best-mcp-servers-you-need-to-know-about/)

[^3]: [MCP Index | The Directory of Model Context Protocol Servers](https://mcpindex.net/en)

[^4]: [Best MCP Servers and Clients List](https://mcp-server-list.com/)

[^5]: [Example Servers - Model Context Protocol](https://modelcontextprotocol.io/examples)

[^6]: [MCP Server Finder | The Ultimate Model Context Protocol Directory](https://www.mcpserverfinder.com/)

[^19]: [Top 10 awesome MCP servers that can make your life easier](https://composio.dev/blog/10-awesome-mcp-servers-to-make-your-life-easier/)

[^23]: [Master the Art of MCP Servers: Build, Test, and Deploy Like a Pro](https://www.geeky-gadgets.com/building-mcp-server-guide/)


# MCP Server Directory APIs

Here are the top MCP server directories with APIs, based on recent sources:

1. **Composio Registry** - Provides 100+ managed MCP servers with built-in authentication and OAuth support[^1]. Offers standardized APIs for integrating tools like Notion, Figma, and GitHub.

2. **PulseMCP** - Features a clean interface with extensive filtering options and official provider verification. Includes use case examples and API documentation for each server[^2].

3. **Glama** - Assigns quality scores to each MCP server and provides detailed API reports. Helps developers quickly assess server security and reliability[^2].

4. **OpenTools** - Offers a unified API supporting Curl, Python and TypeScript to access 2,000+ MCP servers. Provides generative APIs for tool usage[^3].

5. **Smithery** - Gives access to 2,000+ MCP servers through standardized APIs. Focuses on production-ready implementations[^3].

For direct API integration, these directories provide:
- Authentication endpoints
- Server discovery APIs 
- Standardized tool interfaces
- Usage metrics and monitoring
- Documentation and examples

[^1]: [Top 10 awesome MCP servers that can make your life easier](https://dev.to/composiodev/top-10-awesome-mcp-servers-that-can-make-your-life-easier-3n4o)
[^2]: [My Favorite MCP Directories](https://dev.to/techgirl1908/my-favorite-mcp-directories-573n)
[^3]: [The Top 7 MCP-Supported AI Frameworks](https://medium.com/@amosgyamfi/the-top-7-mcp-supported-ai-frameworks-a8e5030c87ab)


### Smithery API

From Smithery docs:

Request:

```python
# Python example using requests
import requests
from urllib.parse import quote

api_key = 'your-smithery-api-token'
query = 'owner:mem0ai is:verified memory'
encoded_query = quote(query)

response = requests.get(
    f'https://registry.smithery.ai/servers?q={encoded_query}&page=1&pageSize=10',
    headers={
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
)

data = response.json()
print(data)
```


Possible example code to query the Smithery API

```python
import httpx
from typing import Dict, List

async def search_smithery_servers(query: str, api_key: str, page: int = 1, page_size: int = 10) -> List[Dict]:
    """
    Search for MCP servers in the Smithery registry using keyword search.
    
    Args:
        query: Search query string for semantic search
        api_key: Smithery API key for authentication
        page: Page number for pagination (default: 1) 
        page_size: Number of results per page (default: 10)
        
    Returns:
        List of matching server records
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    params = {
        "q": query,
        "page": page,
        "pageSize": page_size
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.smithery.ai/v1/servers",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()["servers"]

# Example usage:
async def main():
    api_key = "your-smithery-api-key"
    results = await search_smithery_servers("web search", api_key)
    
    for server in results:
        print(f"Name: {server['displayName']}")
        print(f"Qualified name: {server['name']}")
        print("---")

```

# Functionality required

The MCP Squared tool provides an easy way for users of AI coding tools like Cursor IDE or Windsurf to find and add local MCP Servers and tools to their projects running on their local machines.

The MCP Squared Discovery Service API will be called from a locally running MCP Squared Server (being built as a companion to this) that is called from Cursor IDE, Claude Desktop, Windsurf etc.

The tool will recommend MCP Servers for the current project based on:
- Code and documentation already in the project passed to it
- The prompt in Cursor Chat or Agent that invokes the discovery tool

The user will invoke the tool by asking in Chat to set up useful MCP servers that will be helpful for coding the current project.

Basic workflow:

- The user invokes the tool from Chat or Agent.
- The local MCP Squared server analyses the code based, and finds any project specs or .mdc files and finds the package manager definition file (pyproject.toml, package.json)
- It calls the Discovery Service API with payload including: prompt, spec file atachments (.md, .mdc), package config files.
- The Discovery Service identifies a list of modules/packages or external API services required (eg supbase, mintlify etc)
- It searches for MCP Servers or Tools that can be used to integrate the Cursor or other IDE/coding tool with those tools. 
- The application will generate queries using an LLM for both a) API search for the above APIs, b) a google keyword search query using "(site:{domain.com} OR site:{domain2.com}...)" format
- The search can be done using both known APIs and web search using site:restriction.
- We will merge the results and then use an LLM to select the best matches.
- For each tool we retrieve source we retrieve the full page using a content retrieval API: `https://api.andisearch.com/parser/parser?url={page_url}`
- We use the provided context (project config, specs, prompt) with the retrieved markdown content from the page to construct a context and make an LLM call using langchain to openrouter to sonnet-3.5 to judge which of the found tools are most useful for the project.
- We then generate a list of summaries for each tool to be used with sources that includes: title of tool, it's github, any official project url, description of the tool, the commands to install and configure it, and an overview of other relevant information based on the project.
- The API then returns this information as a JSON obect with a list of MCP servers / tools that should be installed for the project.
- JSON response
	- title: title of the MCP Server or tool
	- github_url: the main repo url
	- project_url: vendor's own page with information about the url if additional to github
	- sources: list of sources used for the information
		- source_name: the domain of the directory website that the tool was found on
		- source_url: the page of the MCP Server or tool on the directory
		- source_title: the title of the directory page
		- source_description: the short description of the source page
	- cli_command: command line to install or configure
	- description: short description of the tool
	- content: markdown with an overview of the tool and summary of how to use it.

# Tech Stack

Python: We will use python 3.12.7 with pyenv and poetry, with pyproject.toml for package management.

How to set up a project with these:

``````markdown
# Setting Up a Python Project with Poetry and Pyenv

## Install Required Tools

1. Install pyenv to manage Python versions:
```bash
curl https://pyenv.run | bash
```

2. Install Python 3.12.7 using pyenv:
```bash
pyenv install 3.12.7
```

3. Install Poetry for dependency management:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Project Setup

1. Create and enter project directory:
```bash
mkdir my_project
cd my_project
```

2. Set local Python version:
```bash
pyenv local 3.12.7
```

3. Initialize Poetry project:
```bash
poetry init
```

## Configure pyproject.toml

Create or update pyproject.toml with project metadata[^1]:

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12.7"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Create Virtual Environment

1. Create and activate virtual environment:
```bash
poetry install
poetry shell
```

2. Verify Python version:
```bash
python --version
# Should output Python 3.12.7
```

## Project Structure

Create basic project structure[^2]:
```
my_project/
├── src/
│   └── my_project/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── README.md
└── pyproject.toml
```

## Adding Dependencies

Add project dependencies:
```bash
poetry add package_name
```

Add development dependencies:
```bash
poetry add --group dev pytest black flake8
```

[^1]: [Writing your pyproject.toml - Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
[^2]: [Python projects with Poetry and VSCode Part 1](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1)
``````

LLMs: Use langchain latest 

```````markdown
# Using LangChain ChatOpenAI with OpenRouter

Here's how to integrate OpenRouter with LangChain to access various open-source language models:

### Installation
```python
pip install langchain langchain-openai openai
```

### Basic Setup
```python
from langchain.chat_models import ChatOpenAI

chat_model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your_openrouter_api_key",  # Get from openrouter.ai/settings/keys
    model="qwen/qwen3-235b-a22b"  # Choose any model from openrouter.ai/models
)
```

### Creating a Simple Chat Chain
```python
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | chat_model

response = chain.invoke({"input": "Hello, how are you?"})
print(response.content)
```

### Streaming Responses
```python
for chunk in chain.stream({"input": "Tell me a short story"}):
    print(chunk.content, end="", flush=True)
```

### Adding Memory
```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=chat_model,
    memory=ConversationBufferMemory()
)

response = conversation.invoke("Hi, what's your name?")
```

OpenRouter provides API fallbacks and access to various models like Mistral, Claude, and Qwen[^1]. The service handles model deployment and offers pay-per-token pricing that's typically cheaper than closed-source alternatives[^1].

[^1]: [OpenRouter + LangChain: Leverage OpenSource models without the Ops hassle](https://medium.com/@gal.peretz/openrouter-langchain-leverage-opensource-models-without-the-ops-hassle-9ffbf0016da7)
```````

We want to use `anthropic/claude-3.5-sonnet` as the model here.


# MCP Squared Discovery Service Implementation

I'll create a mocked version of the API call and response for the MCP Squared Discovery Service. This will demonstrate how the service will work when fully implemented.

## Example API Call

Here's a Python example showing how to make a POST request to the Discovery Service API:

```python
import requests
import json

# API endpoint
url = "https://api.mcpsquared.dev/discover"

# Example prompt from the user
prompt = "I'm building a React application with Supabase for authentication and database. I need to integrate with Stripe for payments. Can you recommend MCP servers that would help me with this project?"

# Example .mdc file content (project specification)
mdc_content = """
# E-commerce Platform

## Overview
Building a modern e-commerce platform with React frontend, Supabase for authentication and database, and Stripe for payment processing.

## Features
- User authentication and profiles
- Product catalog and search
- Shopping cart functionality
- Secure payment processing with Stripe
- Order history and tracking
"""

# Example package.json content
package_json = """{
  "name": "ecommerce-platform",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@supabase/supabase-js": "^2.21.0",
    "@stripe/react-stripe-js": "^2.1.0",
    "@stripe/stripe-js": "^1.52.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.10.0",
    "tailwindcss": "^3.3.2"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^14.0.0",
    "@types/react": "^18.0.38",
    "typescript": "^5.0.4",
    "vite": "^4.3.1"
  }
}"""

# Create the multipart form data
files = {
    'prompt': (None, prompt),
    'project_spec.mdc': ('project_spec.mdc', mdc_content),
    'package.json': ('package.json', package_json)
}

# Make the POST request
response = requests.post(url, files=files)

# Print the response
print(json.dumps(response.json(), indent=2))
```

## Example JSON Response

Here's a mocked JSON response that the API would return:

```json
{
  "mcp_servers": [
    {
      "title": "Supabase MCP Server",
      "github_url": "https://github.com/modelcontextprotocol/supabase-mcp",
      "project_url": "https://supabase.com/docs/guides/ai/mcp-integration",
      "sources": [
        {
          "source_name": "mcpindex.net",
          "source_url": "https://mcpindex.net/en/servers/supabase-mcp",
          "source_title": "Supabase MCP Server - Database and Auth Integration",
          "source_description": "Connect your AI assistant to Supabase databases and authentication services"
        },
        {
          "source_name": "mcp.composio.dev",
          "source_url": "https://mcp.composio.dev/servers/supabase",
          "source_title": "Supabase MCP Server",
          "source_description": "Integrate Supabase with your AI coding assistant"
        }
      ],
      "cli_command": "npm install -g supabase-mcp-server && supabase-mcp setup",
      "description": "Official MCP server for Supabase that provides database operations, authentication management, and storage capabilities directly from your AI assistant.",
      "content": "# Supabase MCP Server\n\nThe Supabase MCP Server allows your AI assistant to interact directly with your Supabase project. It provides tools for:\n\n- Executing database queries\n- Managing user authentication\n- Handling file storage operations\n- Generating TypeScript types from your database schema\n\n## Key Features\n\n- **Database Operations**: Run SQL queries, manage tables, and perform CRUD operations\n- **Auth Management**: Create users, manage roles, and handle authentication flows\n- **Storage Integration**: Upload, download, and manage files in Supabase storage\n- **Schema Introspection**: Automatically understand your database structure\n\n## Configuration\n\nAfter installation, you'll need to configure your Supabase credentials:\n\n```json\n{\n  \"mcpServers\": {\n    \"supabase\": {\n      \"command\": \"supabase-mcp\",\n      \"env\": {\n        \"SUPABASE_URL\": \"your-project-url\",\n        \"SUPABASE_KEY\": \"your-api-key\"\n      }\n    }\n  }\n}\n```\n\nThis server is particularly useful for your React application as it will allow your AI assistant to help with database schema design, authentication flows, and generating the necessary TypeScript interfaces for your Supabase tables."
    },
    {
      "title": "Stripe MCP Server",
      "github_url": "https://github.com/modelcontextprotocol/stripe-mcp",
      "project_url": "https://stripe.com/docs/development/tools/mcp",
      "sources": [
        {
          "source_name": "mcpindex.net",
          "source_url": "https://mcpindex.net/en/servers/stripe-mcp",
          "source_title": "Stripe MCP Server - Payment Processing Integration",
          "source_description": "Integrate Stripe payment processing with your AI assistant"
        },
        {
          "source_name": "mcp-server-list.com",
          "source_url": "https://mcp-server-list.com/servers/stripe",
          "source_title": "Stripe MCP Server",
          "source_description": "Official Stripe MCP server for payment processing"
        }
      ],
      "cli_command": "npm install -g stripe-mcp-server && stripe-mcp init",
      "description": "Official MCP server for Stripe that enables payment processing, subscription management, and checkout integration directly through your AI assistant.",
      "content": "# Stripe MCP Server\n\nThe Stripe MCP Server provides a seamless way to integrate Stripe payment processing into your application with AI assistance. It offers tools for:\n\n- Creating and managing payment intents\n- Setting up subscription plans\n- Managing customers and payment methods\n- Generating checkout sessions\n\n## Key Features\n\n- **Payment Processing**: Create payment intents, handle card payments, and process refunds\n- **Subscription Management**: Create and manage subscription plans and customer subscriptions\n- **Customer Management**: Create and update customer records, manage payment methods\n- **Checkout Integration**: Generate checkout sessions for your React frontend\n\n## Configuration\n\nAfter installation, configure your Stripe API keys:\n\n```json\n{\n  \"mcpServers\": {\n    \"stripe\": {\n      \"command\": \"stripe-mcp\",\n      \"env\": {\n        \"STRIPE_SECRET_KEY\": \"sk_test_...\",\n        \"STRIPE_PUBLISHABLE_KEY\": \"pk_test_...\"\n      }\n    }\n  }\n}\n```\n\nThis server will be particularly valuable for implementing the payment processing features in your e-commerce platform, allowing your AI assistant to help generate the necessary code for Stripe integration in your React application."
    },
    {
      "title": "React DevTools MCP Server",
      "github_url": "https://github.com/modelcontextprotocol/react-devtools-mcp",
      "project_url": "https://react-devtools-mcp.dev",
      "sources": [
        {
          "source_name": "mcpservers.org",
          "source_url": "https://mcpservers.org/servers/react-devtools",
          "source_title": "React DevTools MCP Server",
          "source_description": "Enhance React development with AI-powered component generation and debugging"
        }
      ],
      "cli_command": "npx react-devtools-mcp-server",
      "description": "MCP server that provides React component generation, prop type analysis, and performance optimization suggestions for React applications.",
      "content": "# React DevTools MCP Server\n\nThe React DevTools MCP Server enhances your React development workflow by providing AI-powered assistance for component creation, debugging, and optimization.\n\n## Key Features\n\n- **Component Generation**: Create React components based on natural language descriptions\n- **Prop Type Analysis**: Automatically generate TypeScript interfaces for your components\n- **Performance Optimization**: Identify and fix performance bottlenecks in your React components\n- **State Management**: Get assistance with implementing Redux, Context API, or other state management solutions\n\n## Usage\n\nOnce installed, the React DevTools MCP Server will be available to your AI assistant. You can ask for help with:\n\n- Creating new React components\n- Debugging rendering issues\n- Optimizing component performance\n- Implementing state management patterns\n\nThis server is particularly useful for your React application as it will help you quickly scaffold components, implement best practices, and avoid common pitfalls in React development.\n\n## Example Commands\n\n- \"Generate a product card component for my e-commerce site\"\n- \"Help me implement a shopping cart using Context API\"\n- \"Optimize this component to prevent unnecessary re-renders\"\n- \"Create a form component for Stripe payment integration\""
    }
  ]
}
```

## Implementation Notes

The actual implementation will need to:

1. Set up a FastAPI backend to handle the POST requests with file attachments
2. Implement the logic to analyze the project files and prompt
3. Search for relevant MCP servers using the directory APIs and web search
4. Use LangChain with Claude 3.5 Sonnet via OpenRouter to evaluate and rank the results
5. Format the response as shown in the example JSON

The service will be containerized with Docker and deployed on Kubernetes using Porter, making it scalable and maintainable.

