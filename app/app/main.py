from fastapi import FastAPI
from starlette.requests import Request

from app.core import config
from app.api.urls import root_router
from app.db.session import Session

app = FastAPI(title=config.PROJECT_TITLE, openapi_url="/api/v1/openapi.json")

app.include_router(root_router, prefix='/api')


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
