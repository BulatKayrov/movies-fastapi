import logging

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError
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


class StorageMovie(BaseModel):
    data_files: dict[str, SMovie] = {}  # {'slug': SMovie()}

    def init_storage(self) -> None:
        try:
            data = StorageMovie.from_statement()
        except ValidationError:
            self.save()
            logger.warning("Storage module reloaded")
            return

        self.data_files.update(data.data_files)
        logger.warning("Storage module loaded")

    def save(self):
        settings.DB_URL.write_text(self.model_dump_json(indent=4))
        logger.info("New movie saved")

    @classmethod
    def from_statement(cls):
        if not settings.DB_URL.exists():
            return StorageMovie()
        return cls.model_validate_json(settings.DB_URL.read_text())

    def find_all(self):
        return list(self.data_files.values())

    def find_by_slug(self, slug: str):
        obj = self.data_files.get(slug)
        return obj

    def create(self, data: SMovieCreate):
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

    def delete_by_slug(self, slug: str):
        self.data_files.pop(slug, None)

    def delete_record(self, movie: SMovie):
        self.delete_by_slug(slug=movie.slug)

    def update_record(self, movie: SMovie, movie_in: SMovieUpdate):
        for key, value in movie_in:
            setattr(movie, key, value)

        return movie

    def update(
        self, movie: SMovie, movie_in: SMoviePartialUpdate, partial: bool = False
    ):
        """Универсальный метод обновление записи"""
        for key, value in movie_in.model_dump(
            exclude_none=partial,
            exclude_unset=partial,
        ).items():
            setattr(movie, key, value)

        return movie


storage = StorageMovie()
