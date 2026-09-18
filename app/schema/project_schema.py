from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    status: str = "PLANNING"

    client_id: UUID


class AssignProjectRequest(BaseModel):
    team_id: str
    project_id: str


class CreateProjectResponse(BaseModel):
    success: bool
    message: str
    project_id: str


class AssignProjectResponse(BaseModel):
    success: bool
    message: str
