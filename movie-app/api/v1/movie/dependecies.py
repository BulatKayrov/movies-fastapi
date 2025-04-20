import logging

from fastapi import HTTPException, status, BackgroundTasks, Request, Query, Depends

from api.v1.movie.crud import storage
from core.config import settings

logger = logging.getLogger(__name__)
UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def find_movie_by_slug(slug: str):
    film = storage.find_by_slug(slug)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film


def get_token(
    api_token: str = Query(),
):
    if api_token not in settings.API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )
    return api_token


def save_record(background_task: BackgroundTasks, request: Request):
    yield
    if request.method in UNSAFE_METHODS:
        logger.info("Saving movie record")
        background_task.add_task(storage.save())
