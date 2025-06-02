import logging

import uvicorn
from api import router as api_router_v1
from app_lifespan import lifespan
from core.config import settings
from fastapi import FastAPI
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


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
