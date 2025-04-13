from fastapi import HTTPException, status

from api.v1.movie.crud import DATABASE


async def find_movie_by_id(slug: str):
    film = next((item for item in DATABASE if item.slug == slug), None)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return film
