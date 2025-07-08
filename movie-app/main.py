import logging

import uvicorn
from api import router as api_router_v1
from app_lifespan import lifespan
from core.config import settings
from fastapi import FastAPI
from loguru import logger
from starlette.responses import RedirectResponse

app = FastAPI(
    title="Movies",
    version="1.0",
    description="Movie app",
    docs_url="/docs",
    lifespan=lifespan,
)
app.include_router(api_router_v1)
logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)
# logger = logging.getLogger(__name__)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/status-code-200")
def status_code_200() -> dict:
    return {"status_code": 200}


if __name__ == "__main__":
    logger.info("Starting server")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
