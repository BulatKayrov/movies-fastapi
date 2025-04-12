from api.v1.movie.schemas import SMovie
from fastapi import HTTPException, status

DATABASE = [
    SMovie(movie_id=1, title="Terminator 1", description="Nice film 1", year=1999),
    SMovie(movie_id=2, title="Terminator 2", description="Nice film 2", year=2000),
    SMovie(movie_id=3, title="Terminator 3", description="Nice film 3", year=2001),
]


async def find_movie_by_id(movie_id: int):
    film = next((item for item in DATABASE if item.movie_id == movie_id), None)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film
