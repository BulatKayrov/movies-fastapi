from fastapi import APIRouter
from fastapi.params import Depends

from api.v1.movie.dependecies import DATABASE, find_movie_by_id
from api.v1.movie.schemas import SMovie

router = APIRouter(prefix="/movies", tags=["Фильмы"])


@router.get(path="/", response_model=list[SMovie])
async def get_all_movies():
    return DATABASE


@router.get(path="/{movie_id}", response_model=SMovie)
async def get_one_movie(movie=Depends(find_movie_by_id)):
    return movie
