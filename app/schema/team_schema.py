from pydantic import BaseModel


class AssignTeamRequest(BaseModel):
    team_id: str
    user_id: str

class CreateTeamRequest(BaseModel):
    name : str
    description :str
    project_id : str

class CreateTeamResponse(BaseModel):
    success: bool
    message: str
    team_id: str
    
class AssignTeamResponse(BaseModel):
    success: bool
    message: str


