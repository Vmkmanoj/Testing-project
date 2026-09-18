import os

from collections.abc import AsyncGenerator
from langchain_community.utilities import SQLDatabase

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()


engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    echo=False
)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


sync_url = os.getenv("DATABASE_URL").replace("+asyncpg", "+psycopg2") if os.getenv("DATABASE_URL") else ""
Sql_agent = SQLDatabase.from_uri(sync_url)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    """

    async with AsyncSessionLocal() as session:
        yield session