import logging

from api.v1.movie.schemas import SMovie, SMovieCreate, SMoviePartialUpdate, SMovieUpdate
from core.config import settings
from fastapi import HTTPException, status
from redis import Redis

logger = logging.getLogger(__name__)

redis_movie = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


class StorageMovie:

    @classmethod
    def save(cls, data: SMovie) -> None:
        redis_movie.hset(
            name=settings.REDIS_HASH_KEY_DB,
            key=data.slug,
            value=data.model_dump_json(),
        )

    @classmethod
    def find_all(cls) -> list[SMovie]:
        values = redis_movie.hvals(name=settings.REDIS_HASH_KEY_DB)
        return [SMovie.model_validate_json(item) for item in values]

    @classmethod
    def find_by_slug(cls, slug: str) -> SMovie:
        obj = redis_movie.hget(name=settings.REDIS_HASH_KEY_DB, key=slug)
        if obj:
            return SMovie.model_validate_json(obj)
        return None

    @classmethod
    def create(cls, data: SMovieCreate | SMovie) -> SMovie:
        new_movie = SMovie(**data.model_dump())
        if not cls.find_by_slug(slug=new_movie.slug):
            cls.save(data)
            logger.info("Mobie by slug created %s", new_movie.slug)
            return new_movie
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie exists")

    @classmethod
    def delete_by_slug(cls, slug: str) -> None:
        redis_movie.hdel(settings.REDIS_HASH_KEY_DB, slug)

    @classmethod
    def delete_record(cls, movie: SMovie) -> None:
        cls.delete_by_slug(slug=movie.slug)

    @classmethod
    def update_record(cls, slug: str, movie_in: SMovieUpdate) -> SMovie:
        obj = cls.find_by_slug(slug=slug)
        if obj:
            for key, value in movie_in:
                setattr(obj, key, value)
            cls.save(data=obj)
            return obj
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Movie not found"
        )

    @classmethod
    def update(
        cls, slug: str, movie_in: SMoviePartialUpdate, partial: bool = False
    ) -> SMovie:
        """Универсальный метод обновление записи"""
        obj = cls.find_by_slug(slug=slug)
        if obj:
            for key, value in movie_in.model_dump(
                exclude_none=partial,
                exclude_unset=partial,
            ).items():
                setattr(obj, key, value)
            cls.save(data=obj)
            return obj
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Movie not found"
        )


storage = StorageMovie()
