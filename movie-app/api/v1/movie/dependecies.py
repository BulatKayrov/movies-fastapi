from api.v1.movie.crud import DATABASE
from fastapi import HTTPException, status


async def find_movie_by_id(movie_id: int):
    film = next((item for item in DATABASE if item.movie_id == movie_id), None)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film
