from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProjectContext(BaseModel):
    user_prompt: str
    project_mdc_file_contents: str
    project_package_manager_contents: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/project-context")
def read_project_context(project_context: ProjectContext) -> str:
    print(f"Received project context: {project_context.model_dump_json()}")
    return "Received project context"