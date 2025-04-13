import random
from typing import Annotated

from fastapi import APIRouter, Form
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


@router.post(path="/", response_model=SMovie)
async def create_one_movie(
    title: Annotated[str, Form(min_length=1, max_length=50)],
    description: Annotated[str, Form(min_length=1, max_length=50)],
    year: Annotated[int, Form(ge=1, le=1_000_000)],
):
    pk = random.randint(1, 1_000_000)
    movie = SMovie(movie_id=pk, title=title, description=description, year=year)
    DATABASE.append(movie)
    return movie
