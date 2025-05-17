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
    return "Received project context"