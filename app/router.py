from fastapi import APIRouter
from app.api import auth_router
from app.api import create_employee_router
from app.api import create_client_router
from app.api import project_router
from app.api import assign_team_router

from app.api.employee import router as employee_router
from app.api.client import router as client_router
from app.api.leave_type import router as leave_type_router
from app.api.leave_balance import router as leave_balance_router
from app.api.leave_request import router as leave_request_router
from app.api.agent import router as ai_agent

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(create_employee_router)
router.include_router(create_client_router)
router.include_router(project_router)
router.include_router(assign_team_router)

# Full CRUD routers
router.include_router(employee_router)
router.include_router(client_router)
router.include_router(leave_type_router)
router.include_router(leave_balance_router)
router.include_router(leave_request_router)
router.include_router(ai_agent)
