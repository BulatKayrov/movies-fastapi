import logging

from fastapi import HTTPException, status, BackgroundTasks

from api.v1.movie.crud import storage

logger = logging.getLogger(__name__)


def find_movie_by_slug(slug: str):
    film = storage.find_by_slug(slug)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film


def save_record(
    background_task: BackgroundTasks,
):
    yield
    logger.info("Saving movie record")
    background_task.add_task(storage.save())
