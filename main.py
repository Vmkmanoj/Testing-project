from fastapi import FastAPI
from app.router import router as main_router
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import AsyncSessionLocal
from app.seed.seed_rbac import seed_rbac
from app.seed.seed_leave_types import seed_leave_types
from app.seed.seed_govermernt_holliday import seed_government_holidays
from contextlib import asynccontextmanager
from app.database.base import Base
from app.database.database import engine
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        await seed_rbac(db)
        await seed_leave_types(db)
        await seed_government_holidays()

    yield

    # Shutdown

app = FastAPI(
    lifespan=lifespan
    
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)



