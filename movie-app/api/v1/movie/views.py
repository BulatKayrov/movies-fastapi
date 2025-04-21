from logging import getLogger

from fastapi import APIRouter, status
from fastapi.params import Depends

from api.tools import RESPONSES
from api.v1.movie.crud import storage
from api.v1.movie.dependecies import find_movie_by_slug, save_record, api_or_basic
from api.v1.movie.schemas import SMovie, SMovieCreate, SMovieUpdate, SMoviePartialUpdate

router = APIRouter(
    prefix="/movies",
    tags=["Фильмы"],
    dependencies=[
        Depends(save_record),
        Depends(api_or_basic),
        # Depends(basic_auth_header),
        # Depends(get_token),
    ],
)
logger = getLogger(__name__)


@router.get(
    path="/",
    response_model=list[SMovie],
)
def get_all_movies():
    return storage.find_all()


@router.get(path="/{slug}", response_model=SMovie)
def get_one_movie(movie=Depends(find_movie_by_slug)):
    return movie


@router.post(path="/", response_model=SMovie)
def create_one_movie(data: SMovieCreate):
    return storage.create(data=data)


@router.delete(
    path="/{slug}", responses={**RESPONSES}, status_code=status.HTTP_204_NO_CONTENT
)
def delete_one_movie(movie=Depends(find_movie_by_slug)):
    storage.delete_record(movie=movie)


@router.put(path="/{slug}", response_model=SMovie)
def update_one_movie(movie_in: SMovieUpdate, movie=Depends(find_movie_by_slug)):
    return storage.update_record(movie=movie, movie_in=movie_in)


@router.patch(path="/{slug}", response_model=SMovie)
def partial_update(movie_in: SMoviePartialUpdate, movie=Depends(find_movie_by_slug)):
    return storage.update(movie=movie, movie_in=movie_in, partial=True)
