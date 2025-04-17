from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.movie.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    storage.init_storage()
    yield
    storage.save()
