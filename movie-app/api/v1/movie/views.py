from logging import getLogger

from fastapi import APIRouter, status, BackgroundTasks
from fastapi.params import Depends

from api.tools import RESPONSES
from api.v1.movie.crud import storage
from api.v1.movie.dependecies import find_movie_by_slug
from api.v1.movie.schemas import SMovie, SMovieCreate, SMovieUpdate, SMoviePartialUpdate

router = APIRouter(prefix="/movies", tags=["Фильмы"])
logger = getLogger(__name__)


@router.get(path="/", response_model=list[SMovie])
def get_all_movies():
    return storage.find_all()


@router.get(path="/{slug}", response_model=SMovie)
def get_one_movie(movie=Depends(find_movie_by_slug)):
    return movie


@router.post(path="/", response_model=SMovie)
def create_one_movie(background_task: BackgroundTasks, data: SMovieCreate):
    background_task.add_task(storage.save())
    logger.info("Movie created")
    return storage.create(data=data)


@router.delete(
    path="/{slug}", responses={**RESPONSES}, status_code=status.HTTP_204_NO_CONTENT
)
def delete_one_movie(
    background_task: BackgroundTasks, movie=Depends(find_movie_by_slug)
):
    background_task.add_task(storage.save())
    storage.delete_record(movie=movie)
    logger.info("Movie deleted")


@router.put(path="/{slug}", response_model=SMovie)
def update_one_movie(
    movie_in: SMovieUpdate,
    background_task: BackgroundTasks,
    movie=Depends(find_movie_by_slug),
):
    background_task.add_task(storage.save())
    logger.info("Movie updated")
    return storage.update_record(movie=movie, movie_in=movie_in)


@router.patch(path="/{slug}", response_model=SMovie)
def partial_update(
    movie_in: SMoviePartialUpdate,
    background_task: BackgroundTasks,
    movie=Depends(find_movie_by_slug),
):
    background_task.add_task(storage.save())
    logger.info("Movie updated")
    return storage.update(movie=movie, movie_in=movie_in, partial=True)
