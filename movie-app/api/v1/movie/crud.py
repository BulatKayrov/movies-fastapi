import logging

from fastapi import HTTPException, status
from redis import Redis

from api.v1.movie.schemas import SMovie, SMovieCreate, SMoviePartialUpdate, SMovieUpdate
from core.config import settings

logger = logging.getLogger(__name__)

redis_movie = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


class StorageMovie:

    @classmethod
    def find_all(cls):
        values = redis_movie.hvals(name=settings.REDIS_HASH_KEY_DB)
        return [SMovie.model_validate_json(item) for item in values]

    @classmethod
    def find_by_slug(cls, slug: str):
        obj = redis_movie.hget(name=settings.REDIS_HASH_KEY_DB, key=slug)
        if obj:
            return SMovie.model_validate_json(obj)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    @classmethod
    def create(cls, data: SMovieCreate):
        new_movie = SMovie(**data.model_dump())
        slug = new_movie.slug

        if not redis_movie.hget(name=settings.REDIS_HASH_KEY_DB, key=slug):
            redis_movie.hset(
                name=settings.REDIS_HASH_KEY_DB,
                key=slug,
                value=new_movie.model_dump_json(),
            )

            logger.info("Mobie by slug created %s", slug)
            return new_movie
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie exists")

    @classmethod
    def delete_by_slug(cls, slug: str):
        redis_movie.hdel(settings.REDIS_HASH_KEY_DB, slug)

    @classmethod
    def delete_record(cls, movie: SMovie):
        cls.delete_by_slug(slug=movie.slug)

    @classmethod
    def update_record(cls, movie: SMovie, movie_in: SMovieUpdate):
        for key, value in movie_in:
            setattr(movie, key, value)

        return movie

    @classmethod
    def update(
        cls, movie: SMovie, movie_in: SMoviePartialUpdate, partial: bool = False
    ):
        """Универсальный метод обновление записи"""
        for key, value in movie_in.model_dump(
            exclude_none=partial,
            exclude_unset=partial,
        ).items():
            setattr(movie, key, value)

        return movie


storage = StorageMovie()
