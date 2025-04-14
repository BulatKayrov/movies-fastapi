from fastapi import APIRouter, status
from fastapi.params import Depends

from api.tools import RESPONSES
from api.v1.movie.crud import storage
from api.v1.movie.dependecies import find_movie_by_slug
from api.v1.movie.schemas import SMovie, SMovieCreate, SMovieUpdate, SMoviePartialUpdate

router = APIRouter(prefix="/movies", tags=["Фильмы"])


@router.get(path="/", response_model=list[SMovie])
async def get_all_movies():
    return storage.find_all()


@router.get(path="/{slug}", response_model=SMovie)
async def get_one_movie(movie=Depends(find_movie_by_slug)):
    return movie


@router.post(path="/", response_model=SMovie)
async def create_one_movie(data: SMovieCreate):
    storage.create(data=data)
    return SMovie(**data.model_dump())


@router.delete(
    path="/{slug}", responses={**RESPONSES}, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_one_movie(movie=Depends(find_movie_by_slug)):
    storage.delete_record(movie=movie)


@router.put(path="/{slug}", response_model=SMovie)
async def update_one_movie(movie_in: SMovieUpdate, movie=Depends(find_movie_by_slug)):
    return storage.update_record(movie=movie, movie_in=movie_in)


@router.patch(path="/{slug}", response_model=SMovie)
async def partial_update(
    movie_in: SMoviePartialUpdate, movie=Depends(find_movie_by_slug)
):
    return storage.update(movie=movie, movie_in=movie_in, partial=True)
