from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends

from api.v1.movie.crud import storage
from api.v1.movie.dependecies import api_or_basic, find_movie_by_slug
from api.v1.movie.schemas import SMovie, SMovieCreate, SMoviePartialUpdate, SMovieUpdate
from api.v1.movie.tools import RESPONSES

router = APIRouter(
    prefix="/movies",
    tags=["Фильмы"],
    dependencies=[
        Depends(api_or_basic),
        # Depends(basic_auth_header),
        # Depends(get_token),
    ],
)
logger = getLogger(__name__)


@router.get(path="/", name="movie:find_all")
def get_all_movies() -> list[SMovie]:
    return storage.find_all()


@router.get(path="/{slug}")
def get_one_movie(movie: Annotated[SMovie, Depends(find_movie_by_slug)]) -> SMovie:
    return movie


@router.post(path="/", name="movie:create")
def create_one_movie(data: SMovieCreate) -> SMovie:
    return storage.create(data=data)


@router.delete(
    path="/{slug}",
    responses=RESPONSES,
    status_code=status.HTTP_204_NO_CONTENT,
    name="movie:delete",
)
def delete_one_movie(movie: Annotated[SMovie, Depends(find_movie_by_slug)]) -> None:
    storage.delete_record(movie=movie)


@router.put(path="/{slug}", name="movie:update")
def update_one_movie(movie_in: SMovieUpdate, slug: str) -> SMovie:
    return storage.update_record(slug=slug, movie_in=movie_in)


@router.patch(path="/{slug}", name="movie:partial_update")
def partial_update(movie_in: SMoviePartialUpdate, slug: str) -> SMovie:
    return storage.update(slug=slug, movie_in=movie_in, partial=True)
