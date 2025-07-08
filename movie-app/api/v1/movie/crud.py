import logging

from core.config import settings
from fastapi import HTTPException, status
from redis import Redis

from api.v1.movie.schemas import SMovie, SMovieCreate, SMoviePartialUpdate, SMovieUpdate

logger = logging.getLogger(__name__)


class StorageMovie:

    def __init__(self, instance_redis: Redis) -> None:
        self.redis_movie = instance_redis

    def save(self, data: SMovie) -> None:
        self.redis_movie.hset(
            name=settings.REDIS_HASH_KEY_DB,
            key=data.slug,
            value=data.model_dump_json(),
        )

    def find_all(self) -> list[SMovie]:
        values = self.redis_movie.hvals(name=settings.REDIS_HASH_KEY_DB)
        return [SMovie.model_validate_json(item) for item in values]

    def find_by_slug(self, slug: str) -> SMovie | None:
        obj = self.redis_movie.hget(name=settings.REDIS_HASH_KEY_DB, key=slug)
        if obj:
            return SMovie.model_validate_json(obj)
        return None

    def create(self, data: SMovieCreate | SMovie) -> SMovie:
        new_movie = SMovie(**data.model_dump())
        if not self.find_by_slug(slug=new_movie.slug):
            self.save(data)
            logger.info("Mobie by slug created %s", new_movie.slug)
            return new_movie
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie exists")

    def delete_by_slug(self, slug: str) -> None:
        self.redis_movie.hdel(settings.REDIS_HASH_KEY_DB, slug)

    def delete_record(self, movie: SMovie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update_record(self, slug: str, movie_in: SMovieUpdate) -> SMovie:
        obj = self.find_by_slug(slug=slug)
        if obj:
            for key, value in movie_in:
                setattr(obj, key, value)
            self.save(data=obj)
            return obj
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Movie not found"
        )

    def update(
        self, slug: str, movie_in: SMoviePartialUpdate, partial: bool = False
    ) -> SMovie:
        """Универсальный метод обновление записи"""
        obj = self.find_by_slug(slug=slug)
        if obj:
            for key, value in movie_in.model_dump(
                exclude_none=partial,
                exclude_unset=partial,
            ).items():
                setattr(obj, key, value)
            self.save(data=obj)
            return obj
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Movie not found"
        )


redis_movie = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)

# storage = StorageMovie(testings_flag=True)
storage = StorageMovie(instance_redis=redis_movie)
