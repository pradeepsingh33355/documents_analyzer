from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import Optional, Dict
from app.core.config import settings
from app.api.v1 import document, user
from app.core.database import check_database_connection
from app.services.user_service import create_initial_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_database_connection()
    await create_initial_admin()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/user", tags=["user"])
app.include_router(
    document.router, prefix=f"{settings.API_V1_STR}/document", tags=["document"]
)

#
DOC_STORE: Dict[str, Dict] = {}
