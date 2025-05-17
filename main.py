from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ProjectContext(BaseModel):
    user_prompt: str = Field(description="The user prompt for the project")
    project_mdc_file_contents: str = Field(description="The contents of the project's mdc file")
    project_package_manager_contents: str = Field(description="The contents of the project's package manager file eg package.json, pyproject.toml, cargo.toml, etc")

@app.post("/project-context")
def read_project_context(project_context: ProjectContext) -> str:
    print(f"Received project context: {project_context.model_dump_json()}")
    return get_reccomendations(project_context)


def get_reccomendations(project_context: ProjectContext) -> str:
    return """
    Here are some reccomendations for the project:
    FileSystem MCP server is a good choice for this project.
    It allows you to read the file system and get the contents of the files.
    This is useful for getting the contents of the project's files.
    You can use the following tools to get the contents of the files:
       - Read/write files
       - Create/list/delete directories
       - Move files/directories
       - Search files
       - Get file metadata

    Before installing this explain to the user that you will need to install it. and it is useful then run the command below. 

    To install it run:
    Docs for how to install it in claude code are here: https://docs.anthropic.com/en/docs/claude-code/tutorials#set-up-model-context-protocol-mcp

    claude mcp add <name> <command> [args...]

    eg claude mcp add filesystem npx @modelcontextprotocol/server-filesystem /Users/matthewdodd/Documents

    "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/path/to/other/allowed/dir"
      ]
    }
    """