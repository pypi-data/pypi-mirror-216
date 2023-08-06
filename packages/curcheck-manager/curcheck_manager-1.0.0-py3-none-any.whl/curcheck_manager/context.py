from pydantic import BaseModel


class ProjectContext(BaseModel):
    project_name: str
    is_full: bool = False


class AppContext(BaseModel):
    app_name: str
