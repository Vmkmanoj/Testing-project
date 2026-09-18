from app.api.auth import router as auth_router
from app.api.create_employee import router as create_employee_router
from app.api.create_client import router as create_client_router
from app.api.assign_team import router as assign_team_router
from app.api.project import router as project_router


__all__ = [
    "auth_router",
    "create_employee_router",
    "create_client_router",
    "assign_team_router",
    "project_router",
    
]